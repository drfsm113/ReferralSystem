import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Represents a user profile.

    Attributes:
        user (OneToOneField): The corresponding user instance.
        referral_code (CharField): The referral code for the user.
        registration_date (DateTimeField): The timestamp of user registration.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def generate_referral_code():
    """
    Function to generate a unique referral code.
    """
    characters = string.ascii_letters + string.digits
    referral_code = ''.join(random.choice(characters) for _ in range(6))
    return referral_code


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile and generate a referral code when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance, referral_code=generate_referral_code())


class Referral(models.Model):
    """
    Represents a referral made by a user.

    Attributes:
        referrer (ForeignKey): The user who made the referral.
        referred_user (ForeignKey): The user who was referred.
        registration_date (DateTimeField): The timestamp of referral registration.
    """
    referrer = models.ForeignKey(UserProfile, related_name='referrals', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(UserProfile, related_name='referred_by', on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_user.user.username} referred by {self.referrer.user.username}"


class ReferralPoints(models.Model):
    """
    Represents referral points earned by users.

    Attributes:
        user (OneToOneField): The user associated with the points.
        points (IntegerField): The number of points earned.
        timestamp (DateTimeField): The timestamp of when the points were earned.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.points} points"
