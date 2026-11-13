from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import UserCompanyProfile, AdAccountCredential, AdCampaign
from .serializers import AdAccountCredentialSerializer, AdCampaignSerializer
from .services import AdEngineBotService

def signin_view(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            profile, _ = UserCompanyProfile.objects.get_or_create(user=user)
            if not profile.is_approved_by_owner:
                return redirect('pending-approval')
            return redirect('dashboard')
        else:
            error = "Invalid username or password."
    return render(request, 'ads/signin.html', {'error': error})

def signup_view(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        email = request.POST.get('email')
        p = request.POST.get('password')
        c_name = request.POST.get('company_name')
        reg_no = request.POST.get('registration_number')
        
        if User.objects.filter(username=u).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(username=u, email=email, password=p)
            UserCompanyProfile.objects.create(
                user=user, 
                company_name=c_name, 
                registration_number=reg_no,
                is_approved_by_owner=False
            )
            login(request, user)
            return redirect('dashboard')
    return render(request, 'ads/signup.html', {'error': error})

def verify_identity_view(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserCompanyProfile, user=request.user)
        if 'id_document' in request.FILES:
            profile.id_document = request.FILES['id_document']
        profile.face_verified = True
        profile.save()
        return redirect('pending-approval')
    return render(request, 'ads/verify.html')

def pending_approval_view(request):
    return render(request, 'ads/pending.html')

def owner_portal_view(request):
    secret_code = request.GET.get('code') or request.POST.get('code')
    if secret_code != 'CELOOH2026ADMIN':
        return render(request, 'ads/owner_login.html')
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action_type = request.POST.get('action_type')
        profile = get_object_or_404(UserCompanyProfile, id=profile_id)
        if action_type == 'approve':
            profile.is_approved_by_owner = True
            profile.save()
        elif action_type == 'reject':
            profile.delete()
        return redirect('/owner-matrix/?code=CELOOH2026ADMIN')

    pending_profiles = UserCompanyProfile.objects.filter(is_approved_by_owner=False)
    approved_profiles = UserCompanyProfile.objects.filter(is_approved_by_owner=True)
    return render(request, 'ads/owner_portal.html', {
        'pending_profiles': pending_profiles,
        'approved_profiles': approved_profiles
    })

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    profile, _ = UserCompanyProfile.objects.get_or_create(user=request.user)
    if not profile.is_approved_by_owner and not request.user.is_superuser:
        return redirect('pending-approval')
    
    campaigns = AdCampaign.objects.filter(profile=profile)
    return render(request, 'ads/dashboard.html', {'profile': profile, 'campaigns': campaigns})

def adnetwork_game_view(request):
    return render(request, 'ads/network_matrix.html')

@api_view(['POST'])
def fund_account_balance(request):
    username = request.data.get('username')
    amount = request.data.get('amount')
    if not username or not amount:
        return Response({"error": "Username and amount required."}, status=status.HTTP_400_BAD_REQUEST)
    profile = get_object_or_404(UserCompanyProfile, user__username=username)
    profile.account_balance += float(amount)
    profile.save()
    return Response({"status": "success", "new_balance": profile.account_balance}, status=status.HTTP_200_OK)

class AdAccountCredentialViewSet(viewsets.ModelViewSet):
    queryset = AdAccountCredential.objects.all()
    serializer_class = AdAccountCredentialSerializer

class AdCampaignViewSet(viewsets.ModelViewSet):
    queryset = AdCampaign.objects.all()
    serializer_class = AdCampaignSerializer

    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        campaign = self.get_object()
        bot_service = AdEngineBotService(campaign)
        result = bot_service.deploy_campaign()
        if result.get("status") == "success":
            campaign.status = 'active'
            campaign.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)