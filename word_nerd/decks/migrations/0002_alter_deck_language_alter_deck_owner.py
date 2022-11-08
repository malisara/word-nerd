# Generated by Django 4.1.1 on 2022-11-03 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0003_rename_user_language_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='flashcards.language'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deck',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
