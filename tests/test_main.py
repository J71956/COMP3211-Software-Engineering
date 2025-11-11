"""
Integration tests for main application entry point.

Tests the complete application flow including startup, initialization,
command-line argument processing, and lifecycle management.
"""

import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
from model.game import Game
from model.position import Position
from controller.game_controller import GameController
from controller.file_manager import FileManager


class TestMainApplication(unittest.TestCase):
    """Test cases for main application entry point."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_parse_arguments_default(self):
        """Test parsing arguments with no options."""
        with patch('sys.argv', ['main.py']):
            args = main.parse_arguments()
            self.assertIsNone(args.load)
            self.assertIsNone(args.replay)
            self.assertIsNone(args.player1)
            self.assertIsNone(args.player2)

    def test_parse_arguments_load(self):
        """Test parsing arguments with --load option."""
        with patch('sys.argv', ['main.py', '--load', 'game.jungle']):
            args = main.parse_arguments()
            self.assertEqual(args.load, 'game.jungle')
            self.assertIsNone(args.replay)

    def test_parse_arguments_replay(self):
        """Test parsing arguments with --replay option."""
        with patch('sys.argv', ['main.py', '--replay', 'game.record']):
            args = main.parse_arguments()
            self.assertEqual(args.replay, 'game.record')
            self.assertIsNone(args.load)

    def test_parse_arguments_player_names(self):
        """Test parsing arguments with player names."""
        with patch('sys.argv', ['main.py', '--player1', 'Alice', '--player2', 'Bob']):
            args = main.parse_arguments()
            self.assertEqual(args.player1, 'Alice')
            self.assertEqual(args.player2, 'Bob')

    def test_initialize_game_new(self):
        """Test initializing a new game."""
        args = MagicMock()
        args.load = None
        args.replay = None

        controller = main.initialize_game(args)
        self.assertIsNotNone(controller)
        self.assertIsInstance(controller, GameController)

    def test_initialize_game_load_success(self):
        """Test initializing game from saved file."""
        # Create a temporary save file
        game = Game("Player 1", "Player 2")
        save_file = os.path.join(self.temp_dir, 'test_game.jungle')

        file_manager = FileManager()
        file_manager.save_game(game, save_file)

        args = MagicMock()
        args.load = save_file
        args.replay = None

        with patch('builtins.print'):
            controller = main.initialize_game(args)
            self.assertIsNotNone(controller)
            self.assertIsInstance(controller, GameController)

    def test_initialize_game_load_failure(self):
        """Test initializing game from non-existent file."""
        args = MagicMock()
        args.load = 'nonexistent.jungle'
        args.replay = None

        with patch('builtins.print'):
            controller = main.initialize_game(args)
            self.assertIsNone(controller)

    def test_initialize_game_replay_failure(self):
        """Test replaying game from non-existent file."""
        args = MagicMock()
        args.load = None
        args.replay = 'nonexistent.record'

        with patch('builtins.print'):
            controller = main.initialize_game(args)
            self.assertIsNone(controller)

    @patch('controller.game_controller.GameController.run_game_loop')
    @patch('builtins.print')
    def test_main_success(self, _mock_print, mock_run_loop):
        """Test successful main execution."""
        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 0)
            mock_run_loop.assert_called_once()

    @patch('main.initialize_game')
    @patch('builtins.print')
    def test_main_initialization_failure(self, _mock_print, mock_init):
        """Test main execution with initialization failure."""
        mock_init.return_value = None

        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 1)

    @patch('controller.game_controller.GameController.run_game_loop')
    @patch('builtins.print')
    def test_main_keyboard_interrupt(self, _mock_print, mock_run_loop):
        """Test main execution with keyboard interrupt."""
        mock_run_loop.side_effect = KeyboardInterrupt()

        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 0)

    @patch('controller.game_controller.GameController.run_game_loop')
    @patch('builtins.print')
    def test_main_unexpected_error(self, _mock_print, mock_run_loop):
        """Test main execution with unexpected error."""
        mock_run_loop.side_effect = Exception("Unexpected error")

        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 1)


class TestApplicationIntegration(unittest.TestCase):
    """Integration tests for complete application flow."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_complete_game_flow(self, _mock_print, mock_input):
        """Test complete game flow from start to quit."""
        # Simulate player name inputs, then quit immediately
        mock_input.side_effect = [
            'Player1',  # Player 1 name
            'Player2',  # Player 2 name
            'quit',     # Quit command
            'y'         # Confirm quit
        ]

        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 0)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_game_with_moves(self, _mock_print, mock_input):
        """Test game flow with some moves."""
        # Simulate player names, a few moves, then quit
        mock_input.side_effect = [
            'Player1',       # Player 1 name
            'Player2',       # Player 2 name
            'move 6,0 5,0',  # Move red lion
            'move 2,6 3,6',  # Move blue lion
            'quit',          # Quit command
            'y'              # Confirm quit
        ]

        with patch('sys.argv', ['main.py']):
            exit_code = main.main()
            self.assertEqual(exit_code, 0)

    def test_save_and_load_integration(self):
        """Test saving and loading a game."""
        save_file = os.path.join(self.temp_dir, 'integration_test.jungle')

        # Create and save a game
        game = Game("Alice", "Bob")
        game.make_move(Position(6, 0), Position(5, 0))  # Make a move

        file_manager = FileManager()
        success = file_manager.save_game(game, save_file)
        self.assertTrue(success)

        # Load the game
        loaded_game = file_manager.load_game(save_file)
        self.assertIsNotNone(loaded_game)
        # Note: move_history is not restored on load (design decision)
        # The board state is restored, which is what matters for continuing play
        self.assertEqual(loaded_game.players[0].name, "Alice")
        self.assertEqual(loaded_game.players[1].name, "Bob")
        # Verify the board state was restored (piece moved from 6,0 to 5,0)
        self.assertIsNone(loaded_game.board.get_piece(Position(6, 0)))
        self.assertIsNotNone(loaded_game.board.get_piece(Position(5, 0)))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_from_command_line(self, _mock_print, mock_input):
        """Test loading a game from command line."""
        # Create a saved game
        save_file = os.path.join(self.temp_dir, 'cmdline_test.jungle')
        game = Game("Player1", "Player2")

        file_manager = FileManager()
        file_manager.save_game(game, save_file)

        # Simulate quitting after loading (no name prompts when loading)
        mock_input.side_effect = ['quit', 'y']

        with patch('sys.argv', ['main.py', '--load', save_file]):
            exit_code = main.main()
            self.assertEqual(exit_code, 0)


if __name__ == '__main__':
    unittest.main()
