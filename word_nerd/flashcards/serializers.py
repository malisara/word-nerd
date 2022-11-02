from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class MyLanguageSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField()

    class Meta:
        model = Language
        fields = ['language_id']

    def validate_language_id(self, data):
        try:
            Language.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Language instance does not exist.')
        return data
