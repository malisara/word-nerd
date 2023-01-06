from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from decks.models import Deck
from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user
from .utils_test import register_user_with_a_language


class DeleteDeck(APITestCase):
    url = reverse('delete_deck', kwargs={'pk': 1})

    def test_delete_deck_404_wrong_deck_pk(self):
        register_and_login_user(self.client)
        response = self.client.post(self.url, format='json')
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_deck_404_user_is_not_author(self):
        client = APIClient()
        register_and_login_user(client, username='wronguser')
        create_language_and_add_for_user('eng', 'english', 1, client)
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(Deck.objects.get(id=1).owner.username, 'wronguser')

        register_and_login_user(self.client)
        response = self.client.post(self.url, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successfully_delete_deck(self):
        register_user_with_a_language(self.client)
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, format='json')
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'],
                         "Deck 'Other cards' is deleted.")
