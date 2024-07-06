from django.db import models

# Create your models here.

class HangmanGames(models.Model):
    '''
    Class to store the most important things
    about the Hangman game that a user will play.
    '''
    level = models.CharField(max_length=6)
    word = models.CharField(max_length=45)
    guesses_allowed = models.IntegerField(default=0)
    guesses_taken = models.IntegerField(default=0)

class HangmanGuesses(models.Model):
    '''
    Class to store all the guesses a user makes
    when playing the game.
    '''
    # foreign_key is usually the id of the HangmanGames
    # object of the word that the user is trying to guess
    foreign_key = models.IntegerField(null=False)
    guess = models.CharField(max_length=45)

class TTTMoves(model.Model):
    '''
    TODO: Create a model that stores:
    The game state in the form of a string XXOOXOX
    The outcome (W, D or L) for win, draw or lose respectively
    It needs a game id, but I think that's already a given
    '''
    pass
