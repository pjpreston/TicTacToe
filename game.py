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
        self._current_player = player1

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

    @property
    def current_player(self) -> Player:
        return self._current_player

    def get_player_by_name(self, name: str) -> Player:
        """Return the player with the given name, or raise ValueError."""
        if name == self._player1.name:
            return self._player1
        if name == self._player2.name:
            return self._player2
        raise ValueError(f"No player named '{name}'")

    def make_move(self, player: Player, row: int, col: int, value: str) -> None:
        """Place a value on the grid for the given player, enforcing turn order."""
        if player is not self._current_player:
            raise ValueError(f"It is not {player.name}'s turn")
        self._grid.set(row, col, value)
        self._current_player = self._player2 if player is self._player1 else self._player1
