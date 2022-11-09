from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from decks.models import Deck
from flashcards.models import Language
from users.tests.utils_test import register_and_login_user


class AddNewLanguage(APITestCase):
    url = reverse('add_language', kwargs={'pk': 1})

    def test_wrong_language_pk(self):
        register_and_login_user(self.client)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.data['detail'],
                         'Language instance does not exist.')

    def test_user_already_has_language(self):
        Language.objects.create(code='eng', name='english')
        register_and_login_user(self.client)
        self.assertEqual(Deck.objects.count(), 0)
        self.client.post(self.url, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'],
                         'Language is already selected.')
        self.assertEqual(Deck.objects.count(), 1)

    def test_succesfully_add_new_language(self):
        Language.objects.create(code='eng', name='english')
        register_and_login_user(self.client)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'New language added.')
        deck = Deck.objects.get(id=1)
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(deck.name, 'other cards')
        self.assertEqual(deck.owner.id, 1)
        self.assertEqual(deck.public, False)
        self.assertEqual(deck.language.id, 1)
