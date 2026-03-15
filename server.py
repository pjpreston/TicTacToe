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
game = None


@app.post('/start')
def start_game():
    """Start a new game. Body: {"player1": "Alice", "player2": "Bob"}"""
    global game
    data = request.get_json(force=True)
    try:
        name1 = str(data['player1']).strip()
        name2 = str(data['player2']).strip()
    except (KeyError, TypeError):
        return jsonify(error="Request must include 'player1' and 'player2' names"), 400
    if not name1 or not name2:
        return jsonify(error="Player names cannot be empty"), 400
    if name1 == name2:
        return jsonify(error="Player names must be different"), 400
    game = Game(Player(name1, 1), Player(name2, 2))
    return jsonify(player1=name1, player2=name2), 200


@app.post('/cell')
def set_cell():
    """Set a cell value. Body: {"row": 0, "col": 0, "value": "X", "player": "Player 1"}"""
    if game is None:
        return jsonify(error="Game has not been started yet"), 400
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


@app.get('/move-count')
def move_count():
    """Return the current move count for polling."""
    if game is None:
        return jsonify(move_count=-1)
    return jsonify(move_count=game.move_count)


def _render_setup():
    """Render the player name entry form."""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tic-Tac-Toe - Setup</title>
  <style>
    body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding-top: 60px; }
    h1 { margin-bottom: 20px; }
    #setup-form { display: flex; flex-direction: column; gap: 10px; align-items: center; }
    #setup-form label { font-size: 1rem; }
    #setup-form input { padding: 5px; font-size: 1rem; width: 200px; }
    #setup-form button { padding: 8px 20px; font-size: 1rem; cursor: pointer; margin-top: 10px; }
    #error { color: red; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>Tic-Tac-Toe</h1>
  <div id="setup-form">
    <label>Player 1 (X): <input type="text" id="player1"></label>
    <label>Player 2 (O): <input type="text" id="player2"></label>
    <button id="start-btn">Start Game</button>
  </div>
  <p id="error"></p>
  <script>
    document.getElementById('start-btn').addEventListener('click', async () => {
      const p1 = document.getElementById('player1').value.trim();
      const p2 = document.getElementById('player2').value.trim();
      const errorEl = document.getElementById('error');
      errorEl.textContent = '';
      if (!p1 || !p2) {
        errorEl.textContent = 'Please enter both player names.';
        return;
      }
      try {
        const resp = await fetch('/start', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({player1: p1, player2: p2})
        });
        const data = await resp.json();
        if (!resp.ok) {
          errorEl.textContent = data.error || 'Unknown error';
        } else {
          window.location.reload();
        }
      } catch (err) {
        errorEl.textContent = 'Network error: ' + err.message;
      }
    });
  </script>
</body>
</html>'''
    return Response(html, mimetype='text/html')


@app.get('/')
def render_grid():
    """Render the current grid state as an HTML page."""
    if game is None:
        return _render_setup()

    current_name = game.current_player.name
    current_marker = 'X' if game.current_player is game.player1 else 'O'
    winner = game.rules.winner(game.grid)
    draw = game.rules.is_draw(game.grid)
    game_over = winner is not None or draw

    if winner:
        winner_name = game.player1.name if winner == 'X' else game.player2.name
        status_message = f'{winner_name} wins!'
    elif draw:
        status_message = "It's a draw!"
    else:
        status_message = f'Current turn: {current_name} ({current_marker})'

    header_html = '<tr><th></th>'
    for col in range(3):
        header_html += f'<th>{col}</th>'
    header_html += '</tr>'

    rows_html = ''
    for row in range(3):
        cells_html = f'<th>{row}</th>'
        for col in range(3):
            cell = game.grid.get(row, col) or ''
            cells_html += f'<td>{cell}</td>'
        rows_html += f'<tr>{cells_html}</tr>'

    form_display = 'none' if game_over else 'flex'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tic-Tac-Toe</title>
  <style>
    body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding-top: 40px; }}
    h2 {{ margin-bottom: 10px; }}
    table {{ border-collapse: collapse; }}
    td {{
      width: 80px; height: 80px;
      border: 3px solid #333;
      text-align: center; vertical-align: middle;
      font-size: 2.5rem; font-weight: bold;
    }}
    th {{
      width: 30px; height: 30px;
      text-align: center; vertical-align: middle;
      font-size: 1rem; font-weight: normal;
      color: #666;
    }}
    #move-form {{
      display: {form_display}; gap: 10px; align-items: center; margin-top: 20px;
    }}
    #move-form input {{
      width: 50px; padding: 5px; font-size: 1rem; text-align: center;
    }}
    #move-form button {{
      padding: 6px 16px; font-size: 1rem; cursor: pointer;
    }}
    #error {{ color: red; margin-top: 10px; }}
  </style>
</head>
<body>
  <h2>{status_message}</h2>
  <table>{header_html}{rows_html}</table>
  <div id="move-form">
    <label>Row: <input type="number" id="row" min="0" max="2"></label>
    <label>Col: <input type="number" id="col" min="0" max="2"></label>
    <button id="move-btn">Move</button>
  </div>
  <p id="error"></p>
  <script>
    const btn = document.getElementById('move-btn');
    if (btn) {{
      btn.addEventListener('click', async () => {{
        const row = parseInt(document.getElementById('row').value);
        const col = parseInt(document.getElementById('col').value);
        const errorEl = document.getElementById('error');
        errorEl.textContent = '';
        if (isNaN(row) || isNaN(col)) {{
          errorEl.textContent = 'Please enter both row and col values.';
          return;
        }}
        try {{
          const resp = await fetch('/cell', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{row, col, value: '{current_marker}', player: '{current_name}'}})
          }});
          const data = await resp.json();
          if (!resp.ok) {{
            errorEl.textContent = data.error || 'Unknown error';
          }} else {{
            window.location.reload();
          }}
        }} catch (err) {{
          errorEl.textContent = 'Network error: ' + err.message;
        }}
      }});
    }}
    let knownMoveCount = {game.move_count};
    setInterval(async () => {{
      try {{
        const resp = await fetch('/move-count');
        const data = await resp.json();
        if (data.move_count !== knownMoveCount) {{
          window.location.reload();
        }}
      }} catch (e) {{}}
    }}, 2000);
  </script>
</body>
</html>'''
    return Response(html, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)
