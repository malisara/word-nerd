from django.urls import reverse

from flashcards.models import Language
from users.tests.utils_test import register_and_login_user


def logged_user_adds_a_language(client, url_pk, lamguage_code, language_name):
    Language.objects.create(code=lamguage_code, name=language_name)
    register_and_login_user(client)
    client.post(reverse('add_language', kwargs={'pk': url_pk}), format='json')
