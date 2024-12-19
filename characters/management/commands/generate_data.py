import random
from faker import Faker
from django.core.management.base import BaseCommand
from characters.models import Character, Team, Position, Skills
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # Получаем все команды, позиции и навыки из базы данных
        teams = Team.objects.all()
        positions = Position.objects.all()
        skills = Skills.objects.all()
        users = User.objects.all()  # If you want to associate characters with users

        for _ in range(1000):  # Adjust the number of characters as needed
            random_team = random.choice(teams) if teams else None
            random_position = random.choice(positions) if positions else None
            random_skill = random.choice(skills) if skills else None
            random_user = random.choice(users) if users else None

            # Создание персонажа
            Character.objects.create(
                name=fake.name(),
                team=random_team,
                position=random_position,
                skill=random_skill,
                picture=fake.image_url(),  # Generate a random image URL or use a placeholder
                user=random_user
            )

        self.stdout.write(self.style.SUCCESS('Successfully created fake characters.'))
