from django.core.management.base import BaseCommand
from flashcards.models import Language
import csv


class Command(BaseCommand):
    # Call command:  python3 manage.py <file_name>
    def handle(self, *args, **options):
        with open('flashcards/languages.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    Language.objects.get(code=row[0])
                except Language.DoesNotExist:
                    Language.objects.create(code=row[0], language=row[1])
