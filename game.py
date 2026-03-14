from grid import Grid
from player import Player
from rules import Rules


class Game:
    """Represents a TicTacToe game with two players and a grid."""

    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._grid = Grid()
        self._rules = Rules()

    @property
    def player1(self) -> Player:
        return self._player1

    @property
    def player2(self) -> Player:
        return self._player2

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def rules(self) -> Rules:
        return self._rules
