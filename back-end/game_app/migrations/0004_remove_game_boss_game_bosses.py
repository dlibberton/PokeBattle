# Generated by Django 5.0.4 on 2024-04-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0003_remove_boss_description_boss_attack_boss_defense_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='boss',
        ),
        migrations.AddField(
            model_name='game',
            name='bosses',
            field=models.ManyToManyField(to='game_app.boss'),
        ),
    ]
