from django.db import models
from django.contrib.auth.models import User

class UserCompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    id_document = models.FileField(upload_to='kyc_ids/', blank=True, null=True)
    face_verified = models.BooleanField(default=False)
    verification_method = models.CharField(max_length=50, default='face')
    api_interview_status = models.CharField(max_length=50, default='pending')
    subscription_paid = models.BooleanField(default=False)
    btc_tx_hash = models.CharField(max_length=255, blank=True, null=True)
    is_approved_by_owner = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

class AdCampaign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review & Deployment'),
        ('active', 'Active & Running'),
        ('flagged', 'Flagged & Removed (Terms Violation)'),
        ('completed', 'Completed'),
    ]
    
    OBJECTIVE_CHOICES = [
        ('website', 'Website Traffic & Conversions'),
        ('lead', 'Lead Generation'),
        ('sales', 'Direct Sales / E-commerce'),
        ('awareness', 'Brand Awareness'),
    ]

    profile = models.ForeignKey(UserCompanyProfile, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    campaign_objective = models.CharField(max_length=50, choices=OBJECTIVE_CHOICES, default='website')
    description = models.TextField(blank=True, null=True)
    
    # Targeting Fields
    target_audience_type = models.CharField(max_length=20, default='general')
    target_age = models.CharField(max_length=50, blank=True, null=True, default='General (All Ages)')
    target_countries = models.CharField(max_length=255, blank=True, null=True, default='Global / Worldwide')
    target_gender = models.CharField(max_length=20, default='all', blank=True, null=True)

    platforms = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    ad_video = models.FileField(upload_to='ad_videos/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - (${self.budget})"