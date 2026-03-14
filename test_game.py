from game import Game
from grid import Grid
from player import Player
from rules import Rules


class TestGame:
    def test_has_two_players(self):
        game = Game(Player("Alice"), Player("Bob"))
        assert game.player1.name == "Alice"
        assert game.player2.name == "Bob"

    def test_has_grid(self):
        game = Game(Player("Alice"), Player("Bob"))
        assert isinstance(game.grid, Grid)

    def test_has_rules(self):
        game = Game(Player("Alice"), Player("Bob"))
        assert isinstance(game.rules, Rules)
