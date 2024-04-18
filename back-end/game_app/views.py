import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pokemon, Modifier, Weather, Deck, Game, Boss, handle_game_result, GameStats
from .serializers import PokemonSerializer, ModifierSerializer, WeatherSerializer, BossSerializer, DeckSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import logging
from random import choice
from user_app.models import User
from django.db import transaction
from pokebattle_proj.settings import env

logger = logging.getLogger(__name__)

class ShopPageView(APIView):
    def get_random_location(self):
        # Generate random latitude and longitude
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        return latitude, longitude

    def get_weather(self, latitude, longitude):
        # Make a request to the weather API with random latitude and longitude
        url = f'http://api.weatherapi.com/v1/current.json?key={env.get("api_key")}&q={latitude},{longitude}'  
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_random_bosses(self):
        # Get all boss instances as a list
        all_bosses = list(Boss.objects.all())
        # Shuffle the list of bosses
        random.shuffle(all_bosses)
        return all_bosses[:3]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get existing game for the user if it exists
        try:
            game = Game.objects.get(user=request.user)
            game.delete()  # Delete the existing game
            user_deck = game.user.deck
            user_deck.delete()
        except Game.DoesNotExist:
            pass  # No existing game, proceed to create a new one

        available_pokemon = Pokemon.objects.all()
        available_modifiers = Modifier.objects.all()

        # Serialize available Pokemon and Modifiers
        pokemon_serializer = PokemonSerializer(available_pokemon, many=True)
        modifier_serializer = ModifierSerializer(available_modifiers, many=True)

        # Generate random location
        latitude, longitude = self.get_random_location()
        logger.info(f"Generated random location: latitude={latitude}, longitude={longitude}")

        # Fetch weather information for the random location
        weather_data = self.get_weather(latitude, longitude)

        if weather_data is not None:
            location = weather_data['location']['name']
            temperature = weather_data['current']['temp_c']
            humidity = weather_data['current']['humidity']
            weather_conditions = weather_data['current']['condition']['text']
            logger.info(f"Weather information fetched successfully: location={location}, temperature={temperature}, humidity={humidity}, conditions={weather_conditions}")

            weather = Weather.objects.create(
                location=location,
                temperature=temperature,
                humidity=humidity,
                weather_conditions=weather_conditions
            )
            logger.info("Weather object created successfully.")

            # Get random boss instances
            random_bosses = self.get_random_bosses()

            # Serialize random boss instances
            boss_serializer = BossSerializer(random_bosses, many=True)

            # Create Game object and associate with user and bosses
            game = Game.objects.create(
                user=request.user,
                weather=weather
            )
            game.bosses.add(*random_bosses)
            game.save()
            logger.info("Game object created successfully.")

            # Create JSON response
            data = {
                "user_id": request.user.id,
                "email": request.user.email,
                "available_pokemon": pokemon_serializer.data,
                "available_modifiers": modifier_serializer.data,
                "weather": WeatherSerializer(weather).data,
                "bosses": boss_serializer.data
            }
            logger.info("Response data created successfully.")

            return Response(data)
        else:
            logger.error("Failed to fetch weather information.")
            return Response({"error": "Failed to fetch weather information."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        data = request.data
        
        # Check if the request contains the necessary data for adding a Pokemon to the deck
        if 'pokemon_id' in data:
            return self.add_pokemon_to_deck(data)
        
        # Check if the request contains the necessary data for adding a Modifier to the deck
        elif 'user_id' in data and 'deck_id' in data and 'modifier_id' in data:
            return self.add_modifier_to_deck(data)
        
        # Check if the request contains the necessary data for handling loss
        elif 'game_id' in data:
            return self.handle_loss(data)
        
        # If none of the expected data is found, return an error response
        else:
            return JsonResponse({'error': 'Invalid request data'}, status=400)
    
    def add_pokemon_to_deck(self, data):
        try:
            # Parse the JSON data
            pokemon_id = data['pokemon_id']
            user_id = data['user_id']
            deck_id = data['deck_id']

            # Check if the user has a deck, create one if not
            try:
                deck = Deck.objects.get(user__id=user_id)
            except Deck.DoesNotExist:
                deck = Deck.objects.create(user_id=user_id, name='Default Deck')

            # Retrieve the Pokemon object
            pokemon = Pokemon.objects.get(id=pokemon_id)

            # Add the Pokemon to the deck
            deck.pokemons.add(pokemon)

            return JsonResponse({'message': 'Pokemon added to deck successfully'}, status=200)

        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
        except Pokemon.DoesNotExist:
            return JsonResponse({'error': 'Pokemon not found'}, status=404)

    def add_modifier_to_deck(self, data):
        try:
            # Parse the JSON data
            user_id = data['user_id']
            deck_id = data['deck_id']
            modifier_id = data['modifier_id']

            # Retrieve the user's deck
            deck = Deck.objects.get(id=deck_id, user__id=user_id)

            # Retrieve the Modifier object
            modifier = Modifier.objects.get(id=modifier_id)

            # Add the Modifier to the deck
            deck.modifiers.add(modifier)

            return JsonResponse({'message': 'Modifier added to deck successfully'}, status=200)

        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
        except Deck.DoesNotExist:
            return JsonResponse({'error': 'Deck not found'}, status=404)
        except Modifier.DoesNotExist:
            return JsonResponse({'error': 'Modifier not found'}, status=404)


    def handle_loss(self, data):
        try:
            # Parse the JSON data
            game_id = data['game_id']

            # Retrieve the game instance
            game = Game.objects.get(id=game_id)

            # Update the winner field to False
            game.winner = False
            game.save()

            # Retrieve the user's deck
            user_deck = game.user.deck

            # Handle the game result to create GameStats
            with transaction.atomic(): 
                handle_game_result(game, user_deck)

            return JsonResponse({'message': 'Game lost, GameStats created'}, status=200)

        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        
            
class StatsPageView(APIView):
    def get(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Retrieve the user's GameStats object
            game_stats = GameStats.objects.get(game__user=request.user)

            # Serialize the GameStats object
            game_stats_data = {
                "game_id": game_stats.game_id,
                "users_deck_id": game_stats.users_deck_id,
                "boss_name": game_stats.boss_name,
                "modifiers": [modifier.id for modifier in game_stats.modifiers.all()],
                "pokemons": [pokemon.id for pokemon in game_stats.pokemons.all()],
                "weather": {
                    "location": game_stats.weather.location,
                    "temperature": game_stats.weather.temperature,
                    "humidity": game_stats.weather.humidity,
                    "weather_conditions": game_stats.weather.weather_conditions
                }
            }

            return Response(game_stats_data, status=status.HTTP_200_OK)

        except GameStats.DoesNotExist:
            return Response({"error": "GameStats not found for the user."}, status=status.HTTP_404_NOT_FOUND)
        
class BattlePageView(APIView):
    def get(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Retrieve the user's game if it exists
            game = Game.objects.get(user=request.user)
            user_deck = game.user.deck

            # Retrieve all Pokemon and modifiers in the user's deck
            user_pokemon = user_deck.pokemons.all()
            user_modifier = user_deck.modifiers.all()

            # Serialize the user's deck, pokemons, and modifiers
            deck_serializer = DeckSerializer(user_deck)
            pokemon_serializer = PokemonSerializer(user_pokemon, many=True)
            modifier_serializer = ModifierSerializer(user_modifier, many=True)

            # Serialize the weather attached to the game model
            weather_serializer = WeatherSerializer(game.weather)

            # Serialize the bosses attached to the game model
            boss_serializer = BossSerializer(game.bosses.all(), many=True)

            # Create JSON response
            data = {
                "user_deck": deck_serializer.data,
                "user_pokemon": pokemon_serializer.data,
                "user_modifier": modifier_serializer.data,
                "weather": weather_serializer.data,
                "bosses": boss_serializer.data
            }

            return Response(data)
        except Game.DoesNotExist:
            return Response({"error": "No active game found."}, status=status.HTTP_404_NOT_FOUND)