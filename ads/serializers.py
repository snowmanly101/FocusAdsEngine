from rest_framework import serializers
from .models import AdCampaign

class AdCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdCampaign
        fields = ['id', 'profile', 'title', 'platforms', 'budget', 'ad_video', 'status', 'created_at']