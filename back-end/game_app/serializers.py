from rest_framework import serializers
from .models import Pokemon, Modifier, Deck, Boss, Weather, Game, GameStats

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'

class ModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifier
        fields = '__all__'

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = '__all__'

class BossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boss
        fields = '__all__'

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameStats
        fields = '__all__'