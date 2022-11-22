from rest_framework import serializers

from .models import Deck


class UserLanguagesPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return self.context['request'].user.languages


class NewDeckSerializer(serializers.ModelSerializer):
    language = UserLanguagesPrimaryKeyRelatedField()

    class Meta:
        model = Deck
        fields = ['language', 'name', 'public']


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['name', 'public']
