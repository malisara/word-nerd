from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from decks.models import Language
from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user


class AddNewLanguage(APITestCase):
    url = reverse('my_decks', kwargs={'language_pk': 1})

    def test_wrong_pk_language_doesnt_exist(self):
        register_and_login_user(self.client)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Language is not selected.")

    def test_wrong_pk_language_exists_but_not_selected(self):
        register_and_login_user(self.client)
        Language.objects.create(code='eng', name='english')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Language is not selected.")

    def test_return_users_decks(self):
        register_and_login_user(self.client)
        create_language_and_add_for_user('eng', 'english', 1, self.client)
        _create_new_deck(self.client, 1, 'TestDeck')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['decks']), 2)
        deck = response.data['decks'][1]  # 1st deck is created automatically
        self.assertEqual(deck['name'], 'TestDeck')
        self.assertFalse(deck['public'], False)


def _create_new_deck(client, language_pk, deck_name):
    data = {'language': language_pk, 'name': deck_name}
    client.post(reverse('new_deck'), data, format='json')
