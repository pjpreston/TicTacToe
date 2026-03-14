import pytest
from grid import Grid
from rules import Rules


@pytest.fixture
def grid():
    return Grid()


@pytest.fixture
def rules():
    return Rules()


def fill(grid, moves):
    """Helper: apply a list of (row, col, value) moves to a grid."""
    for row, col, value in moves:
        grid.set(row, col, value)


class TestWinner:
    def test_no_winner_on_empty_grid(self, grid, rules):
        assert rules.winner(grid) is None

    def test_x_wins_top_row(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (0, 1, 'X'), (0, 2, 'X')])
        assert rules.winner(grid) == 'X'

    def test_o_wins_middle_row(self, grid, rules):
        fill(grid, [(1, 0, 'O'), (1, 1, 'O'), (1, 2, 'O')])
        assert rules.winner(grid) == 'O'

    def test_x_wins_bottom_row(self, grid, rules):
        fill(grid, [(2, 0, 'X'), (2, 1, 'X'), (2, 2, 'X')])
        assert rules.winner(grid) == 'X'

    def test_x_wins_left_column(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (1, 0, 'X'), (2, 0, 'X')])
        assert rules.winner(grid) == 'X'

    def test_o_wins_middle_column(self, grid, rules):
        fill(grid, [(0, 1, 'O'), (1, 1, 'O'), (2, 1, 'O')])
        assert rules.winner(grid) == 'O'

    def test_x_wins_right_column(self, grid, rules):
        fill(grid, [(0, 2, 'X'), (1, 2, 'X'), (2, 2, 'X')])
        assert rules.winner(grid) == 'X'

    def test_x_wins_main_diagonal(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (1, 1, 'X'), (2, 2, 'X')])
        assert rules.winner(grid) == 'X'

    def test_o_wins_anti_diagonal(self, grid, rules):
        fill(grid, [(0, 2, 'O'), (1, 1, 'O'), (2, 0, 'O')])
        assert rules.winner(grid) == 'O'

    def test_no_winner_partial_board(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X')])
        assert rules.winner(grid) is None


class TestIsDraw:
    def test_empty_grid_is_not_draw(self, grid, rules):
        assert rules.is_draw(grid) is False

    def test_draw_when_full_with_no_winner(self, grid, rules):
        # X O X
        # X X O
        # O X O
        fill(grid, [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'X'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'O'),
        ])
        assert rules.is_draw(grid) is True

    def test_not_draw_when_winner_exists(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (0, 1, 'X'), (0, 2, 'X')])
        assert rules.is_draw(grid) is False

    def test_not_draw_when_board_not_full(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (0, 1, 'O')])
        assert rules.is_draw(grid) is False


class TestIsGameOver:
    def test_not_over_on_empty_grid(self, grid, rules):
        assert rules.is_game_over(grid) is False

    def test_over_when_winner(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (0, 1, 'X'), (0, 2, 'X')])
        assert rules.is_game_over(grid) is True

    def test_over_on_draw(self, grid, rules):
        fill(grid, [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'X'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'O'),
        ])
        assert rules.is_game_over(grid) is True

    def test_not_over_mid_game(self, grid, rules):
        fill(grid, [(0, 0, 'X'), (1, 1, 'O'), (0, 1, 'X')])
        assert rules.is_game_over(grid) is False
