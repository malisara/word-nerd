from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.tests.utils_test import register_and_login_user
from flashcards.models import Language


class GetAllLanguages(APITestCase):

    def test_return_all_language(self):
        Language.objects.create(code='eng', language='english')
        register_and_login_user(self.client)
        response = self.client.get(reverse('all_languages'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['language'], 'english')
        Language.objects.create(code='nor', language='norwegian')
        response = self.client.get(reverse('all_languages'), format='json')
        self.assertEqual(len(response.data), 2)
