# Generated by Django 4.1.1 on 2022-11-02 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_rename_language_language_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='user',
            new_name='users',
        ),
    ]
