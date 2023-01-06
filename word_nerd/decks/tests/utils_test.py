from flashcards.tests.utils_test import create_language_and_add_for_user
from users.tests.utils_test import register_and_login_user


def register_user_with_a_language(client):
    # New deck is automatically created after user adds a new language
    # Deck attributes: deck.name = 'Other cards', deck.public = False
    register_and_login_user(client)
    create_language_and_add_for_user('eng', 'english', 1, client)
