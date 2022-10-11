from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTest(APITestCase):
    url = reverse('register')

    def test_register_user(self):
        data = {'username': 'testuser1',
                'password': 'testnogeslo1', 'password2': 'testnogeslo1'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser1')
        self.assertNotEqual(User.objects.get().password, 'testnogeslo1')

    def test_passwords_dont_match(self):
        data = {'username': 'testuser1',
                'password': 'testnogeslo1', 'password2': 'geslotestno1'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            response.data['non_field_errors'][0], "Passwords don't match")

    def test_empty_password(self):
        data = {'username': 'testuser1',
                'password': 'testnogeslo1', 'password2': ''}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_weak_password(self):
        data = {'username': 'testuser1',
                'password': 'password', 'password2': 'password'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['password']
                         [0], 'This password is too common.')
