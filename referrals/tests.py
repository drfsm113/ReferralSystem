import logging  # Import the logging module

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token  # Import Token model
from referrals.models import UserProfile, Referral

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)


# <editor-fold desc="user register test pass">
class UserRegistrationTestCase(APITestCase):
    def test_user_registration_without_referral_code(self):
        url = reverse('register')
        data = {'username': 'test_user', 'email': 'test@example.com', 'password': 'test123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('user_id' in response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_registration_with_valid_referral_code(self):
        url = reverse('register')
        referral_user = User.objects.create_user(username='referrer', email='referrer@example.com', password='test123')
        data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test123',
            'referral_code': referral_user.userprofile.referral_code
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('user_id' in response.data)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserProfile.objects.count(), 2)

    def test_user_registration_with_invalid_referral_code(self):
        url = reverse('register')
        data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test123',
            'referral_code': 'invalid_code'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
# </editor-fold>


# <editor-fold desc="user details">

class UserDetailsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')

    def test_get_user_details_authenticated(self):
        url = f'/api/user/{self.user.pk}/'

        # Log in the user
        self.client.login(username='test_user', password='test_password')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)



# </editor-fold>


# # <editor-fold desc="referral">
class ReferralsListTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='test123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='test123')
        self.referral = Referral.objects.create(referrer=self.user1.userprofile, referred_user=self.user2.userprofile)

    def test_referrals_list(self):
        url = reverse('referrals-list')
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# # </editor-fold>
#
