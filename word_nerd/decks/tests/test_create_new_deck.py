from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from decks.models import Deck
from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user


class AddNewLanguage(APITestCase):
    url = reverse('new_deck')

    def test_invalid_serializer_wrong_language_pk(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language_id": 2, "name": "  "}
        # First deck is created when the language is chosen
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data")
        self.assertEqual(response.data["errors"]["language_id"][0],
                         "Language does not exist")

    def test_invalid_serializer_no_deck_name(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language_id": 1, "name": ""}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data")
        self.assertEqual(response.data["errors"]["name"][0],
                         "This field may not be blank.")

    def test_invalid_serializer_only_spaces_in_name(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language_id": 1, "name": "  "}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid data")
        self.assertEqual(response.data["errors"]["name"][0],
                         "This field may not be blank.")

    def test_successfully_create_new_deck(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language_id": 1, "name": "Awesome deck!", "public": True}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "New deck created.")
        deck = Deck.objects.get(id=2)
        self.assertEqual(deck.public, True)
        self.assertEqual(deck.language.id, 1)
        self.assertEqual(deck.name, "Awesome deck!")
        self.assertEqual(deck.owner.id, 1)

    def test_create_new_deck_default_public_attribute(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        data = {"language_id": 1, "name": "Awesome deck!"}
        self.assertEqual(Deck.objects.count(), 1)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Deck.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "New deck created.")
        deck = Deck.objects.get(id=2)
        self.assertEqual(deck.public, False)
        self.assertEqual(deck.language.id, 1)
        self.assertEqual(deck.name, "Awesome deck!")
        self.assertEqual(deck.owner.id, 1)
