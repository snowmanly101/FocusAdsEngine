from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdAccountCredentialViewSet, 
    AdCampaignViewSet, 
    dashboard_view, 
    signup_view, 
    signin_view, 
    verify_identity_view,
    api_interview_view,
    pending_approval_view,
    about_view,
    feedback_view,
    terms_view,
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
    path('signup/', signup_view, name='signup'),
    path('verify/', verify_identity_view, name='verify-identity'),
    path('api-interview/', api_interview_view, name='api-interview'),
    path('pending/', pending_approval_view, name='pending-approval'),
    path('about/', about_view, name='about'),
    path('feedback/', feedback_view, name='feedback'),
    path('terms/', terms_view, name='terms'),
    path('owner-matrix/', owner_portal_view, name='owner-portal'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('network-matrix/', adnetwork_game_view, name='network-matrix'),
    path('fund-balance/', fund_account_balance, name='fund-balance'),
    path('', include(router.urls)),
]