"""
Unit tests for GameState class.
"""

import unittest
from model.game_state import GameState
from model.board import Board
from model.player import Player
from model.position import Position
from model.enums import PlayerColor
from model.piece import Cat, Dog, Rat


class TestGameState(unittest.TestCase):
    """Test cases for GameState class."""

    def setUp(self):
        """Set up test fixtures."""
        self.player1 = Player("Player 1", PlayerColor.RED)
        self.player2 = Player("Player 2", PlayerColor.BLUE)
        self.board = Board()

    def test_game_state_creation(self):
        """Test creating a game state with board state, player index, and move count."""
        board_state = {}
        game_state = GameState(board_state, 0, 5)

        self.assertEqual(game_state.current_player_index, 0)
        self.assertEqual(game_state.move_count, 5)
        self.assertEqual(len(game_state.board_state), 0)

    def test_game_state_properties_are_read_only(self):
        """Test that game state properties cannot be modified."""
        board_state = {}
        game_state = GameState(board_state, 0, 5)

        # Properties should not be modifiable
        with self.assertRaises(AttributeError):
            game_state.current_player_index = 1

        with self.assertRaises(AttributeError):
            game_state.move_count = 10

    def test_board_state_property_returns_copy(self):
        """Test that board_state property returns a copy."""
        cat = Cat(self.player1, Position(3, 3))
        board_state = {Position(3, 3): cat}
        game_state = GameState(board_state, 0, 0)

        state1 = game_state.board_state
        state2 = game_state.board_state

        # Should be equal but not the same object
        self.assertEqual(state1, state2)
        self.assertIsNot(state1, state2)

    def test_capture_from_empty_board(self):
        """Test capturing state from an empty board."""
        game_state = GameState.capture_from_board(self.board, 0, 0)

        self.assertEqual(game_state.current_player_index, 0)
        self.assertEqual(game_state.move_count, 0)
        self.assertEqual(len(game_state.board_state), 0)

    def test_capture_from_board_with_pieces(self):
        """Test capturing state from a board with pieces."""
        cat = Cat(self.player1, Position(3, 3))
        dog = Dog(self.player2, Position(4, 4))

        self.board.set_piece(Position(3, 3), cat)
        self.board.set_piece(Position(4, 4), dog)

        game_state = GameState.capture_from_board(self.board, 1, 10)

        self.assertEqual(game_state.current_player_index, 1)
        self.assertEqual(game_state.move_count, 10)
        self.assertEqual(len(game_state.board_state), 2)
        self.assertEqual(game_state.board_state[Position(3, 3)], cat)
        self.assertEqual(game_state.board_state[Position(4, 4)], dog)

    def test_restore_to_empty_board(self):
        """Test restoring an empty state to a board."""
        board_state = {}
        game_state = GameState(board_state, 0, 0)

        game_state.restore_to_board(self.board)

        # Board should be empty
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                self.assertIsNone(self.board.get_piece(Position(row, col)))

    def test_restore_to_board_with_pieces(self):
        """Test restoring a state with pieces to a board."""
        cat = Cat(self.player1, Position(3, 3))
        dog = Dog(self.player2, Position(4, 4))

        board_state = {
            Position(3, 3): cat,
            Position(4, 4): dog
        }
        game_state = GameState(board_state, 0, 0)

        game_state.restore_to_board(self.board)

        # Check that pieces are restored
        self.assertEqual(self.board.get_piece(Position(3, 3)), cat)
        self.assertEqual(self.board.get_piece(Position(4, 4)), dog)

        # Check that other positions are empty
        self.assertIsNone(self.board.get_piece(Position(0, 0)))
        self.assertIsNone(self.board.get_piece(Position(5, 5)))

    def test_restore_updates_piece_positions(self):
        """Test that restoring updates piece positions correctly."""
        cat = Cat(self.player1, Position(2, 2))

        board_state = {Position(3, 3): cat}
        game_state = GameState(board_state, 0, 0)

        game_state.restore_to_board(self.board)

        # Piece position should be updated to match the saved state
        self.assertEqual(cat.position, Position(3, 3))
        self.assertEqual(self.board.get_piece(Position(3, 3)), cat)

    def test_capture_and_restore_round_trip(self):
        """Test that capturing and restoring preserves the board state."""
        cat = Cat(self.player1, Position(3, 3))
        dog = Dog(self.player2, Position(4, 4))
        rat = Rat(self.player1, Position(5, 5))

        self.board.set_piece(Position(3, 3), cat)
        self.board.set_piece(Position(4, 4), dog)
        self.board.set_piece(Position(5, 5), rat)

        # Capture state
        game_state = GameState.capture_from_board(self.board, 1, 15)

        # Clear board
        self.board.set_piece(Position(3, 3), None)
        self.board.set_piece(Position(4, 4), None)
        self.board.set_piece(Position(5, 5), None)

        # Verify board is empty
        self.assertIsNone(self.board.get_piece(Position(3, 3)))
        self.assertIsNone(self.board.get_piece(Position(4, 4)))
        self.assertIsNone(self.board.get_piece(Position(5, 5)))

        # Restore state
        game_state.restore_to_board(self.board)

        # Verify pieces are restored
        self.assertEqual(self.board.get_piece(Position(3, 3)), cat)
        self.assertEqual(self.board.get_piece(Position(4, 4)), dog)
        self.assertEqual(self.board.get_piece(Position(5, 5)), rat)

    def test_game_state_equality(self):
        """Test game state equality comparison."""
        cat = Cat(self.player1, Position(3, 3))

        board_state1 = {Position(3, 3): cat}
        board_state2 = {Position(3, 3): cat}
        board_state3 = {}

        state1 = GameState(board_state1, 0, 5)
        state2 = GameState(board_state2, 0, 5)
        state3 = GameState(board_state3, 0, 5)
        state4 = GameState(board_state1, 1, 5)
        state5 = GameState(board_state1, 0, 10)

        # Same board state, player index, and move count should be equal
        self.assertEqual(state1, state2)

        # Different board state should not be equal
        self.assertNotEqual(state1, state3)

        # Different player index should not be equal
        self.assertNotEqual(state1, state4)

        # Different move count should not be equal
        self.assertNotEqual(state1, state5)

    def test_game_state_repr(self):
        """Test developer-friendly representation."""
        cat = Cat(self.player1, Position(3, 3))
        board_state = {Position(3, 3): cat}
        game_state = GameState(board_state, 1, 20)

        state_repr = repr(game_state)

        self.assertIn("GameState", state_repr)
        self.assertIn("current_player=1", state_repr)
        self.assertIn("move_count=20", state_repr)
        self.assertIn("pieces=1", state_repr)

    def test_restore_clears_existing_pieces(self):
        """Test that restore clears existing pieces before restoring."""
        cat = Cat(self.player1, Position(3, 3))
        dog = Dog(self.player2, Position(4, 4))
        rat = Rat(self.player1, Position(5, 5))

        # Set up initial board state
        self.board.set_piece(Position(3, 3), cat)
        self.board.set_piece(Position(4, 4), dog)

        # Create a state with only the rat
        board_state = {Position(5, 5): rat}
        game_state = GameState(board_state, 0, 0)

        # Restore should clear cat and dog, and place only rat
        game_state.restore_to_board(self.board)

        self.assertIsNone(self.board.get_piece(Position(3, 3)))
        self.assertIsNone(self.board.get_piece(Position(4, 4)))
        self.assertEqual(self.board.get_piece(Position(5, 5)), rat)

    def test_multiple_captures_are_independent(self):
        """Test that multiple captures create independent states."""
        cat = Cat(self.player1, Position(3, 3))
        self.board.set_piece(Position(3, 3), cat)

        # Capture first state
        state1 = GameState.capture_from_board(self.board, 0, 5)

        # Move piece and capture second state
        self.board.set_piece(Position(3, 3), None)
        self.board.set_piece(Position(4, 4), cat)
        cat.position = Position(4, 4)

        state2 = GameState.capture_from_board(self.board, 1, 6)

        # States should be different
        self.assertNotEqual(state1, state2)
        self.assertEqual(len(state1.board_state), 1)
        self.assertEqual(len(state2.board_state), 1)
        self.assertIn(Position(3, 3), state1.board_state)
        self.assertIn(Position(4, 4), state2.board_state)


if __name__ == '__main__':
    unittest.main()
