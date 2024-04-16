import requests
from game_app.models import Pokemon, Boss

def fetch_and_load_pokemon_data_by_id(pokemon_ids):
    for pokemon_id in pokemon_ids:
        # Fetch data from the PokeAPI for each Pokemon ID
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/')
        if response.status_code == 200:
            data = response.json()
            
            # Extract attack and defense stats
            attack = data.get('stats')[4].get('base_stat')  # Assuming attack is at index 4
            defense = data.get('stats')[3].get('base_stat')  # Assuming defense is at index 3
            types = data.get('types')
            if types:
                first_type = types[0].get('type').get('name')
            else:
                first_type = None
            
            # Create an instance of the Pokemon model and save it
            Pokemon.objects.create(
                name=data.get('name'),
                pokemon_id=pokemon_id,
                attack=attack,
                defense=defense,
                type=first_type
            )
            print(f"Pokemon {pokemon_id} data loaded successfully.")
        else:
            print(f"Failed to fetch Pokemon data for ID {pokemon_id} from the PokeAPI.")
            

def fetch_and_load_boss_data_by_id(pokemon_ids):
    for pokemon_id in pokemon_ids:
        # Fetch data from the PokeAPI for each Pokemon ID
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/')
        if response.status_code == 200:
            data = response.json()
            
            # Extract attack and defense stats
            attack = data.get('stats')[4].get('base_stat')  # Assuming attack is at index 4
            defense = data.get('stats')[3].get('base_stat')  # Assuming defense is at index 3
            types = data.get('types')
            if types:
                first_type = types[0].get('type').get('name')
            else:
                first_type = None
            
            # Create an instance of the Pokemon model and save it
            Boss.objects.create(
                name=data.get('name'),
                pokemon_id=pokemon_id,
                attack=attack,
                defense=defense,
                type=first_type
            )
            print(f"Boss {pokemon_id} data loaded successfully.")
        else:
            print(f"Failed to fetch Boss data for ID {pokemon_id} from the PokeAPI.")