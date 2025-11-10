"""
Unit tests for Player class.
"""

import unittest
from model.player import Player
from model.enums import PlayerColor
from model.position import Position


class TestPlayer(unittest.TestCase):
    """Test cases for Player class."""

    def test_player_creation(self):
        """Test creating a player with name and color."""
        player = Player("Alice", PlayerColor.RED)

        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.color, PlayerColor.RED)
        self.assertEqual(len(player.pieces), 0)

    def test_player_name_property(self):
        """Test that name property is read-only."""
        player = Player("Bob", PlayerColor.BLUE)
        self.assertEqual(player.name, "Bob")

        # Name should not be modifiable
        with self.assertRaises(AttributeError):
            player.name = "Charlie"

    def test_player_color_property(self):
        """Test that color property is read-only."""
        player = Player("Alice", PlayerColor.RED)
        self.assertEqual(player.color, PlayerColor.RED)

        # Color should not be modifiable
        with self.assertRaises(AttributeError):
            player.color = PlayerColor.BLUE

    def test_add_piece(self):
        """Test adding pieces to a player."""
        from model.piece import Cat

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))

        player.add_piece(cat)

        self.assertEqual(len(player.pieces), 1)
        self.assertIn(cat, player.pieces)

    def test_add_multiple_pieces(self):
        """Test adding multiple pieces to a player."""
        from model.piece import Cat, Dog, Wolf

        player = Player("Bob", PlayerColor.BLUE)
        cat = Cat(player, Position(2, 0))
        dog = Dog(player, Position(2, 1))
        wolf = Wolf(player, Position(2, 2))

        player.add_piece(cat)
        player.add_piece(dog)
        player.add_piece(wolf)

        self.assertEqual(len(player.pieces), 3)
        self.assertIn(cat, player.pieces)
        self.assertIn(dog, player.pieces)
        self.assertIn(wolf, player.pieces)

    def test_remove_piece(self):
        """Test removing a piece from a player."""
        from model.piece import Cat

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))

        player.add_piece(cat)
        self.assertEqual(len(player.pieces), 1)

        player.remove_piece(cat)
        self.assertEqual(len(player.pieces), 0)
        self.assertNotIn(cat, player.pieces)

    def test_remove_nonexistent_piece(self):
        """Test removing a piece that doesn't exist (should not raise error)."""
        from model.piece import Cat, Dog

        player = Player("Bob", PlayerColor.BLUE)
        cat = Cat(player, Position(2, 0))
        dog = Dog(player, Position(2, 1))

        player.add_piece(cat)

        # Removing a piece that was never added should not raise an error
        player.remove_piece(dog)
        self.assertEqual(len(player.pieces), 1)

    def test_get_active_pieces(self):
        """Test getting all active pieces."""
        from model.piece import Cat, Dog

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))
        dog = Dog(player, Position(2, 1))

        player.add_piece(cat)
        player.add_piece(dog)

        active_pieces = player.get_active_pieces()

        self.assertEqual(len(active_pieces), 2)
        self.assertIn(cat, active_pieces)
        self.assertIn(dog, active_pieces)

    def test_get_active_pieces_returns_list(self):
        """Test that get_active_pieces returns a list."""
        player = Player("Bob", PlayerColor.BLUE)

        active_pieces = player.get_active_pieces()

        self.assertIsInstance(active_pieces, list)
        self.assertEqual(len(active_pieces), 0)

    def test_has_pieces_with_pieces(self):
        """Test has_pieces returns True when player has pieces."""
        from model.piece import Cat

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))

        player.add_piece(cat)

        self.assertTrue(player.has_pieces())

    def test_has_pieces_without_pieces(self):
        """Test has_pieces returns False when player has no pieces."""
        player = Player("Bob", PlayerColor.BLUE)

        self.assertFalse(player.has_pieces())

    def test_has_pieces_after_removal(self):
        """Test has_pieces after removing all pieces."""
        from model.piece import Cat

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))

        player.add_piece(cat)
        self.assertTrue(player.has_pieces())

        player.remove_piece(cat)
        self.assertFalse(player.has_pieces())

    def test_get_den_position_red_player(self):
        """Test getting den position for red player."""
        player = Player("Alice", PlayerColor.RED)

        den_pos = player.get_den_position()

        self.assertEqual(den_pos, Position(8, 3))

    def test_get_den_position_blue_player(self):
        """Test getting den position for blue player."""
        player = Player("Bob", PlayerColor.BLUE)

        den_pos = player.get_den_position()

        self.assertEqual(den_pos, Position(0, 3))

    def test_get_trap_positions_red_player(self):
        """Test getting trap positions for red player."""
        player = Player("Alice", PlayerColor.RED)

        trap_positions = player.get_trap_positions()

        self.assertEqual(len(trap_positions), 4)
        self.assertIn(Position(7, 2), trap_positions)
        self.assertIn(Position(7, 4), trap_positions)
        self.assertIn(Position(8, 2), trap_positions)
        self.assertIn(Position(8, 4), trap_positions)

    def test_get_trap_positions_blue_player(self):
        """Test getting trap positions for blue player."""
        player = Player("Bob", PlayerColor.BLUE)

        trap_positions = player.get_trap_positions()

        self.assertEqual(len(trap_positions), 4)
        self.assertIn(Position(0, 2), trap_positions)
        self.assertIn(Position(0, 4), trap_positions)
        self.assertIn(Position(1, 2), trap_positions)
        self.assertIn(Position(1, 4), trap_positions)

    def test_player_string_representation(self):
        """Test string representation of player."""
        player = Player("Alice", PlayerColor.RED)

        player_str = str(player)

        self.assertIn("Alice", player_str)
        self.assertIn("red", player_str)

    def test_player_repr(self):
        """Test developer-friendly representation."""
        player = Player("Bob", PlayerColor.BLUE)

        player_repr = repr(player)

        self.assertIn("Player", player_repr)
        self.assertIn("Bob", player_repr)
        self.assertIn("blue", player_repr)
        self.assertIn("pieces=0", player_repr)

    def test_player_equality(self):
        """Test player equality comparison."""
        player1 = Player("Alice", PlayerColor.RED)
        player2 = Player("Alice", PlayerColor.RED)
        player3 = Player("Bob", PlayerColor.RED)
        player4 = Player("Alice", PlayerColor.BLUE)

        # Same name and color should be equal
        self.assertEqual(player1, player2)

        # Different name should not be equal
        self.assertNotEqual(player1, player3)

        # Different color should not be equal
        self.assertNotEqual(player1, player4)

    def test_player_hash(self):
        """Test that players can be used in sets and as dict keys."""
        player1 = Player("Alice", PlayerColor.RED)
        player2 = Player("Alice", PlayerColor.RED)
        player3 = Player("Bob", PlayerColor.BLUE)

        # Should be able to add to set
        player_set = {player1, player2, player3}

        # player1 and player2 are equal, so set should have 2 elements
        self.assertEqual(len(player_set), 2)

        # Should be able to use as dict key
        player_dict = {player1: "first", player3: "second"}
        self.assertEqual(player_dict[player2], "first")

    def test_pieces_property_returns_copy(self):
        """Test that pieces property returns a copy, not the original set."""
        from model.piece import Cat

        player = Player("Alice", PlayerColor.RED)
        cat = Cat(player, Position(2, 0))

        player.add_piece(cat)

        pieces1 = player.pieces
        pieces2 = player.pieces

        # Should be equal but not the same object
        self.assertEqual(pieces1, pieces2)
        self.assertIsNot(pieces1, pieces2)


if __name__ == '__main__':
    unittest.main()
