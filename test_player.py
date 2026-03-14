import pytest
from player import Player


class TestPlayer:
    def test_name(self):
        player = Player("Alice", 1)
        assert player.name == "Alice"

    def test_id(self):
        player = Player("Alice", 1)
        assert player.id == 1

    def test_invalid_id(self):
        with pytest.raises(ValueError):
            Player("Alice", 3)

    def test_two_players(self):
        p1 = Player("Alice", 1)
        p2 = Player("Bob", 2)
        assert p1.name == "Alice"
        assert p1.id == 1
        assert p2.name == "Bob"
        assert p2.id == 2
