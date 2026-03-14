class Grid:
    """Represents a 3x3 tic-tac-toe grid."""

    def __init__(self):
        self._cells = [[None] * 3 for _ in range(3)]

    def get(self, row: int, col: int) -> str | None:
        """Return the value at (row, col): 'X', 'O', or None."""
        self._check_bounds(row, col)
        return self._cells[row][col]

    def set(self, row: int, col: int, value: str) -> None:
        """Place 'X' or 'O' at (row, col). Raises ValueError if already occupied."""
        self._check_bounds(row, col)
        if value not in ('X', 'O'):
            raise ValueError(f"Value must be 'X' or 'O', got {value!r}")
        if self._cells[row][col] is not None:
            raise ValueError(f"Cell ({row}, {col}) is already occupied")
        self._cells[row][col] = value

    def render(self) -> None:
        """Print the grid to the screen."""
        for i, row in enumerate(self._cells):
            print(' | '.join(cell if cell is not None else ' ' for cell in row))
            if i < 2:
                print('-----------')

    def _check_bounds(self, row: int, col: int) -> None:
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise IndexError(f"Position ({row}, {col}) is out of bounds")
