from django.contrib.auth.models import User
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=2)
    users = models.ManyToManyField(User, related_name='languages')
