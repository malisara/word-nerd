from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from decks.models import Deck
from flashcards.models import Language
from users.tests.utils_test import register_and_login_user


class AddNewLanguage(APITestCase):
    url = reverse('add_language')

    def test_wrong_language_pk(self):
        register_and_login_user(self.client)
        response = self.client.post(
            self.url, {"language_id": "1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.data['detail'], 'Invalid data.')
        self.assertEqual(response.data['errors']['language_id'][0],
                         'Language instance does not exist.')

    def test_user_already_has_language(self):
        Language.objects.create(code='eng', name='english')
        register_and_login_user(self.client)
        data = {"language_id": "1"}
        self.assertEqual(Deck.objects.count(), 0)
        self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'],
                         'Language is already chosen.')
        self.assertEqual(Deck.objects.count(), 1)

    def test_succesfully_add_new_language(self):
        Language.objects.create(code='eng', name='english')
        register_and_login_user(self.client)
        response = self.client.post(
            self.url, {"language_id": "1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'New language added.')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(Deck.objects.get(id=1).name, 'uncategorized cards')
        self.assertEqual(Deck.objects.get(id=1).owner.id, 1)
        self.assertEqual(Deck.objects.get(id=1).public, False)
        self.assertEqual(Deck.objects.get(id=1).language.id, 1)
