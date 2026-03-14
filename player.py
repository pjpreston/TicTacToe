class Player:
    """Represents a TicTacToe player."""

    def __init__(self, name: str, player_id: int):
        if player_id not in (1, 2):
            raise ValueError(f"Player id must be 1 or 2, got {player_id!r}")
        self._name = name
        self._id = player_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id
