import json
import anthropic
from grid import Grid
from pydantic import BaseModel
DEFAULT_MODEL = 'claude-sonnet-4-6'
#DEFAULT_MODEL = 'claude-opus-4-6'

class Coordinate(BaseModel):
    row: int
    col: int

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

Respond with ONLY a JSON object in this format: {{"row": <int>, "col": <int>}}
Pick your next move."""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=50,        
        messages=[
            {"role": "user", "content": prompt},            
        ],
    )

    response_text = "{" + message.content[0].text.strip()

    print(f"LLM response = {response_text}")

    # Parse the JSON response, retrying with fallback if needed
    try:
        move = json.loads(response_text)
        row, col = int(move['row']), int(move['col'])
        if (row, col) in empty_cells:
            print(f"Parsed ({row}, {col}) from response")
            return (row, col)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("Could not parse LLM response.")
        pass

    print("...into fallback territory...")

    # Fallback: try to extract numbers from the response
    import re
    numbers = re.findall(r'\d+', response_text)
    if len(numbers) >= 2:
        row, col = int(numbers[0]), int(numbers[1])
        if (row, col) in empty_cells:
            print("Using some weirdly extracted numbers from the response as fallback")
            return (row, col)

    print(f"Last resort - using first empty cell I can find : ({empty_cells[0] if empty_cells else 'No moves left'})")

    # Last resort: pick the first available cell
    return empty_cells[0]
