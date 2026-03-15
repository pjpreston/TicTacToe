from grid import Grid
from rules import Rules


def choose_move(grid: Grid, marker: str) -> tuple[int, int]:
    """Choose the best move for the given marker using minimax.

    Returns a (row, col) tuple for the best available cell.
    """
    opponent = 'O' if marker == 'X' else 'X'
    rules = Rules()

    def _minimax(g: Grid, is_maximising: bool) -> int:
        winner = rules.winner(g)
        if winner == marker:
            return 1
        if winner == opponent:
            return -1
        if rules.is_draw(g):
            return 0

        best = -2 if is_maximising else 2
        current_marker = marker if is_maximising else opponent
        for r in range(3):
            for c in range(3):
                if g.get(r, c) is None:
                    g._cells[r][c] = current_marker
                    score = _minimax(g, not is_maximising)
                    g._cells[r][c] = None
                    if is_maximising:
                        best = max(best, score)
                    else:
                        best = min(best, score)
        return best

    best_score = -2
    best_move = None
    for r in range(3):
        for c in range(3):
            if grid.get(r, c) is None:
                grid._cells[r][c] = marker
                score = _minimax(grid, False)
                grid._cells[r][c] = None
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move
