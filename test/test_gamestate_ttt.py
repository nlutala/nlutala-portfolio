'''
Test the functionality of the GameState class

Nathan Lutala (nlutala)
'''
from website.projects.gamestate_ttt import GameState
from website.projects.ml_cpu_ttt import MLCPU
from secrets import choice
from django.test import TestCase

class TestGameState(TestCase):
    def test_gamestate_raises_value_error_if_player_tries_to_put_symbol_on_taken_place(self):
        gs = GameState()

        # Let the Naive CPU put an item in place first
        cpu = MLCPU()
        index = cpu.make_move(gs.get_game_state(), gs.get_available_positions())
        gs.set_game_state(index, cpu.get_symbol())

        # Let the human (myself) put an item in the same place the CPU did
        with self.assertRaises(ValueError):
            gs.set_game_state(index, "O")

        # Let the Naive CPU put an item in the same place again
        with self.assertRaises(ValueError):
            gs.set_game_state(index, cpu.get_symbol())

    def test_gamestate_is_done_method_after_two_moves(self):
        gs = GameState()

        # Let the Naive CPU put an item in place first
        cpu = MLCPU()
        index = cpu.make_move(gs.get_game_state(), gs.get_available_positions())
        gs.set_game_state(index, cpu.get_symbol())

        # Let the human (myself) put an item in the same place the CPU did
        free_spaces = gs.get_available_positions()
        gs.set_game_state(choice(free_spaces), "O")

        assert gs.is_done() == False
        assert gs.outcome == ""
