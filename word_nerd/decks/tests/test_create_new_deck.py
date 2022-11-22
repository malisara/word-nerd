from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from decks.models import Deck, Language
from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user


class AddNewLanguage(APITestCase):
    url = reverse('new_deck')

    def test_invalid_serializer_wrong_language_pk(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language": 2, "name": "WrongPK"}
        # First deck is created when the language is chosen
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data.")
        self.assertEqual(response.data['errors']['language'][0],
                         'Invalid pk "2" - object does not exist.')

    def test_invalid_seralizer_language_exists_but_not_selected(self):
        register_and_login_user(self.client)
        Language.objects.create(code='eng', name='english')
        data = {"language": 1, "name": "I want to create a deck"}
        self.assertEqual(Deck.objects.count(), 0)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid data.')
        self.assertEqual(response.data['errors']['language'][0],
                         'Invalid pk "1" - object does not exist.')

    def test_invalid_serializer_no_deck_name(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language": 1, "name": ""}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data.")
        self.assertEqual(response.data["errors"]["name"][0],
                         "This field may not be blank.")

    def test_invalid_serializer_only_spaces_in_name(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language": 1, "name": "  "}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data.")
        self.assertEqual(response.data["errors"]["name"][0],
                         "This field may not be blank.")

    def test_successfully_create_new_deck(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language": 1, "name": "Awesome deck!", "public": True}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "New deck created.")
        deck = Deck.objects.get(id=2)
        self.assertTrue(deck.public)
        self.assertEqual(deck.language.id, 1)
        self.assertEqual(deck.name, "Awesome deck!")
        self.assertEqual(deck.owner.id, 1)

    def test_create_new_deck_default_public_attribute(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language": 1, "name": "Awesome deck!"}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "New deck created.")
        deck = Deck.objects.get(id=2)
        self.assertFalse(deck.public)
        self.assertEqual(deck.language.id, 1)
        self.assertEqual(deck.name, "Awesome deck!")
        self.assertEqual(deck.owner.id, 1)
