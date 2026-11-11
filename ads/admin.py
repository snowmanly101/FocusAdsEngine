from django.contrib import admin
from .models import UserCompanyProfile, AdAccountCredential, AdCampaign

@admin.register(UserCompanyProfile)
class UserCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'registration_number', 'account_balance', 'kyc_status', 'facial_verification_verified')
    list_filter = ('kyc_status', 'facial_verification_verified')
    search_fields = ('company_name', 'registration_number', 'user__username')

@admin.register(AdAccountCredential)
class AdAccountCredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform_name', 'account_id', 'is_active', 'created_at')
    list_filter = ('platform_name', 'is_active')

@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'user', 'campaign_type', 'daily_budget', 'status', 'created_at')
    list_filter = ('status', 'campaign_type')
    search_fields = ('campaign_name', 'user__username')