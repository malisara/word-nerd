from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .utils_test import register_and_login_user


class LogoutTest(APITestCase):
    url = reverse('logout')

    def test_logout_user(self):
        register_and_login_user(self.client).data['token']
        self.assertEqual(Token.objects.count(), 1)
        response = self.client.post(self.url, format='json')
        self.assertEqual(Token.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "logout successful")

    def test_logout_user_not_logged_in(self):
        self.assertEqual(Token.objects.all().count(), 0)
        response = self.client.post(self.url, format='json')
        self.assertEqual(Token.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], "you weren't logged in")
