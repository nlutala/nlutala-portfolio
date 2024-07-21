'''
Test the functionality of the MLCPU class

Nathan Lutala (nlutala)
'''
from django.test import TestCase
from website.projects.ml_cpu_ttt import MLCPU
from website.projects.gamestate_ttt import GameState

class TestMLCPU(TestCase):
    def test_make_move_returns_index_that_is_not_already_taken(self):
        gs = GameState()
        ml_cpu_1 = MLCPU("O")
        ml_cpu_2 = MLCPU("X")

        gs.set_game_state(
            ml_cpu_1.make_move(gs.get_game_state(), gs.get_available_positions()), 
            ml_cpu_1.get_symbol()
        )

        game_state = gs.get_game_state()
        available_positions = gs.get_available_positions()

        assert game_state[ml_cpu_2.make_move(game_state, available_positions)] == "_"
