from django.contrib import admin
from .models import UserCompanyProfile, AdAccountCredential, AdCampaign

@admin.register(UserCompanyProfile)
class UserCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'registration_number', 'account_balance', 'face_verified', 'is_approved_by_owner', 'created_at')
    list_filter = ('is_approved_by_owner', 'face_verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'registration_number')

@admin.register(AdAccountCredential)
class AdAccountCredentialAdmin(admin.ModelAdmin):
    list_display = ('profile', 'platform', 'ad_account_id', 'is_active')
    list_filter = ('platform', 'is_active')

@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'platform', 'budget', 'status', 'created_at')
    list_filter = ('platform', 'status', 'created_at')
    search_fields = ('title', 'profile__company_name')