# Generated by Django 5.0.6 on 2024-07-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_hangmangames_guesses_allowed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TTTMoves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_state', models.CharField(max_length=9)),
                ('outcome', models.CharField(max_length=1)),
                ('player_turn', models.CharField(max_length=1)),
            ],
        ),
    ]
