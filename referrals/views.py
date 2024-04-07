from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserProfile, Referral
from .serializers import UserProfileSerializer, ReferralSerializer
from .serializers import UserSerializer


# <editor-fold desc="user registration">
class UserRegistration(generics.CreateAPIView):
    """
    Endpoint for user registration.

    Accepts POST requests with user data including username, email, password, and referral_code.
    Optional field: referral_code (if provided, the user who referred this user receives a point).
    Returns a unique user ID and a success message upon successful registration.
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id, 'message': 'User registered successfully.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# </editor-fold>


# <editor-fold desc="user details view by id">
class UserDetails(APIView):
    """
    Endpoint for retrieving user details.

    Accepts GET requests with a valid token in the Authorization header.
    Returns the user's details including name, email, referral code, and registration date.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]  # Require authentication
    # authentication_classes = [JWTAuthentication, ]  # Require authentication


    def get(self, request, pk):
        # Retrieve the user profile object or return 400 if not found
        try:
            user_profile = UserProfile.objects.get(user_id=pk)
        except:
            return Response({"message": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the user profile data
        serializer = UserProfileSerializer(user_profile)

        # Return the serialized data as response
        return Response(serializer.data, status=status.HTTP_200_OK)


# </editor-fold>


# <editor-fold desc="referral users list">
class ReferralsList(generics.ListAPIView):
    """
    Endpoint for retrieving user referrals.

    Accepts GET requests with a valid token in the Authorization header.
    Returns a list of users who registered using the current user's referral code (if any).
    Returns a paginated response with 20 users per page.
    Returns the timestamp of registration for each referral.
    """
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JWTAuthentication, ]
    pagination_class = PageNumberPagination  # Pagination configured

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return Referral.objects.filter(referrer=user_profile)
# </editor-fold>
