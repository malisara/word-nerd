from django.contrib.auth.models import User
import django.contrib.auth.password_validation as django_validators
from django.core import exceptions
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        password = data['password']
        confirmed_password = data.pop('password2')

        errors = {}
        if password != confirmed_password:
            raise serializers.ValidationError(f"Passwords don't match")
        try:
            # validate the password and catch errors
            django_validators.validate_password(
                password=password, user=User(data['username'], data['password']))
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'])
            return user
        except Exception as e:
            return e
