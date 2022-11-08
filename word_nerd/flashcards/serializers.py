from rest_framework import serializers

from .models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class LanguageIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, data):
        if Language.objects.filter(id=data).count() == 0:
            raise serializers.ValidationError(
                'Language instance does not exist.')
        return data
