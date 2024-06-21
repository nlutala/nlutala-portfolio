from django.db import models

# Create your models here.

class HangmanGames(models.Model):
    RESULT = {
        "W": "Won",
        "L": "Lost"
    }
    level = models.CharField(max_length=6)
    word = models.CharField(max_length=45)
    number_of_guesses = models.IntegerField()
    number_of_guesses_taken = models.IntegerField()
    date_played = models.CharField()
    result = models.CharField(choices=RESULT)
