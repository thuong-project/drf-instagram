import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .serializers import UserSerializer
from rest_framework.test import APIClient


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'test0', 'password': '111111'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test0')


class AuthenticateTests(APITestCase):
    USER = {"username": "test0", "password": "111111"}

    def setUp(self) -> None:
        user = UserSerializer(data=self.USER)
        if user.is_valid():
            user.save()

    def test_jwt(self):
        response = self.client.post('/api/token/', self.USER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        me = self.client.get('/api/users/me/')
        self.assertEqual(me.status_code, status.HTTP_200_OK)

    # @unittest.skip("demonstrating skipping")
    # def test_log_in_facebook(self):
    #     data = {
    #             'grant_type': 'convert_token',
    #             'client_id': 'o1qsztCVa2xPHko0V5lWLuVR4qan9jRwjMClfggl',
    #             'client_secret': 'qtoC4RK2jx0f5u4B8AXhMp1Nsyv28lGoXJanh4629rjqakRtqTiIg5dt4uFZ11SaiGHOFUDNS7vmS33b0jXgyBDcrNSxUslFJXxSvRObUULXoFzAoz9BCuX8sL0OqGD3',
    #             'backend': 'facebook',
    #             'token': 'EAAPCJKO2LYcBAOOBimTGnyGNCYdDLzjgRF5iXfcQ2REoQ8ZAvBUfYOENVGxZBmmXj6HZCHEa2s7GiQkL65C1TahJXmZCXBV9jnFot5wyrbIDnPlO7BtG9Sgv3hkOApvVMXTd7DyYv9kjRi0a2TK07oOrENqAZCXT9mj4E5u4axQZDZD'
    #             }
    #     self.client.credentials()
    #     response = self.client.post('/auth/convert-token/', data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer '+response["access_token"])
    #     me = self.client.get('/api/users/me/')
    #     self.assertEqual(me.status_code, status.HTTP_200_OK)
