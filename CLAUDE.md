# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A TicTacToe game built with Python and Flask. The server exposes a web UI (`GET /`) and an API endpoint (`POST /cell`) for making moves.

## Commands

- **Run all tests:** `python -m pytest -q`
- **Run a single test file:** `python -m pytest test_rules.py -q`
- **Run the server:** `python server.py` (Flask dev server on port 5000)

## Architecture

Layered design with no circular dependencies:

```
server.py (Flask routes) → game.py (orchestrator) → grid.py, rules.py, player.py
```

- **Game** composes 2 Players, 1 Grid, and 1 Rules instance
- **Rules** is stateless — takes a Grid and evaluates win/draw conditions
- **Grid** holds mutable 3x3 board state; values are `'X'`, `'O'`, or `None`
- **Player** holds a player name

Tests mirror source files (`test_grid.py`, `test_rules.py`, `test_player.py`, `test_game.py`) using pytest with fixtures.

## Jira Integration

Issues are tracked in the **KAN** project on `londoncoders.atlassian.net` (cloud ID: `e98c6404-1046-4186-a5ee-645e94e6f939`).
