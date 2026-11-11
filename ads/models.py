from django.db import models
from django.contrib.auth.models import User

class UserCompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    id_document = models.FileField(upload_to='kyc_ids/', blank=True, null=True)
    face_verified = models.BooleanField(default=False)
    is_approved_by_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

class AdAccountCredential(models.Model):
    PLATFORM_CHOICES = [
        ('meta', 'Meta Ads'),
        ('google', 'Google Ads'),
        ('tiktok', 'TikTok Ads'),
    ]
    profile = models.ForeignKey(UserCompanyProfile, on_delete=models.CASCADE, related_name='credentials')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    access_token = models.TextField()
    ad_account_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

class AdCampaign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Deployment'),
        ('active', 'Active & Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    profile = models.ForeignKey(UserCompanyProfile, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    platform = models.CharField(max_length=20)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.platform} (${self.budget})"