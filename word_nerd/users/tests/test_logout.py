from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .utils_test import register_and_login_user


class LogoutTest(APITestCase):
    url = reverse('logout')

    def test_logout_user(self):
        token = register_and_login_user(self.client).data['token']
        response = self.client.post(self.url, token, format='json')
        self.assertEqual(len(Token.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "logout successful")

    def test_logout_user_not_logged_in(self):
        self.assertEqual(len(Token.objects.all()), 0)
        response = self.client.post(self.url, format='json')
        self.assertEqual(len(Token.objects.all()), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "you weren't logged in")
