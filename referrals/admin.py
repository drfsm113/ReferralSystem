from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Referral, ReferralPoints


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'registration_date']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_user', 'registration_date']


@admin.register(ReferralPoints)
class ReferralPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'timestamp']
