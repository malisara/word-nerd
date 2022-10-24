from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .utils_test import register_user, register_and_login_user


class LoginTest(APITestCase):

    def test_login_user(self):
        self.assertEqual(Token.objects.count(), 0)
        response = register_and_login_user(self.client)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data['token']), 0)

    def test_login_wrong_data(self):
        register_user(self.client)
        self.assertEqual(Token.objects.count(), 0)
        data = {'username': 'testuser2', 'password': 'coolpassyow2'}
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(Token.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0],
                         'Unable to log in with provided credentials.')

    def test_login_get_request(self):
        register_user(self.client)
        data = {'username': 'testuser1', 'coolpassyow1': 'coolpassyow1'}
        response = self.client.get(reverse('login'), data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    def test_login_blank_fields(self):
        data = {'username': '', 'password': ''}
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0],
                         'This field may not be blank.')
        self.assertEqual(response.data['password'][0],
                         'This field may not be blank.')

    # TODO test valid token
