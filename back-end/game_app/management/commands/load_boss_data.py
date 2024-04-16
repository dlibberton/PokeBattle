from django.core.management.base import BaseCommand
from game_app.data_loader import fetch_and_load_boss_data_by_id

class Command(BaseCommand):
    help = 'Fetch and load Pokemon data into the database'

    def handle(self, *args, **kwargs):
        pokemon_ids = [150, 487, 144, 145, 146, 384]  # Example: Pokemon IDs to fetch and load boss legendaries
        fetch_and_load_boss_data_by_id(pokemon_ids)