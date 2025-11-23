"""
Unit tests for FileManager class.
Tests save/load functionality for .jungle files.
"""

import unittest
import json
import tempfile
from pathlib import Path

from controller.file_manager import FileManager
from model.game import Game
from model.position import Position
from model.enums import GameStatus
from model.exceptions import FileOperationException


class TestFileManagerSaveLoad(unittest.TestCase):
    """Test cases for FileManager save and load operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_game_creates_file(self):
        """Test that save_game creates a .jungle file."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        result = FileManager.save_game(game, str(filepath))

        self.assertTrue(result)
        self.assertTrue(filepath.exists())

    def test_save_game_adds_extension(self):
        """Test that save_game adds .jungle extension if missing."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game"

        FileManager.save_game(game, str(filepath))

        jungle_file = self.temp_path / "test_game.jungle"
        self.assertTrue(jungle_file.exists())

    def test_save_game_valid_json(self):
        """Test that saved file contains valid JSON."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn('version', data)
        self.assertIn('players', data)
        self.assertIn('board_state', data)

    def test_save_game_includes_player_info(self):
        """Test that saved game includes player information."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data['players']), 2)
        self.assertEqual(data['players'][0]['name'], "Alice")
        self.assertEqual(data['players'][1]['name'], "Bob")
        self.assertEqual(data['players'][0]['color'], "red")
        self.assertEqual(data['players'][1]['color'], "blue")

    def test_save_game_includes_board_state(self):
        """Test that saved game includes board state with pieces."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Should have 16 pieces (8 per player)
        self.assertEqual(len(data['board_state']), 16)

        # Check a specific piece (Red Rat at 8,0)
        self.assertIn('8,0', data['board_state'])
        rat_data = data['board_state']['8,0']
        self.assertEqual(rat_data['piece'], 'Rat')
        self.assertEqual(rat_data['owner'], 'red')
        self.assertEqual(rat_data['rank'], 1)

    def test_save_game_includes_current_player(self):
        """Test that saved game includes current player index."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['current_player'], 0)

    def test_save_game_includes_game_status(self):
        """Test that saved game includes game status."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['game_status'], 'ongoing')

    def test_load_game_file_not_found(self):
        """Test that load_game raises exception for non-existent file."""
        filepath = self.temp_path / "nonexistent.jungle"

        with self.assertRaises(FileOperationException) as context:
            FileManager.load_game(str(filepath))

        self.assertIn("File not found", str(context.exception))

    def test_load_game_invalid_extension(self):
        """Test that load_game raises exception for wrong file extension."""
        filepath = self.temp_path / "test.txt"
        filepath.write_text("test")

        with self.assertRaises(FileOperationException) as context:
            FileManager.load_game(str(filepath))

        self.assertIn("Invalid file extension", str(context.exception))

    def test_load_game_invalid_json(self):
        """Test that load_game raises exception for invalid JSON."""
        filepath = self.temp_path / "test.jungle"
        filepath.write_text("not valid json")

        with self.assertRaises(FileOperationException) as context:
            FileManager.load_game(str(filepath))

        self.assertIn("Invalid JSON", str(context.exception))

    def test_load_game_restores_players(self):
        """Test that load_game restores player information."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        self.assertIsNotNone(loaded_game)
        self.assertEqual(len(loaded_game.players), 2)
        self.assertEqual(loaded_game.players[0].name, "Alice")
        self.assertEqual(loaded_game.players[1].name, "Bob")

    def test_load_game_restores_board_state(self):
        """Test that load_game restores board state with pieces."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        # Check that pieces are restored
        rat_pos = Position(8, 0)
        piece = loaded_game.board.get_piece(rat_pos)
        self.assertIsNotNone(piece)
        self.assertEqual(piece.__class__.__name__, 'Rat')
        self.assertEqual(piece.rank, 1)
        self.assertEqual(piece.owner.name, "Alice")

    def test_load_game_restores_current_player(self):
        """Test that load_game restores current player."""
        game = Game("Alice", "Bob")
        # Make a move to change current player
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.jungle"
        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        self.assertEqual(loaded_game.current_player_index, 1)
        self.assertEqual(loaded_game.get_current_player().name, "Bob")

    def test_load_game_restores_game_status(self):
        """Test that load_game restores game status."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        self.assertEqual(loaded_game.game_status, GameStatus.ONGOING)

    def test_save_and_load_after_moves(self):
        """Test save and load after making several moves."""
        game = Game("Alice", "Bob")

        # Make some moves
        game.make_move(Position(8, 0), Position(7, 0))  # Red Rat
        game.make_move(Position(0, 6), Position(1, 6))  # Blue Rat

        filepath = self.temp_path / "test_game.jungle"
        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        # Verify pieces moved
        self.assertIsNone(loaded_game.board.get_piece(Position(8, 0)))
        self.assertIsNotNone(loaded_game.board.get_piece(Position(7, 0)))
        self.assertIsNone(loaded_game.board.get_piece(Position(0, 6)))
        self.assertIsNotNone(loaded_game.board.get_piece(Position(1, 6)))

    def test_save_creates_backup(self):
        """Test that saving over existing file creates backup."""
        game = Game("Alice", "Bob")
        filepath = self.temp_path / "test_game.jungle"

        # Save first time
        FileManager.save_game(game, str(filepath))
        first_content = filepath.read_text()

        # Make a move and save again
        game.make_move(Position(8, 0), Position(7, 0))
        FileManager.save_game(game, str(filepath))

        # Backup should have been created and removed
        backup_path = self.temp_path / "test_game.jungle.bak"
        self.assertFalse(backup_path.exists())

        # New file should be different
        second_content = filepath.read_text()
        self.assertNotEqual(first_content, second_content)


if __name__ == '__main__':
    unittest.main()



class TestFileManagerRecord(unittest.TestCase):
    """Test cases for FileManager record operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_record_creates_file(self):
        """Test that save_record creates a .record file."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        result = FileManager.save_record(game, str(filepath))

        self.assertTrue(result)
        self.assertTrue(filepath.exists())

    def test_save_record_adds_extension(self):
        """Test that save_record adds .record extension if missing."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game"
        FileManager.save_record(game, str(filepath))

        record_file = self.temp_path / "test_game.record"
        self.assertTrue(record_file.exists())

    def test_save_record_includes_header(self):
        """Test that record file includes proper header."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        content = filepath.read_text()
        self.assertIn("JUNGLE_GAME_RECORD_V1.0", content)
        self.assertIn("Players: Alice (Red), Bob (Blue)", content)
        self.assertIn("Start Time:", content)

    def test_save_record_includes_moves(self):
        """Test that record file includes move history."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))  # Red Rat
        game.make_move(Position(0, 6), Position(1, 6))  # Blue Rat

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        content = filepath.read_text()
        self.assertIn("Move 1:", content)
        self.assertIn("Move 2:", content)
        self.assertIn("Rat", content)

    def test_save_record_includes_game_result_ongoing(self):
        """Test that record includes 'In Progress' for ongoing games."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        content = filepath.read_text()
        self.assertIn("Game Result: In Progress", content)

    def test_load_record_file_not_found(self):
        """Test that load_record raises exception for non-existent file."""
        filepath = self.temp_path / "nonexistent.record"

        with self.assertRaises(FileOperationException) as context:
            FileManager.load_record(str(filepath))

        self.assertIn("File not found", str(context.exception))

    def test_load_record_invalid_extension(self):
        """Test that load_record raises exception for wrong file extension."""
        filepath = self.temp_path / "test.txt"
        filepath.write_text("test")

        with self.assertRaises(FileOperationException) as context:
            FileManager.load_record(str(filepath))

        self.assertIn("Invalid file extension", str(context.exception))

    def test_load_record_returns_moves(self):
        """Test that load_record returns list of move dictionaries."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))
        game.make_move(Position(0, 6), Position(1, 6))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        moves = FileManager.load_record(str(filepath))

        self.assertIsNotNone(moves)
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0]['piece_type'], 'Rat')
        self.assertEqual(moves[0]['from_row'], 8)
        self.assertEqual(moves[0]['from_col'], 0)

    def test_replay_record_creates_game(self):
        """Test that replay_record creates a game instance."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        replayed_game = FileManager.replay_record(str(filepath))

        self.assertIsNotNone(replayed_game)
        self.assertIsInstance(replayed_game, Game)

    def test_replay_record_restores_player_names(self):
        """Test that replay_record restores player names from file."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        replayed_game = FileManager.replay_record(str(filepath))

        self.assertEqual(replayed_game.players[0].name, "Alice")
        self.assertEqual(replayed_game.players[1].name, "Bob")

    def test_replay_record_executes_moves(self):
        """Test that replay_record executes all moves."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))  # Red Rat
        game.make_move(Position(0, 6), Position(1, 6))  # Blue Rat

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        replayed_game = FileManager.replay_record(str(filepath))

        # Verify pieces moved
        self.assertIsNone(replayed_game.board.get_piece(Position(8, 0)))
        self.assertIsNotNone(replayed_game.board.get_piece(Position(7, 0)))
        self.assertIsNone(replayed_game.board.get_piece(Position(0, 6)))
        self.assertIsNotNone(replayed_game.board.get_piece(Position(1, 6)))

    def test_replay_record_maintains_turn_order(self):
        """Test that replay_record maintains correct turn order."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))  # Red move
        game.make_move(Position(0, 6), Position(1, 6))  # Blue move

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        replayed_game = FileManager.replay_record(str(filepath))

        # After 2 moves (Red, Blue), it should be Red's turn again
        self.assertEqual(replayed_game.current_player_index, 0)
        self.assertEqual(replayed_game.get_current_player().name, "Alice")

    def test_replay_record_with_custom_names(self):
        """Test that replay_record can use custom player names."""
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))

        filepath = self.temp_path / "test_game.record"
        FileManager.save_record(game, str(filepath))

        replayed_game = FileManager.replay_record(
            str(filepath),
            player1_name="Charlie",
            player2_name="Diana"
        )

        self.assertEqual(replayed_game.players[0].name, "Charlie")
        self.assertEqual(replayed_game.players[1].name, "Diana")


