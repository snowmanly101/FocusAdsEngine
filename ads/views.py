from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import secrets
from .models import UserCompanyProfile, AdCampaign
from .serializers import AdCampaignSerializer
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
            if not profile.subscription_paid:
                return redirect('btc-subscription')
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
        user_api_key = request.POST.get('user_api_key', '').strip()
        
        if User.objects.filter(username=u).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(username=u, email=email, password=p)
            has_valid_api = bool(user_api_key)
            
            # If they provided an API key, generate/save it and auto-approve
            if not user_api_key and has_valid_api:
                user_api_key = f"FAE-API-{secrets.token_hex(8).upper()}"
            
            UserCompanyProfile.objects.create(
                user=user, 
                company_name=c_name, 
                registration_number=reg_no,
                verification_method='api' if has_valid_api else 'subscription',
                face_verified=True, 
                subscription_paid=has_valid_api,
                is_approved_by_owner=has_valid_api,
                api_key=user_api_key
            )
            login(request, user)
            
            if has_valid_api:
                return redirect('dashboard')
            return redirect('btc-subscription')
            
    return render(request, 'ads/signup.html', {'error': error})

def btc_subscription_view(request):
    profile = get_object_or_404(UserCompanyProfile, user=request.user)
    if request.method == 'POST':
        tx_hash = request.POST.get('btc_tx_hash')
        if tx_hash:
            profile.btc_tx_hash = tx_hash
            profile.subscription_paid = True
            
            # Automatically generate an API key upon successful payment if none exists
            if not profile.api_key:
                profile.api_key = f"FAE-API-{secrets.token_hex(8).upper()}"
            
            profile.is_approved_by_owner = True
            profile.save()
            return redirect('dashboard')
    return render(request, 'ads/btc_subscription.html', {'profile': profile})

def verify_identity_view(request):
    profile = get_object_or_404(UserCompanyProfile, user=request.user)
    if request.method == 'POST':
        if 'id_document' in request.FILES:
            profile.id_document = request.FILES['id_document']
        profile.face_verified = True
        profile.save()
        return redirect('pending-approval')
    return render(request, 'ads/verify.html', {'profile': profile})

def api_interview_view(request):
    profile = get_object_or_404(UserCompanyProfile, user=request.user)
    if request.method == 'POST':
        profile.api_interview_status = 'recorded_and_reviewed'
        profile.save()
        return redirect('pending-approval')
    return render(request, 'ads/api_interview.html', {'profile': profile})

def pending_approval_view(request):
    profile = get_object_or_404(UserCompanyProfile, user=request.user)
    if profile.is_approved_by_owner:
        return redirect('dashboard')
    
    error = None
    success_msg = None
    
    if request.method == 'POST':
        form_action = request.POST.get('form_action')
        
        if form_action == 'submit_api':
            entered_key = request.POST.get('api_key', '').strip()
            if entered_key:
                profile.api_key = entered_key
                profile.is_approved_by_owner = True
                profile.save()
                return redirect('dashboard')
            else:
                error = "Please enter a valid API key."
                
        elif form_action == 'contact_verification':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            if full_name and email:
                success_msg = "Verification details received! Our team will contact you via email to schedule your AnyDesk interview."
            else:
                error = "Please fill in your full name and email."
                
    return render(request, 'ads/pending.html', {
        'profile': profile,
        'error': error,
        'success_msg': success_msg
    })

def about_view(request):
    return render(request, 'ads/about.html')

def feedback_view(request):
    success = False
    if request.method == 'POST':
        success = True
    return render(request, 'ads/feedback.html', {'success': success})

def terms_view(request):
    return render(request, 'ads/terms.html')

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

    pending_profiles = UserCompanyProfile.objects.filter(is_approved_by_owner=False, subscription_paid=True)
    approved_profiles = UserCompanyProfile.objects.filter(is_approved_by_owner=True)
    return render(request, 'ads/owner_portal.html', {
        'pending_profiles': pending_profiles,
        'approved_profiles': approved_profiles
    })

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    profile, _ = UserCompanyProfile.objects.get_or_create(user=request.user)
    if not profile.subscription_paid:
        return redirect('btc-subscription')
    if not profile.is_approved_by_owner and not request.user.is_superuser:
        return redirect('pending-approval')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        platforms_list = request.POST.getlist('platforms')
        platforms_str = ",".join(platforms_list)
        budget = request.POST.get('budget')
        ad_video = request.FILES.get('ad_video')
        
        AdCampaign.objects.create(
            profile=profile,
            title=title,
            platforms=platforms_str,
            budget=budget,
            ad_video=ad_video,
            status='active'
        )
        return redirect('dashboard')

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

class AdCampaignViewSet(viewsets.ModelViewSet):
    queryset = AdCampaign.objects.all()
    serializer_class = AdCampaignSerializer