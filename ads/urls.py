from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdAccountCredentialViewSet, AdCampaignViewSet, dashboard_view, fund_account_balance

router = DefaultRouter()
router.register(r'credentials', AdAccountCredentialViewSet)
router.register(r'campaigns', AdCampaignViewSet)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('fund-balance/', fund_account_balance, name='fund-balance'),
    path('', include(router.urls)),
]