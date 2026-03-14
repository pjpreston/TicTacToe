# testing notes
# start server with `python server.py`
# use curl to set cell values, e.g.:
# curl -X POST -H "Content-Type: application/json" -d '{"row":0,"col":0,"value":"X","player":"Player 1"}' http://localhost:5000/cell        
# better - use SIMPLE REST CLIENT
# POST this BODY {"row":0,"col":1,"value":"X", "player":"Player 1"}
# to URL http://localhost:5000/cell

from flask import Flask, jsonify, request, Response
from game import Game
from player import Player

app = Flask(__name__)
game = Game(Player("Player 1", 1), Player("Player 2", 2))


@app.post('/cell')
def set_cell():
    """Set a cell value. Body: {"row": 0, "col": 0, "value": "X", "player": "Player 1"}"""
    data = request.get_json(force=True)
    try:
        row = int(data['row'])
        col = int(data['col'])
        value = str(data['value'])
        player_name = str(data['player'])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="Request must include integer 'row', 'col', string 'value', and string 'player'"), 400

    try:
        player = game.get_player_by_name(player_name)
    except ValueError:
        return jsonify(error=f"No player named '{player_name}'"), 400

    if player is not game.current_player:
        return jsonify(error=f"Invalid move. It is currently {game.current_player.name}'s turn"), 400

    try:
        game.make_move(player, row, col, value)
    except (IndexError, ValueError) as e:
        return jsonify(error=str(e)), 400

    winner = game.rules.winner(game.grid)
    draw = game.rules.is_draw(game.grid)
    next_player = game.current_player.name
    print(f"Next turn: {next_player}")
    return jsonify(row=row, col=col, value=value, winner=winner, draw=draw, next_player=next_player), 200


@app.get('/')
def render_grid():
    """Render the current grid state as an HTML page."""
    rows_html = ''
    for row in range(3):
        cells_html = ''
        for col in range(3):
            cell = game.grid.get(row, col) or ''
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
