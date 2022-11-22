from django.urls import reverse

from flashcards.models import Language


def create_language_and_add_for_user(language_code,
                                     language_name, language_pk, client):
    Language.objects.create(code=language_code, name=language_name)
    client.post(reverse('add_language', kwargs={'pk': language_pk}),
                format='json')
