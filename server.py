from flask import Flask, jsonify, request, Response
from grid import Grid
from rules import Rules

app = Flask(__name__)
grid = Grid()
rules = Rules()


@app.post('/cell')
def set_cell():
    """Set a cell value. Body: {"row": 0, "col": 0, "value": "X"}"""
    data = request.get_json(force=True)
    try:
        row = int(data['row'])
        col = int(data['col'])
        value = str(data['value'])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Request must include integer 'row', 'col' and string 'value'"), 400

    try:
        grid.set(row, col, value)
    except (IndexError, ValueError) as e:
        return jsonify(error=str(e)), 400

    winner = rules.winner(grid)
    draw = rules.is_draw(grid)
    return jsonify(row=row, col=col, value=value, winner=winner, draw=draw), 200


@app.get('/')
def render_grid():
    """Render the current grid state as an HTML page."""
    rows_html = ''
    for row in range(3):
        cells_html = ''
        for col in range(3):
            cell = grid.get(row, col) or ''
            cells_html += f'<td>{cell}</td>'
        rows_html += f'<tr>{cells_html}</tr>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tic-Tac-Toe</title>
  <style>
    body {{ font-family: sans-serif; display: flex; justify-content: center; padding-top: 60px; }}
    table {{ border-collapse: collapse; }}
    td {{
      width: 80px; height: 80px;
      border: 3px solid #333;
      text-align: center; vertical-align: middle;
      font-size: 2.5rem; font-weight: bold;
    }}
  </style>
</head>
<body>
  <table>{rows_html}</table>
</body>
</html>'''
    return Response(html, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)
