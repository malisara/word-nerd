from django.contrib.auth.models import User
import django.contrib.auth.password_validation as django_validators
from django.core import exceptions as django_exceptions
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        password = data['password']
        confirmed_password = data.pop('password2')

        if password != confirmed_password:
            raise serializers.ValidationError("Passwords don't match")
        try:
            # validate the password and catch errors
            django_validators.validate_password(
                password=password, user=User(data['username'], data['password']))
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return data

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
