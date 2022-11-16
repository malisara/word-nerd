from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from flashcards.models import Language
from .models import Deck


class NewDeckSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField()

    class Meta:
        model = Deck
        fields = ['language_id', 'name', 'public']

    def validate_language_id(self, data):
        try:
            Language.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Language does not exist')
        return data
