from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdAccountCredentialViewSet, 
    AdCampaignViewSet, 
    dashboard_view, 
    signup_view, 
    signin_view, 
    adnetwork_game_view,
    fund_account_balance
)

router = DefaultRouter()
router.register(r'credentials', AdAccountCredentialViewSet)
router.register(r'campaigns', AdCampaignViewSet)

urlpatterns = [
    path('', adnetwork_game_view, name='root-network-matrix'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('network-matrix/', adnetwork_game_view, name='network-matrix'),
    path('fund-balance/', fund_account_balance, name='fund-balance'),
    path('', include(router.urls)),
]