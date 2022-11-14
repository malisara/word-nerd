from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from decks.models import Deck
from flashcards.models import Language
from users.tests.utils_test import register_and_login_user
from .utils_test import logged_user_adds_a_language


class AddNewLanguage(APITestCase):
    url = reverse('my_languages')

    def test_user_has_no_languages(self):
        register_and_login_user(self.client)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'], [])

    def test_user_has_one_language(self):
        logged_user_adds_a_language(self.client, 1, 'eng', 'english')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'][0]['name'], 'english')
        self.assertEqual(response.data['languages'][0]['id'], 1)
        self.assertEqual(len(response.data['languages']), 1)

    def test_user_has_two_language(self):
        logged_user_adds_a_language(self.client, 1, 'eng', 'english')
        logged_user_adds_a_language(self.client, 2, 'fin', 'finnish')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['languages'][0]['name'], 'english')
        self.assertEqual(response.data['languages'][0]['id'], 1)
        self.assertEqual(response.data['languages'][1]['name'], 'finnish')
        self.assertEqual(response.data['languages'][1]['id'], 2)
        self.assertEqual(len(response.data['languages']), 2)
