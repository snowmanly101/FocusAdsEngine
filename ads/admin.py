from django.contrib import admin
from .models import UserCompanyProfile, AdCampaign

@admin.register(UserCompanyProfile)
class UserCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'registration_number', 'account_balance', 'subscription_paid', 'face_verified', 'is_approved_by_owner', 'created_at')
    list_filter = ('is_approved_by_owner', 'subscription_paid', 'face_verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'registration_number')

@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'platforms', 'budget', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'profile__company_name')