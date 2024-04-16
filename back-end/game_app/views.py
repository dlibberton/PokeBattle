import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pokemon, Modifier, Weather, Deck, Game, Boss, create_game_stats, GameStats
from .serializers import PokemonSerializer, ModifierSerializer, WeatherSerializer, BossSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import logging
from random import choice
from user_app.models import User

logger = logging.getLogger(__name__)


class ShopPageView(APIView):
    def get_random_location(self):
        # Generate random latitude and longitude
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        return latitude, longitude

    def get_weather(self, latitude, longitude):
        # Make a request to the weather API with random latitude and longitude
        api_key = "df2c312635c8474faf1202027241404"
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}'  
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
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get available Pokemon and Modifiers
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
            # Extract relevant weather information
            location = weather_data['location']['name']
            temperature = weather_data['current']['temp_c']
            humidity = weather_data['current']['humidity']
            weather_conditions = weather_data['current']['condition']['text']
            logger.info(f"Weather information fetched successfully: location={location}, temperature={temperature}, humidity={humidity}, conditions={weather_conditions}")

            # Create Weather object
            weather = Weather.objects.create(
                location=location,
                temperature=temperature,
                humidity=humidity,
                weather_conditions=weather_conditions
            )
            logger.info("Weather object created successfully.")
            # Create Game object and associate with user
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

            # Create GameStats for the lost game
            create_game_stats(game)

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
                "modifiers": [modifier.id for modifier in game_stats.modifiers.all()],
                "weather_id": game_stats.weather_id,
                "boss_name": game_stats.boss_name
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
            # Retrieve the user
            user = request.user

            # Retrieve the user's deck and associated modifiers
            users_deck = user.deck
            modifiers = users_deck.modifiers.all()

            # Retrieve the game associated with the user
            game = user.game

            # Retrieve all bosses for the game
            bosses = [game.boss1, game.boss2, game.boss3]

            # Choose a random boss from the available bosses
            random_boss = choice(bosses)

            # Retrieve the weather for the game
            weather = game.weather

            # Return the data
            data = {
                "users_deck_id": users_deck.id,
                "modifiers": [modifier.id for modifier in modifiers],
                "random_boss_name": random_boss.name,
                "weather_id": weather.id
            }

            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({"error": "User's deck or game not found."}, status=status.HTTP_404_NOT_FOUND)