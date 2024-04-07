from django.urls import path
from .views import UserRegistration, UserDetails, ReferralsList

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('user/<int:pk>/', UserDetails.as_view(), name='user-details'),
    path('referrals/', ReferralsList.as_view(), name='referrals-list'),
]
