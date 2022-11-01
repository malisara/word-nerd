from django.core.management.base import BaseCommand
from flashcards.models import Language
import csv


class Command(BaseCommand):
    # Call command:  python3 manage.py fill_database_with_languages
    def handle(self, *args, **options):
        Language.objects.all().delete()
        with open('flashcards/languages.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                Language.objects.create(code=row[0], name=row[1])
