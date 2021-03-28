import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .serializers import UserFullInfoSerializer
from oauth2_provider.models import Application
from instagram.settings import env


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('users-list')
        data = {'username': 'test0', 'password': '111111'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test0')


class JwtTests(APITestCase):
    USER = {"username": "test0", "password": "111111"}

    def setUp(self) -> None:
        user = UserFullInfoSerializer(data=self.USER)
        if user.is_valid():
            user.save()

    def test_jwt(self):
        response = self.client.post('/api/token/', self.USER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        me = self.client.get('/api/users/me/')
        self.assertEqual(me.status_code, status.HTTP_200_OK)


# @unittest.skip("demonstrating skipping")
class OAuthTests(APITestCase):

    def setUp(self) -> None:
        user = User.objects.create(username="admin", is_superuser=True)
        self.app = Application.objects.create(user=user, client_type="confidential", authorization_grant_type="password")

    def test_log_in_facebook(self):
        data = {
            'grant_type': 'convert_token',
            'client_id': self.app.client_id,
            'client_secret': self.app.client_secret,
            'backend': 'facebook',
            'token': env('FB_ACCESS_TOKEN')
        }
        self.client.credentials()
        response = self.client.post('/api/auth/convert-token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data["access_token"])
        me = self.client.get('/api/users/me/')
        self.assertEqual(me.status_code, status.HTTP_200_OK)
