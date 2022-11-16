from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.tests.utils_test import register_and_login_user
from .utils_test import create_language_and_add_for_user


class AddNewLanguage(APITestCase):
    url = reverse('my_languages')

    def test_user_has_no_languages(self):
        register_and_login_user(self.client)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'], [])

    def test_user_has_one_language(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'][0]['name'], 'english')
        self.assertEqual(response.data['languages'][0]['id'], 1)
        self.assertEqual(len(response.data['languages']), 1)

    def test_user_has_two_languages(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        create_language_and_add_for_user('fin', 'finnish', 2, self.client)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'][0]['name'], 'english')
        self.assertEqual(response.data['languages'][0]['id'], 1)
        self.assertEqual(response.data['languages'][1]['name'], 'finnish')
        self.assertEqual(response.data['languages'][1]['id'], 2)
        self.assertEqual(len(response.data['languages']), 2)
