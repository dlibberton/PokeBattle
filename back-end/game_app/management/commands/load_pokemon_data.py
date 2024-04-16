from django.core.management.base import BaseCommand
from game_app.data_loader import fetch_and_load_pokemon_data_by_id

class Command(BaseCommand):
    help = 'Fetch and load Pokemon data into the database'

    def handle(self, *args, **kwargs):
        pokemon_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 152, 153, 154, 155, 156, 157, 158, 159, 160, 252, 253, 254, 255, 256, 257, 258, 259, 260]  # Example: Pokemon IDs to fetch and load
        fetch_and_load_pokemon_data_by_id(pokemon_ids)