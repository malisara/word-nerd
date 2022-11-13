from django.contrib.auth.models import User
from django.db import models

from flashcards.models import Language


class Deck(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    name = models.CharField(max_length=40, default='Other cards')
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
