# Generated by Django 4.1.1 on 2022-11-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_alter_deck_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='name',
            field=models.CharField(blank=True, default='Other cards', max_length=40),
        ),
    ]
