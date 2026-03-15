import anthropic
from grid import Grid
from pydantic import BaseModel

DEFAULT_MODEL = 'claude-sonnet-4-6'


class Coordinate(BaseModel):
    row: int
    col: int


MAKE_MOVE_TOOL = {
    "name": "make_move",
    "description": "Place your marker on the board at the given coordinate.",
    "input_schema": Coordinate.model_json_schema(),
}


def choose_move(grid: Grid, marker: str, model: str = DEFAULT_MODEL) -> tuple[int, int]:
    """Choose a move by asking an LLM to pick the best cell.

    Returns a (row, col) tuple for the chosen cell.
    """
    opponent = 'O' if marker == 'X' else 'X'
    board_lines = []
    for r in range(3):
        row_cells = []
        for c in range(3):
            val = grid.get(r, c)
            row_cells.append(val if val else '.')
        board_lines.append(' '.join(row_cells))
    board_str = '\n'.join(board_lines)

    empty_cells = [
        (r, c) for r in range(3) for c in range(3) if grid.get(r, c) is None
    ]

    prompt = f"""You are playing Tic-Tac-Toe. You are '{marker}', your opponent is '{opponent}'.

The board (rows 0-2, cols 0-2, '.' = empty):
{board_str}

Available cells: {empty_cells}

Use the make_move tool to place your marker. Pick the best move."""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=200,
        tools=[MAKE_MOVE_TOOL],
        tool_choice={"type": "tool", "name": "make_move"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in message.content:
        if block.type == "tool_use" and block.name == "make_move":
            coord = Coordinate.model_validate(block.input)
            print(f"LLM move: ({coord.row}, {coord.col})")
            if (coord.row, coord.col) in empty_cells:
                return (coord.row, coord.col)

    # Fallback: first available cell
    print(f"LLM did not return a valid move, using first empty cell: {empty_cells[0]}")
    return empty_cells[0]
