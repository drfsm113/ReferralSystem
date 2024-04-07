from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


# <editor-fold desc="User Registration">
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Serializes user data including username, email, password, and referral_code.
    """
    email = serializers.EmailField(required=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_referral_code(self, value):
        """
        Validates referral_code.
        """
        if value:
            if not UserProfile.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("Invalid referral code.")
        return value

    def validate_email(self, value):
        """
        Validates email uniqueness.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        try:
            user = User.objects.create_user(**validated_data)
            if referral_code:
                referred_by = UserProfile.objects.filter(referral_code=referral_code).first()
                if referred_by:
                    Referral.objects.create(referrer=referred_by, referred_user=user.userprofile)
                    referral_points, _ = ReferralPoints.objects.get_or_create(user=referred_by.user)
                    referral_points.points += 1
                    referral_points.save()
            return user
        except Exception as e:
            raise serializers.ValidationError("Failed to create user.") from e
# </editor-fold>

# <editor-fold desc="User Details">
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Serializes user profile data including user details, referral code, and registration date.
    """
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'referral_code', 'registration_date']
# </editor-fold>


# <editor-fold desc="Referrals">
class ReferralSerializer(serializers.ModelSerializer):
    """
    Serializer for the Referral model.

    Serializes referral data including referred user and registration date.
    """
    referred_user = UserProfileSerializer()

    class Meta:
        model = Referral
        fields = ['referred_user', 'registration_date']
# </editor-fold>
