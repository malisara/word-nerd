from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from decks.models import Deck
from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user


class UpdateDeck(APITestCase):
    url = reverse('edit_deck', kwargs={'pk': 1})
    data = {'name': 'newname', 'public': True}

    def test_update_deck_404_wrong_deck_pk(self):
        register_and_login_user(self.client)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_deck_404_user_is_not_author(self):
        client = APIClient()
        register_and_login_user(client, username='wronguser')
        create_language_and_add_for_user('eng', 'english', 1, client)
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(Deck.objects.get(id=1).owner.username, 'wronguser')

        register_and_login_user(self.client)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_deck_without_deck_name(self):
        _register_user_with_a_language(self.client)
        data = {'public': True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, 'Other cards')  # Default deck name
        self.assertTrue(deck.public)
        self.assertEqual(deck.owner.username, 'testuser1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Deck is updated.')

    def test_update_deck_without_public(self):
        _register_user_with_a_language(self.client)
        data = {'name': 'Not like other cards'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, 'Not like other cards')
        self.assertFalse(deck.public)  # Default value
        self.assertEqual(deck.owner.username, 'testuser1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Deck is updated.')

    def test_update_deck(self):
        _register_user_with_a_language(self.client)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        deck = Deck.objects.get(id=1)
        self.assertEqual(deck.name, 'newname')
        self.assertTrue(deck.public)
        self.assertEqual(response.data['detail'], 'Deck is updated.')


def _register_user_with_a_language(client):
    # New deck is automatically created after user adds a new language
    # Deck attributes: deck.name = 'Other cards', deck.public = False
    register_and_login_user(client)
    create_language_and_add_for_user('eng', 'english', 1, client)
