from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdAccountCredentialViewSet, 
    AdCampaignViewSet, 
    dashboard_view, 
    signup_view, 
    signin_view, 
    verify_identity_view,
    pending_approval_view,
    owner_portal_view,
    adnetwork_game_view,
    fund_account_balance
)

router = DefaultRouter()
router.register(r'credentials', AdAccountCredentialViewSet)
router.register(r'campaigns', AdCampaignViewSet)

urlpatterns = [
    path('', signin_view, name='root-signin'),
    path('signin/', signin_view, name='signin'),
    path('api/signin/', signin_view, name='api-signin'),
    path('signup/', signup_view, name='signup'),
    path('api/signup/', signup_view, name='api-signup'),
    path('verify/', verify_identity_view, name='verify-identity'),
    path('api/verify/', verify_identity_view, name='api-verify-identity'),
    path('pending/', pending_approval_view, name='pending-approval'),
    path('owner-matrix/', owner_portal_view, name='owner-portal'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/dashboard/', dashboard_view, name='api-dashboard'),
    path('network-matrix/', adnetwork_game_view, name='network-matrix'),
    path('fund-balance/', fund_account_balance, name='fund-balance'),
    path('', include(router.urls)),
]