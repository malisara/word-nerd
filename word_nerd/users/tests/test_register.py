from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .utils_test import register_user


class RegisterTest(APITestCase):

    def test_register_user(self):
        response = register_user(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser1')
        self.assertNotEqual(User.objects.get().password, 'coolpassyow1')

    def test_passwords_dont_match(self):
        response = register_user(
            self.client, 'testuser1', 'coolpassyow1', 'coolpassyow')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            response.data['non_field_errors'][0], "Passwords don't match")

    def test_empty_password(self):
        response = register_user(self.client, 'testuser1', '', '')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['password'][0],
                         "This field may not be blank.")

    def test_weak_password(self):
        response = register_user(
            self.client, 'testuser1', 'password', 'password')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['password'][0],
                         'This password is too common.')
