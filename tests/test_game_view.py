"""
Unit tests for GameView class.
Tests view formatting and display logic for various game states.
"""

import unittest
from model.game import Game
from model.move import MoveResult
from model.position import Position
from view.game_view import GameView


class TestGameView(unittest.TestCase):
    """Test cases for GameView class."""

    def setUp(self):
        """Set up test fixtures."""
        self.view = GameView()
        self.game = Game("Alice", "Bob")

    def test_initialization(self):
        """Test GameView initializes with BoardRenderer."""
        self.assertIsNotNone(self.view.board_renderer)

    def test_display_game_state_initial(self):
        """Test displaying initial game state."""
        result = self.view.display_game_state(self.game)

        # Check for game header
        self.assertIn("JUNGLE GAME", result)

        # Check for player information
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)

        # Check for current turn
        self.assertIn("Current Turn", result)

        # Check for board rendering
        self.assertIn("|", result)  # Board borders

        # Check for undo status
        self.assertIn("Undo", result)

    def test_display_game_state_with_moves(self):
        """Test displaying game state after moves have been made."""
        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        result = self.view.display_game_state(self.game)

        # Check for move history section
        self.assertIn("Recent Moves", result)

        # Check that the move appears
        self.assertIn("Rat", result)

    def test_format_game_status_ongoing(self):
        """Test formatting game status for ongoing game."""
        result = self.view._format_game_status(self.game)

        # Check for players
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)

        # Check for current turn
        self.assertIn("Current Turn", result)

        # Check for piece counts
        self.assertIn("Pieces Remaining", result)
        self.assertIn("8", result)  # Each player starts with 8 pieces



    def test_format_move_history_empty(self):
        """Test formatting move history when no moves made."""
        # Create a new game with no moves
        result = self.view._format_move_history(self.game)

        # Should show header but no moves
        self.assertIn("Recent Moves", result)

    def test_format_move_history_with_moves(self):
        """Test formatting move history with moves."""
        # Make several moves
        self.game.make_move(Position(8, 0), Position(7, 0))  # Red rat up
        self.game.make_move(Position(0, 6), Position(1, 6))  # Blue rat down
        self.game.make_move(Position(8, 2), Position(7, 2))  # Red leopard up

        result = self.view._format_move_history(self.game)

        # Check for move history header
        self.assertIn("Recent Moves", result)

        # Check for move numbers
        self.assertIn("1.", result)
        self.assertIn("2.", result)
        self.assertIn("3.", result)

        # Check for player names
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)

    def test_format_move_history_max_recent_moves(self):
        """Test that move history limits display to recent moves."""
        # Make more than 5 moves
        moves = [
            (Position(8, 0), Position(7, 0)),  # 1. Red rat up
            (Position(0, 6), Position(1, 6)),  # 2. Blue rat down
            (Position(8, 2), Position(7, 2)),  # 3. Red leopard up
            (Position(0, 4), Position(1, 4)),  # 4. Blue leopard down
            (Position(8, 4), Position(7, 4)),  # 5. Red wolf up
            (Position(0, 2), Position(1, 2)),  # 6. Blue wolf down
            (Position(8, 6), Position(7, 6)),  # 7. Red elephant up
        ]

        for from_pos, to_pos in moves:
            self.game.make_move(from_pos, to_pos)

        result = self.view._format_move_history(self.game, max_recent_moves=5)

        # Should show only last 5 moves (3-7)
        self.assertIn("3.", result)
        self.assertIn("7.", result)

        # Should indicate earlier moves exist
        self.assertIn("earlier moves", result)

    def test_display_welcome_message(self):
        """Test welcome message display."""
        result = self.view.display_welcome_message()

        # Check for welcome header
        self.assertIn("WELCOME TO JUNGLE GAME", result)

        # Check for game description
        self.assertIn("strategic", result)

        # Check for terrain legend
        self.assertIn("Terrain Legend", result)
        self.assertIn("Land", result)
        self.assertIn("Water", result)

        # Check for commands
        self.assertIn("Commands", result)
        self.assertIn("move", result)
        self.assertIn("undo", result)
        self.assertIn("save", result)



    def test_display_move_result_success(self):
        """Test displaying successful move result."""
        result = MoveResult(True, "Rat moved from (8,0) to (7,0)")
        display = self.view.display_move_result(result)

        self.assertIn("✓", display)
        self.assertIn("Rat moved", display)

    def test_display_move_result_failure(self):
        """Test displaying failed move result."""
        result = MoveResult(False, "Invalid move")
        display = self.view.display_move_result(result)

        self.assertIn("✗", display)
        self.assertIn("Invalid move", display)

    def test_display_error(self):
        """Test error message display."""
        result = self.view.display_error("Something went wrong")

        self.assertIn("ERROR", result)
        self.assertIn("Something went wrong", result)

    def test_display_info(self):
        """Test info message display."""
        result = self.view.display_info("Game saved successfully")

        self.assertIn("INFO", result)
        self.assertIn("Game saved successfully", result)

    def test_display_undo_result_success(self):
        """Test displaying successful undo result."""
        result = self.view.display_undo_result(True)

        self.assertIn("✓", result)
        self.assertIn("undone successfully", result)

    def test_display_undo_result_failure(self):
        """Test displaying failed undo result."""
        result = self.view.display_undo_result(False)

        self.assertIn("✗", result)
        self.assertIn("No moves to undo", result)

    def test_display_game_state_shows_piece_counts(self):
        """Test that game state display shows piece counts."""
        result = self.view.display_game_state(self.game)

        # Should show piece counts for both players
        self.assertIn("Pieces Remaining", result)
        self.assertIn("Alice=8", result)
        self.assertIn("Bob=8", result)

    def test_display_game_state_after_capture(self):
        """Test game state display after a piece is captured."""
        # Set up a capture scenario
        # Move red rat to capture blue rat
        self.game.board.set_piece(Position(0, 6), None)  # Remove blue rat
        self.game.board.set_piece(Position(1, 6), self.game.board.get_piece(Position(0, 6)))

        # Move red rat up and capture
        self.game.make_move(Position(8, 0), Position(7, 0))
        self.game.make_move(Position(0, 0), Position(1, 0))  # Blue elephant
        self.game.make_move(Position(7, 0), Position(8, 0))

        result = self.view.display_game_state(self.game)

        # Piece counts should be updated
        self.assertIn("Pieces Remaining", result)

    def test_display_game_state_undo_available(self):
        """Test that game state shows undo availability."""
        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        result = self.view.display_game_state(self.game)

        # Should show undo is available
        self.assertIn("Undo available", result)
        self.assertIn("1 move(s) can be undone", result)

    def test_display_game_state_undo_not_available(self):
        """Test that game state shows when undo is not available."""
        result = self.view.display_game_state(self.game)

        # Should show undo is not available
        self.assertIn("Undo not available", result)

    def test_game_view_returns_strings(self):
        """Test that all display methods return strings."""
        # Test all display methods return strings
        self.assertIsInstance(self.view.display_game_state(self.game), str)
        self.assertIsInstance(self.view.display_welcome_message(), str)
        self.assertIsInstance(self.view.display_error("test"), str)
        self.assertIsInstance(self.view.display_info("test"), str)
        self.assertIsInstance(self.view.display_undo_result(True), str)

        result = MoveResult(True, "test")
        self.assertIsInstance(self.view.display_move_result(result), str)


if __name__ == '__main__':
    unittest.main()
