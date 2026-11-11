from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AdAccountCredential, AdCampaign
from .serializers import AdAccountCredentialSerializer, AdCampaignSerializer
from .services import AdEngineBotService

def dashboard_view(request):
    """Renders the custom frontend dashboard for the ad engine bot."""
    return render(request, 'ads/dashboard.html')

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
        
        # Initialize our bot engine service
        bot_service = AdEngineBotService(campaign)
        result = bot_service.deploy_campaign()
        
        if result.get("status") == "success":
            campaign.status = 'active'
            campaign.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)