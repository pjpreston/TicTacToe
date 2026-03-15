import pytest
from grid import Grid
from ai_player import choose_move


@pytest.fixture
def grid():
    return Grid()


def test_choose_move_returns_valid_cell(grid):
    row, col = choose_move(grid, 'X')
    assert 0 <= row <= 2
    assert 0 <= col <= 2


def test_choose_move_picks_empty_cell(grid):
    grid.set(0, 0, 'X')
    row, col = choose_move(grid, 'O')
    assert grid.get(row, col) is None


def test_choose_move_takes_winning_move(grid):
    grid.set(0, 0, 'O')
    grid.set(0, 1, 'O')
    # O should complete the top row
    row, col = choose_move(grid, 'O')
    assert (row, col) == (0, 2)


def test_choose_move_blocks_opponent_win(grid):
    grid.set(0, 0, 'X')
    grid.set(0, 1, 'X')
    # O should block X from winning at (0, 2)
    row, col = choose_move(grid, 'O')
    assert (row, col) == (0, 2)


def test_choose_move_only_one_cell_left(grid):
    grid.set(0, 0, 'X')
    grid.set(0, 1, 'O')
    grid.set(0, 2, 'X')
    grid.set(1, 0, 'O')
    grid.set(1, 1, 'X')
    grid.set(1, 2, 'X')
    grid.set(2, 0, 'O')
    grid.set(2, 1, 'X')
    # Only (2, 2) is left
    row, col = choose_move(grid, 'O')
    assert (row, col) == (2, 2)
