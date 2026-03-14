import pytest
from grid import Grid


@pytest.fixture
def grid():
    return Grid()


class TestGet:
    def test_empty_cell_returns_none(self, grid):
        assert grid.get(0, 0) is None

    def test_all_cells_initially_none(self, grid):
        for row in range(3):
            for col in range(3):
                assert grid.get(row, col) is None

    def test_returns_correct_value_after_set(self, grid):
        grid.set(1, 2, 'X')
        assert grid.get(1, 2) == 'X'

    def test_out_of_bounds_raises(self, grid):
        with pytest.raises(IndexError):
            grid.get(3, 0)

    def test_negative_index_raises(self, grid):
        with pytest.raises(IndexError):
            grid.get(-1, 0)


class TestSet:
    def test_set_x(self, grid):
        grid.set(0, 0, 'X')
        assert grid.get(0, 0) == 'X'

    def test_set_o(self, grid):
        grid.set(2, 2, 'O')
        assert grid.get(2, 2) == 'O'

    def test_occupied_cell_raises(self, grid):
        grid.set(0, 0, 'X')
        with pytest.raises(ValueError):
            grid.set(0, 0, 'O')

    def test_occupied_cell_unchanged_after_failed_set(self, grid):
        grid.set(0, 0, 'X')
        with pytest.raises(ValueError):
            grid.set(0, 0, 'O')
        assert grid.get(0, 0) == 'X'

    def test_invalid_value_raises(self, grid):
        with pytest.raises(ValueError):
            grid.set(0, 0, 'Z')

    def test_lowercase_value_raises(self, grid):
        with pytest.raises(ValueError):
            grid.set(0, 0, 'x')

    def test_out_of_bounds_raises(self, grid):
        with pytest.raises(IndexError):
            grid.set(0, 3, 'X')

    def test_does_not_affect_other_cells(self, grid):
        grid.set(1, 1, 'X')
        assert grid.get(0, 0) is None
        assert grid.get(2, 2) is None


class TestRender:
    def test_renders_empty_grid(self, grid, capsys):
        grid.render()
        output = capsys.readouterr().out
        assert output == "  |   |  \n-----------\n  |   |  \n-----------\n  |   |  \n"

    def test_renders_x_in_correct_position(self, grid, capsys):
        grid.set(0, 0, 'X')
        grid.render()
        output = capsys.readouterr().out
        assert output.startswith('X')

    def test_renders_o_in_correct_position(self, grid, capsys):
        grid.set(2, 2, 'O')
        grid.render()
        output = capsys.readouterr().out
        assert output.strip().endswith('O')

    def test_renders_separators(self, grid, capsys):
        grid.render()
        output = capsys.readouterr().out
        assert output.count('-----------') == 2
