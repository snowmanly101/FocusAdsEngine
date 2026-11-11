from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import UserCompanyProfile, AdAccountCredential, AdCampaign
from .serializers import AdAccountCredentialSerializer, AdCampaignSerializer
from .services import AdEngineBotService

def dashboard_view(request):
    """Renders the custom frontend dashboard for the ad engine bot."""
    return render(request, 'ads/dashboard.html')

def signup_view(request):
    """Renders the global animated signup page."""
    return render(request, 'ads/signup.html')

def signin_view(request):
    """Renders the global animated sign in page."""
    return render(request, 'ads/signin.html')

def adnetwork_game_view(request):
    """Renders the interactive Network Matrix game and simulation view."""
    return render(request, 'ads/network_matrix.html')

@api_view(['POST'])
def fund_account_balance(request):
    """
    API endpoint to add funds to a user's company profile balance.
    Expects JSON: {"username": "...", "amount": 100.00}
    """
    username = request.data.get('username')
    amount = request.data.get('amount')

    if not username or not amount:
        return Response({"error": "Username and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile, created = UserCompanyProfile.objects.get_or_create(
            user__username=username,
            defaults={'company_name': f"{username}'s Company", 'registration_number': 'PENDING'}
        )
        profile.account_balance += float(amount)
        profile.save()
        return Response({
            "status": "success",
            "message": f"Successfully added ${amount} to account.",
            "new_balance": profile.account_balance
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdAccountCredentialViewSet(viewsets.ModelViewSet):
    queryset = AdAccountCredential.objects.all()
    serializer_class = AdAccountCredentialSerializer

class AdCampaignViewSet(viewsets.ModelViewSet):
    queryset = AdCampaign.objects.all()
    serializer_class = AdCampaignSerializer

    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        """
        Custom API action to trigger the Ad Engine Bot for a specific campaign.
        URL: /api/campaigns/{id}/deploy/
        """
        campaign = self.get_object()
        bot_service = AdEngineBotService(campaign)
        result = bot_service.deploy_campaign()
        
        if result.get("status") == "success":
            campaign.status = 'active'
            campaign.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)