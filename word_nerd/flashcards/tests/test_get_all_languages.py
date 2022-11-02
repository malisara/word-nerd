from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from flashcards.models import Language
from users.tests.utils_test import register_and_login_user


class GetAllLanguages(APITestCase):

    def test_return_all_languages(self):
        Language.objects.create(code='eng', name='english')
        register_and_login_user(self.client)
        response = self.client.get(reverse('all_languages'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'english')
        Language.objects.create(code='nor', name='norwegian')
        response = self.client.get(reverse('all_languages'), format='json')
        self.assertEqual(len(response.data), 2)
