import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # Получаем модели через lazy loading
        Content = apps.get_model('characters', 'Content')
        ContentType = apps.get_model('characters', 'ContentType')

        # Получаем все типы контента и пользователей из базы данных
        content_types = ContentType.objects.all()
        users = User.objects.all()  # If you want to associate content with users

        for _ in range(1000):  # Adjust the number of content instances as needed
            random_content_type = random.choice(content_types) if content_types else None
            random_user = random.choice(users) if users else None

            # Создание контента
            Content.objects.create(
                type=random_content_type,
                episode_name=fake.sentence(),
                episode=random.randint(1, 50),  # Random episode number
                volume=random.randint(1, 10),    # Random volume number
                description=fake.text(),
                picture=fake.image_url(),         # Generate a random image URL or use a placeholder
                user=random_user
            )

        self.stdout.write(self.style.SUCCESS('Successfully created fake content.'))
