from rest_framework import serializers
from .models import AdAccountCredential, AdCampaign

class AdAccountCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdAccountCredential
        fields = ['id', 'user', 'platform_name', 'account_id', 'access_token', 'is_active', 'created_at']
        extra_kwargs = {'access_token': {'write_only': True}}  # Keeps tokens secure

class AdCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdCampaign
        fields = ['id', 'user', 'credential', 'campaign_name', 'objective', 'daily_budget', 'status', 'created_at']