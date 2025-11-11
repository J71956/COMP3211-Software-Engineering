"""
Unit tests for GameController class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from controller.game_controller import GameController
from model.game import Game
from model.position import Position
from model.exceptions import GameOverException, FileOperationException


class TestGameController(unittest.TestCase):
    """Test cases for GameController class."""

    def setUp(self):
        """Set up test fixtures."""
        self.controller = GameController()
        self.controller.game = Game("TestPlayer1", "TestPlayer2")

    def test_initialization_without_game(self):
        """Test controller initialization without a game."""
        controller = GameController()
        self.assertIsNone(controller.game)
        self.assertIsNotNone(controller.view)
        self.assertIsNotNone(controller.command_parser)
        self.assertIsNotNone(controller.file_manager)
        self.assertFalse(controller.running)

    def test_initialization_with_game(self):
        """Test controller initialization with an existing game."""
        game = Game("Player1", "Player2")
        controller = GameController(game)
        self.assertEqual(controller.game, game)
        self.assertIsNotNone(controller.view)

    def test_process_command_move_valid(self):
        """Test processing a valid move command."""
        result = self.controller.process_command("a0 b0")
        # The move should fail (no piece at a0 in initial setup), but command should be processed
        self.assertFalse(result)

    def test_process_command_move_with_keyword(self):
        """Test processing a move command with 'move' keyword."""
        result = self.controller.process_command("move a0 b0")
        # Command should be processed even if move fails
        self.assertFalse(result)

    def test_process_command_undo(self):
        """Test processing an undo command."""
        # Make a valid move first
        self.controller.game.make_move(Position(8, 0), Position(7, 0))

        # Now undo
        result = self.controller.process_command("undo")
        self.assertTrue(result)

    def test_process_command_undo_shortcut(self):
        """Test processing undo command with shortcut."""
        # Make a valid move first
        self.controller.game.make_move(Position(8, 0), Position(7, 0))

        # Now undo with shortcut
        result = self.controller.process_command("u")
        self.assertTrue(result)

    def test_process_command_undo_no_moves(self):
        """Test undo command when no moves have been made."""
        result = self.controller.process_command("undo")
        self.assertFalse(result)

    def test_process_command_save(self):
        """Test processing a save command."""
        with patch.object(self.controller.file_manager, 'save_game', return_value=True):
            result = self.controller.process_command("save test.jungle")
            self.assertTrue(result)

    def test_process_command_save_shortcut(self):
        """Test processing save command with shortcut."""
        with patch.object(self.controller.file_manager, 'save_game', return_value=True):
            result = self.controller.process_command("s test.jungle")
            self.assertTrue(result)

    def test_process_command_save_no_filename(self):
        """Test save command without filename."""
        result = self.controller.process_command("save")
        self.assertFalse(result)

    def test_process_command_load(self):
        """Test processing a load command."""
        mock_game = Game("LoadedPlayer1", "LoadedPlayer2")
        with patch.object(self.controller.file_manager, 'load_game', return_value=mock_game):
            result = self.controller.process_command("load test.jungle")
            self.assertTrue(result)
            self.assertEqual(self.controller.game, mock_game)

    def test_process_command_load_shortcut(self):
        """Test processing load command with shortcut."""
        mock_game = Game("LoadedPlayer1", "LoadedPlayer2")
        with patch.object(self.controller.file_manager, 'load_game', return_value=mock_game):
            result = self.controller.process_command("l test.jungle")
            self.assertTrue(result)

    def test_process_command_load_no_filename(self):
        """Test load command without filename."""
        result = self.controller.process_command("load")
        self.assertFalse(result)

    def test_process_command_record(self):
        """Test processing a record command."""
        with patch.object(self.controller.file_manager, 'save_record', return_value=True):
            result = self.controller.process_command("record test.record")
            self.assertTrue(result)

    def test_process_command_record_no_filename(self):
        """Test record command without filename."""
        result = self.controller.process_command("record")
        self.assertFalse(result)

    def test_process_command_replay(self):
        """Test processing a replay command."""
        mock_game = Game("ReplayPlayer1", "ReplayPlayer2")
        with patch.object(self.controller.file_manager, 'replay_record', return_value=mock_game):
            result = self.controller.process_command("replay test.record")
            self.assertTrue(result)
            self.assertEqual(self.controller.game, mock_game)

    def test_process_command_replay_no_filename(self):
        """Test replay command without filename."""
        result = self.controller.process_command("replay")
        self.assertFalse(result)

    def test_process_command_quit(self):
        """Test processing a quit command."""
        self.controller.running = True
        result = self.controller.process_command("quit")
        self.assertTrue(result)
        self.assertFalse(self.controller.running)

    def test_process_command_quit_shortcut(self):
        """Test processing quit command with shortcut."""
        self.controller.running = True
        result = self.controller.process_command("q")
        self.assertTrue(result)
        self.assertFalse(self.controller.running)

    def test_process_command_help(self):
        """Test processing a help command."""
        result = self.controller.process_command("help")
        self.assertTrue(result)

    def test_process_command_help_shortcut(self):
        """Test processing help command with shortcut."""
        result = self.controller.process_command("h")
        self.assertTrue(result)

    def test_process_command_unknown(self):
        """Test processing an unknown command."""
        result = self.controller.process_command("unknown")
        self.assertFalse(result)

    def test_process_command_empty(self):
        """Test processing an empty command."""
        result = self.controller.process_command("")
        self.assertFalse(result)

    def test_handle_move_command_valid_move(self):
        """Test handling a valid move."""
        # Move rat from (8,0) to (7,0)
        result = self.controller._handle_move_command("8,0 7,0")
        self.assertTrue(result)

    def test_handle_move_command_invalid_position(self):
        """Test handling a move with invalid position."""
        result = self.controller._handle_move_command("10,10 11,11")
        self.assertFalse(result)

    def test_handle_move_command_no_piece(self):
        """Test handling a move from empty square."""
        result = self.controller._handle_move_command("4,4 5,5")
        self.assertFalse(result)

    def test_handle_undo_command_success(self):
        """Test successful undo."""
        # Make a move first
        self.controller.game.make_move(Position(8, 0), Position(7, 0))

        # Undo it
        result = self.controller._handle_undo_command()
        self.assertTrue(result)

    def test_handle_undo_command_no_moves(self):
        """Test undo when no moves available."""
        result = self.controller._handle_undo_command()
        self.assertFalse(result)

    def test_handle_save_command_success(self):
        """Test successful save."""
        with patch.object(self.controller.file_manager, 'save_game', return_value=True):
            result = self.controller._handle_save_command(['save', 'test.jungle'])
            self.assertTrue(result)

    def test_handle_save_command_failure(self):
        """Test save failure."""
        with patch.object(self.controller.file_manager, 'save_game',
                          side_effect=FileOperationException("Save failed")):
            result = self.controller._handle_save_command(['save', 'test.jungle'])
            self.assertFalse(result)

    def test_handle_load_command_success(self):
        """Test successful load."""
        mock_game = Game("LoadedPlayer1", "LoadedPlayer2")
        with patch.object(self.controller.file_manager, 'load_game', return_value=mock_game):
            result = self.controller._handle_load_command(['load', 'test.jungle'])
            self.assertTrue(result)
            self.assertEqual(self.controller.game, mock_game)

    def test_handle_load_command_failure(self):
        """Test load failure."""
        with patch.object(self.controller.file_manager, 'load_game',
                          side_effect=FileOperationException("Load failed")):
            result = self.controller._handle_load_command(['load', 'test.jungle'])
            self.assertFalse(result)

    def test_handle_record_command_success(self):
        """Test successful record save."""
        with patch.object(self.controller.file_manager, 'save_record', return_value=True):
            result = self.controller._handle_record_command(['record', 'test.record'])
            self.assertTrue(result)

    def test_handle_replay_command_success(self):
        """Test successful replay."""
        mock_game = Game("ReplayPlayer1", "ReplayPlayer2")
        with patch.object(self.controller.file_manager, 'replay_record', return_value=mock_game):
            result = self.controller._handle_replay_command(['replay', 'test.record'])
            self.assertTrue(result)
            self.assertEqual(self.controller.game, mock_game)

    def test_handle_quit_command_no_game(self):
        """Test quit with no game in progress."""
        self.controller.game = None
        result = self.controller._handle_quit_command()
        self.assertTrue(result)
        self.assertFalse(self.controller.running)

    def test_handle_quit_command_game_over(self):
        """Test quit when game is over."""
        # Force game over
        self.controller.game._game_status = self.controller.game.game_status.__class__.PLAYER_ONE_WINS
        result = self.controller._handle_quit_command()
        self.assertTrue(result)
        self.assertFalse(self.controller.running)


if __name__ == '__main__':
    unittest.main()
