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
    modifier = models.OneToOneField(Modifier, on_delete=models.CASCADE)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)
    boss_name = models.CharField(max_length=100)
    
@receiver(post_save, sender=Game)
def create_game_stats(sender, instance, created, **kwargs):
    if not created and instance.winner == False:
        # If winner is False, create a GameStats object

        # Get the user's deck
        user_deck = instance.user.deck

        # Get all modifiers associated with the user's deck
        deck_modifiers = user_deck.modifiers.all()

        # Get the last boss associated with the game
        last_boss = instance.boss

        # Create GameStats object and associate modifiers
        game_stats = GameStats.objects.create(
            game=instance,
            users_deck=user_deck,
            weather=instance.weather,
            boss_name=last_boss.name
        )
        
        # Add all modifiers associated with the user's deck to GameStats
        game_stats.modifiers.add(*deck_modifiers)

        game_stats.save()