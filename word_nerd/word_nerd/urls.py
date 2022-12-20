"""word_nerd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.authtoken import views as api_views

from flashcards import views as flashcards_views
from users import views as user_views
from decks import views as deck_views

urlpatterns = [
    path('register/', user_views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', api_views.obtain_auth_token, name='login'),
    path('logout/', user_views.LogoutUserAPIView().as_view(), name='logout'),

    path('all-languages/', flashcards_views.AllLanguagesAPIView().as_view(),
         name='all_languages'),
    path('my-languages/add/<int:pk>/', flashcards_views.AddLanguageAPIView.as_view(),
         name='add_language'),
    path('my-languages/', flashcards_views.GetUserLanguagesAPIView.as_view(),
         name='my_languages'),

    path('new-deck/', deck_views.NewDeckAPIView.as_view(), name='new_deck'),
    path('my-languages/<int:language_pk>/decks',
         deck_views.GetUserDecksAPIView.as_view(), name='my_decks'),
    path('decks/<int:pk>/edit', deck_views.EditDeckAPIView.as_view(),
         name='edit_deck'),
]
