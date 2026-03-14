from player import Player


class TestPlayer:
    def test_name(self):
        player = Player("Alice")
        assert player.name == "Alice"

    def test_two_players(self):
        p1 = Player("Alice")
        p2 = Player("Bob")
        assert p1.name == "Alice"
        assert p2.name == "Bob"
