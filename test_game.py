import pytest
from game import Game
from grid import Grid
from player import Player
from rules import Rules


class TestGame:
    def test_has_two_players(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert game.player1.name == "Alice"
        assert game.player2.name == "Bob"

    def test_has_grid(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert isinstance(game.grid, Grid)

    def test_has_rules(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert isinstance(game.rules, Rules)


class TestGetPlayerByName:
    def test_finds_player1(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert game.get_player_by_name("Alice") is game.player1

    def test_finds_player2(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert game.get_player_by_name("Bob") is game.player2

    def test_unknown_name_raises(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        with pytest.raises(ValueError, match="No player named"):
            game.get_player_by_name("Charlie")


class TestTurnManagement:
    def test_player1_goes_first(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        assert game.current_player is game.player1

    def test_turn_alternates_after_move(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        game.make_move(game.player1, 0, 0, "X")
        assert game.current_player is game.player2
        game.make_move(game.player2, 0, 1, "O")
        assert game.current_player is game.player1

    def test_wrong_player_cannot_move(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        with pytest.raises(ValueError, match="not.*turn"):
            game.make_move(game.player2, 0, 0, "O")

    def test_no_consecutive_moves(self):
        game = Game(Player("Alice", 1), Player("Bob", 2))
        game.make_move(game.player1, 0, 0, "X")
        with pytest.raises(ValueError, match="not.*turn"):
            game.make_move(game.player1, 1, 0, "X")
