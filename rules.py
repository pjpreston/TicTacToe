from grid import Grid


class Rules:
    """Encapsulates the win/draw rules for Tic-Tac-Toe."""

    _LINES = [
        # rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def winner(self, grid: Grid) -> str | None:
        """Return 'X' or 'O' if that player has won, otherwise None."""
        for line in self._LINES:
            values = [grid.get(r, c) for r, c in line]
            if values[0] is not None and values[0] == values[1] == values[2]:
                return values[0]
        return None

    def is_draw(self, grid: Grid) -> bool:
        """Return True if the grid is full and there is no winner."""
        if self.winner(grid) is not None:
            return False
        return all(grid.get(r, c) is not None for r in range(3) for c in range(3))

    def is_game_over(self, grid: Grid) -> bool:
        """Return True if the game has ended (win or draw)."""
        return self.winner(grid) is not None or self.is_draw(grid)
