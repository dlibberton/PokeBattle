from django.core.management.base import BaseCommand
from game_app.models import Modifier

class Command(BaseCommand):
    help = 'Generate sample data for Modifier model'

    def handle(self, *args, **kwargs):
        modifiers_data = [
            {"name": "Green Thumb", "description": "All grass pokemon in your deck gain 20 health and 20 defense"},
            {"name": "Spring has Sprung", "description": "Evolve a grass pokemon in your deck"},
            {"name": "Typhoon", "description": "All water pokemon in your deck gain 40 defense"},
            {"name": "Fountain of knowledge", "description": "Evolve a water pokemon in your deck"},
            {"name": "Firestorm", "description": "All fire pokemon in your deck gain 40 attack"},
            {"name": "Avatar", "description": "Evolve all pokemon in your deck if they are unique types"},
            {"name": "Forest Fire", "description": "Evolve all grass and fire pokemon"},
            {"name": "Steam Powered", "description": "Evolve all water and fire pokemon"},
            {"name": "Oasis", "description": "Evolve all grass and water pokemon"},
        ]

        for data in modifiers_data:
            modifier = Modifier.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created modifier: {modifier.name}'))