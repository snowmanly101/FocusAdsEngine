from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedTextField

class UserCompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    business_address = models.TextField()
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    id_document = models.FileField(upload_to='kyc_ids/', blank=True, null=True)
    facial_verification_verified = models.BooleanField(default=False)
    kyc_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class AdAccountCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=50)
    account_id = models.CharField(max_length=100)
    access_token = EncryptedTextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform_name} ({self.account_id})"


class AdCampaign(models.Model):
    CAMPAIGN_TYPES = [
        ('traffic', 'Website Traffic'),
        ('conversions', 'Sales & Conversions'),
        ('leads', 'Lead Generation'),
        ('engagement', 'Social Engagement'),
        ('video_views', 'Video Views'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credential = models.ForeignKey(AdAccountCredential, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPES, default='conversions')
    objective = models.CharField(max_length=100)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.campaign_name} [{self.campaign_type}]"