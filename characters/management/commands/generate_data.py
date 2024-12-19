from django.core.management.base import BaseCommand
from faker import Faker
from characters.models import Character

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(10):
            Character.objects.create(
                name=fake.name()
            )
