from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    pokemon_id = models.IntegerField(unique=True)
    attack = models.IntegerField()
    defense = models.IntegerField()
    type = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.name

class Modifier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Deck(models.Model):
    user = models.OneToOneField("user_app.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    pokemons = models.ManyToManyField(Pokemon, related_name='decks')
    modifiers = models.ManyToManyField(Modifier, related_name='decks')


class Boss(models.Model):
    name = models.CharField(max_length=100)
    pokemon_id = models.IntegerField(unique=True, default=1)
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=1)
    type = models.CharField(max_length=30, default='')
    
    def __str__(self):
        return self.name

class Weather(models.Model):
    location = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    weather_conditions = models.CharField(max_length=100)
    
class Game(models.Model):
    user = models.OneToOneField("user_app.User", on_delete=models.CASCADE)
    bosses = models.ManyToManyField(Boss)
    
    weather = models.ForeignKey(Weather, on_delete=models.SET_NULL, blank=True, null=True)
    winner = models.BooleanField(default=True)
    
class GameStats(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    users_deck = models.OneToOneField(Deck, on_delete=models.CASCADE)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)
    boss_name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon, related_name='game_stats', blank=True)
    modifiers = models.ManyToManyField(Modifier, related_name='game_stats', blank=True)
    
    def add_pokemon(self, pokemon):
        self.pokemons.add(pokemon)
        
    
def handle_game_result(game, user_deck):
        # Get the last boss associated with the game
        last_boss = game.bosses.last()

        # Create GameStats object
        game_stats = GameStats.objects.create(
            game=game,
            users_deck=user_deck,
            weather=game.weather,
            boss_name=last_boss.name
        )

            # Retrieve all pokemons associated with the user's deck
        user_pokemons = user_deck.pokemons.all()
        print(user_pokemons)
        #game_stats.pokemons.add(*user_pokemons)
        #print("added pokemon", game_stats.pokemons.all())
        #print(game_stats.pokemons.all())
        for pokemon in user_pokemons:
           game_stats.add_pokemon(pokemon)

        # Retrieve all modifiers associated with the user's deck
        user_modifiers = user_deck.modifiers.all()
        for modifier in user_modifiers:
            game_stats.modifiers.add(modifier)
            game_stats.save()

