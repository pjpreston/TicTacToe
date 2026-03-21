import anthropic
from grid import Grid
from pydantic import BaseModel

#DEFAULT_MODEL = 'claude-sonnet-4-6'
#DEFAULT_MODEL = 'claude-haiku-4-5-20251001'
DEFAULT_MODEL = 'claude-opus-4-6'

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

    system = """You are an expert Tic-Tac-Toe player. Before choosing a move, think several moves ahead:
1. Check if you can win immediately (complete a 3-in-a-row).
2. Check if your opponent can win on their next turn — if so, block them.
3. For each available cell, simulate what your opponent's best response would be, and what you would do after that.
4. Prioritize: centre (1,1), then corners (0,0), (0,2), (2,0), (2,2), then edges.
Choose the move that gives you the best outcome after looking ahead."""

    prompt = f"""You are '{marker}', your opponent is '{opponent}'.

The board (rows 0-2, cols 0-2, '.' = empty):
{board_str}

Available cells: {empty_cells}

Analyse each available move by considering what happens 2-3 moves ahead, then use the make_move tool to place your marker at the best cell."""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=3000,
        system=system,
        thinking={"type": "enabled", "budget_tokens": 2000},
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
