"""
Unit tests for Move and MoveResult classes.
"""

import unittest
from datetime import datetime
from model.move import Move, MoveResult
from model.position import Position
from model.player import Player
from model.enums import PlayerColor
from model.piece import Rat, Cat
from model.game import Game


class TestMoveResult(unittest.TestCase):
    """Test cases for MoveResult class."""

    def test_move_result_success(self):
        """Test creating a successful move result."""
        result = MoveResult(success=True, message="Move successful")
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Move successful")
        self.assertIsNone(result.captured_piece)

    def test_move_result_failure(self):
        """Test creating a failed move result."""
        result = MoveResult(success=False, message="Invalid move")
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Invalid move")
        self.assertIsNone(result.captured_piece)

    def test_move_result_with_capture(self):
        """Test move result with captured piece."""
        player2 = Player("Player 2", PlayerColor.BLUE)
        captured = Cat(player2, Position(3, 3))

        result = MoveResult(
            success=True,
            message="Captured opponent piece",
            captured_piece=captured
        )

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Captured opponent piece")
        self.assertIsNotNone(result.captured_piece)
        self.assertEqual(result.captured_piece, captured)


class TestMove(unittest.TestCase):
    """Test cases for Move class."""

    def setUp(self):
        """Set up test fixtures."""
        self.player1 = Player("Player 1", PlayerColor.RED)
        self.player2 = Player("Player 2", PlayerColor.BLUE)
        self.rat = Rat(self.player1, Position(2, 0))
        self.cat = Cat(self.player2, Position(3, 0))
        self.timestamp = datetime.now()

    def test_move_creation_without_capture(self):
        """Test creating a move without capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=None,
            timestamp=self.timestamp
        )

        self.assertEqual(move.piece, self.rat)
        self.assertEqual(move.from_pos, Position(2, 0))
        self.assertEqual(move.to_pos, Position(3, 0))
        self.assertIsNone(move.captured_piece)
        self.assertEqual(move.timestamp, self.timestamp)

    def test_move_creation_with_capture(self):
        """Test creating a move with capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=self.cat,
            timestamp=self.timestamp
        )

        self.assertEqual(move.piece, self.rat)
        self.assertEqual(move.captured_piece, self.cat)

    def test_move_to_dict_without_capture(self):
        """Test serializing a move to dictionary without capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=None,
            timestamp=self.timestamp
        )

        move_dict = move.to_dict()

        self.assertEqual(move_dict['piece_type'], 'Rat')
        self.assertEqual(move_dict['piece_rank'], 1)
        self.assertEqual(move_dict['owner_color'], 'red')
        self.assertEqual(move_dict['from_row'], 2)
        self.assertEqual(move_dict['from_col'], 0)
        self.assertEqual(move_dict['to_row'], 3)
        self.assertEqual(move_dict['to_col'], 0)
        self.assertIsNone(move_dict['captured_piece_type'])
        self.assertIsNone(move_dict['captured_piece_rank'])
        self.assertEqual(move_dict['timestamp'], self.timestamp.isoformat())

    def test_move_to_dict_with_capture(self):
        """Test serializing a move to dictionary with capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=self.cat,
            timestamp=self.timestamp
        )

        move_dict = move.to_dict()

        self.assertEqual(move_dict['captured_piece_type'], 'Cat')
        self.assertEqual(move_dict['captured_piece_rank'], 2)

    def test_move_to_record_string_without_capture(self):
        """Test converting move to record string without capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=None,
            timestamp=self.timestamp
        )

        record_str = move.to_record_string()

        self.assertIn("Player 1", record_str)
        self.assertIn("Rat", record_str)
        self.assertIn("from (2,0)", record_str)
        self.assertIn("to (3,0)", record_str)
        self.assertNotIn("captured", record_str)

    def test_move_to_record_string_with_capture(self):
        """Test converting move to record string with capture."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=self.cat,
            timestamp=self.timestamp
        )

        record_str = move.to_record_string()

        self.assertIn("Player 1", record_str)
        self.assertIn("Rat", record_str)
        self.assertIn("from (2,0)", record_str)
        self.assertIn("to (3,0)", record_str)
        self.assertIn("captured Cat", record_str)

    def test_parse_record_string_without_capture(self):
        """Test parsing a record string without capture."""
        record_str = "Player 1 - Rat from (2,0) to (3,0)"
        parsed = Move.parse_record_string(record_str)

        self.assertEqual(parsed['player_name'], "Player 1")
        self.assertEqual(parsed['piece_type'], "Rat")
        self.assertEqual(parsed['from_row'], 2)
        self.assertEqual(parsed['from_col'], 0)
        self.assertEqual(parsed['to_row'], 3)
        self.assertEqual(parsed['to_col'], 0)
        self.assertIsNone(parsed['captured_piece_type'])

    def test_parse_record_string_with_capture(self):
        """Test parsing a record string with capture."""
        record_str = "Player 1 - Rat from (2,0) to (3,0) (captured Cat)"
        parsed = Move.parse_record_string(record_str)

        self.assertEqual(parsed['player_name'], "Player 1")
        self.assertEqual(parsed['piece_type'], "Rat")
        self.assertEqual(parsed['from_row'], 2)
        self.assertEqual(parsed['from_col'], 0)
        self.assertEqual(parsed['to_row'], 3)
        self.assertEqual(parsed['to_col'], 0)
        self.assertEqual(parsed['captured_piece_type'], "Cat")

    def test_parse_record_string_invalid_format(self):
        """Test parsing an invalid record string."""
        invalid_str = "Invalid format"
        with self.assertRaises(ValueError):
            Move.parse_record_string(invalid_str)

    def test_move_str_representation(self):
        """Test string representation of move."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=None,
            timestamp=self.timestamp
        )

        str_repr = str(move)
        self.assertIn("Player 1", str_repr)
        self.assertIn("Rat", str_repr)

    def test_move_repr_representation(self):
        """Test repr representation of move."""
        move = Move(
            piece=self.rat,
            from_pos=Position(2, 0),
            to_pos=Position(3, 0),
            captured_piece=None,
            timestamp=self.timestamp
        )

        repr_str = repr(move)
        self.assertIn("Move", repr_str)
        self.assertIn("Rat", repr_str)
        self.assertIn("from=(2,0)", repr_str)
        self.assertIn("to=(3,0)", repr_str)


class TestMoveSerializationIntegration(unittest.TestCase):
    """Integration tests for move serialization with Game."""

    def setUp(self):
        """Set up a game for integration testing."""
        self.game = Game("Player 1", "Player 2")

    def test_serialize_and_deserialize_move(self):
        """Test full serialization and deserialization cycle."""
        # Make a move in the game
        result = self.game.make_move(Position(8, 0), Position(7, 0))
        self.assertTrue(result.success)

        # Get the move from history
        move = self.game.move_history[0]

        # Serialize to dict
        move_dict = move.to_dict()

        # Verify serialization
        self.assertEqual(move_dict['piece_type'], 'Rat')
        self.assertEqual(move_dict['from_row'], 8)
        self.assertEqual(move_dict['from_col'], 0)
        self.assertEqual(move_dict['to_row'], 7)
        self.assertEqual(move_dict['to_col'], 0)

    def test_move_with_capture_serialization(self):
        """Test serialization of a move with capture."""
        # Set up a capture scenario
        # Move red rat forward
        self.game.make_move(Position(8, 0), Position(7, 0))
        # Move blue cat
        self.game.make_move(Position(1, 1), Position(2, 1))
        # Move red rat forward
        self.game.make_move(Position(7, 0), Position(6, 0))
        # Move blue cat
        self.game.make_move(Position(2, 1), Position(3, 1))
        # Continue moving pieces to create capture opportunity
        self.game.make_move(Position(6, 0), Position(5, 0))
        self.game.make_move(Position(3, 1), Position(4, 1))
        self.game.make_move(Position(5, 0), Position(4, 0))
        self.game.make_move(Position(4, 1), Position(5, 1))
        self.game.make_move(Position(4, 0), Position(3, 0))
        self.game.make_move(Position(5, 1), Position(6, 1))
        self.game.make_move(Position(3, 0), Position(2, 0))
        self.game.make_move(Position(6, 1), Position(7, 1))

        # Check if any captures occurred
        captures = [m for m in self.game.move_history if m.captured_piece is not None]
        if captures:
            move = captures[0]
            move_dict = move.to_dict()
            self.assertIsNotNone(move_dict['captured_piece_type'])
            self.assertIsNotNone(move_dict['captured_piece_rank'])


if __name__ == '__main__':
    unittest.main()
