"""
Integration tests for complete game scenarios.
Tests end-to-end game flows, save/load/record functionality, and complex move sequences.
"""

import unittest
import tempfile
from pathlib import Path

from model.game import Game
from model.position import Position
from controller.file_manager import FileManager




class TestSaveLoadIntegration(unittest.TestCase):
    """Test save/load functionality integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_load_mid_game(self):
        """Test saving and loading a game in progress."""
        # Create game and make several moves
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))
        game.make_move(Position(0, 6), Position(1, 6))
        game.make_move(Position(8, 6), Position(7, 6))

        # Save game
        filepath = self.temp_path / "test_save.jungle"
        FileManager.save_game(game, str(filepath))

        # Load game
        loaded_game = FileManager.load_game(str(filepath))

        # Verify game state matches
        self.assertEqual(loaded_game.current_player_index, game.current_player_index)
        self.assertEqual(loaded_game.players[0].name, "Alice")
        self.assertEqual(loaded_game.players[1].name, "Bob")

        # Verify board state matches
        for row in range(9):
            for col in range(7):
                pos = Position(row, col)
                original_piece = game.board.get_piece(pos)
                loaded_piece = loaded_game.board.get_piece(pos)

                if original_piece is None:
                    self.assertIsNone(loaded_piece)
                else:
                    self.assertIsNotNone(loaded_piece)
                    self.assertEqual(
                        original_piece.__class__.__name__,
                        loaded_piece.__class__.__name__
                    )

    def test_save_load_continue_playing(self):
        """Test that loaded game can continue playing."""
        # Create game and make moves
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))
        game.make_move(Position(0, 6), Position(1, 6))

        # Save and load
        filepath = self.temp_path / "continue_game.jungle"
        FileManager.save_game(game, str(filepath))
        loaded_game = FileManager.load_game(str(filepath))

        # Continue playing
        result = loaded_game.make_move(Position(8, 6), Position(7, 6))
        self.assertTrue(result.success)

        # Verify piece moved
        self.assertIsNone(loaded_game.board.get_piece(Position(8, 6)))
        self.assertIsNotNone(loaded_game.board.get_piece(Position(7, 6)))


class TestRecordIntegration(unittest.TestCase):
    """Test record functionality integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_record_and_replay_game(self):
        """Test recording and replaying a complete game."""
        # Create game and make simple moves
        game = Game("Alice", "Bob")
        moves = [
            (Position(8, 6), Position(8, 5)),  # Red elephant left
            (Position(0, 0), Position(0, 1)),  # Blue elephant right
            (Position(8, 5), Position(8, 5)),  # Red elephant up
            (Position(0, 1), Position(1, 1)),  # Blue elephant down (captures blue cat)
        ]

        for from_pos, to_pos in moves:
            game.make_move(from_pos, to_pos)

        # Save record
        filepath = self.temp_path / "test_record.record"
        FileManager.save_record(game, str(filepath))

        # Replay record
        replayed_game = FileManager.replay_record(str(filepath))

        # Verify final board state matches
        for row in range(9):
            for col in range(7):
                pos = Position(row, col)
                original_piece = game.board.get_piece(pos)
                replayed_piece = replayed_game.board.get_piece(pos)

                if original_piece is None:
                    self.assertIsNone(replayed_piece)
                else:
                    self.assertIsNotNone(replayed_piece)
                    self.assertEqual(
                        original_piece.__class__.__name__,
                        replayed_piece.__class__.__name__
                    )

    def test_record_with_captures(self):
        """Test recording and replaying game with captures."""
        game = Game("Player1", "Player2")

        # Set up a capture (elephant captures cat)
        game.make_move(Position(8, 6), Position(7, 6))  # Red elephant up
        game.make_move(Position(0, 0), Position(0, 1))  # Blue elephant right
        game.make_move(Position(7, 6), Position(7, 5))  # Red elephant left
        game.make_move(Position(0, 1), Position(1, 1))  # Blue elephant down (captures blue cat)

        # Save and replay
        filepath = self.temp_path / "capture_record.record"
        FileManager.save_record(game, str(filepath))
        replayed_game = FileManager.replay_record(str(filepath))

        # Verify capture occurred in replay
        self.assertIsNone(replayed_game.board.get_piece(Position(0, 1)))
        self.assertIsNotNone(replayed_game.board.get_piece(Position(1, 1)))


class TestComplexMoveSequences(unittest.TestCase):
    """Test complex move sequences and edge cases."""

    def test_rat_water_movement_sequence(self):
        """Test rat moving through water."""
        game = Game()

        # Move pieces sideways to clear paths
        game.make_move(Position(6, 0), Position(6, 1))  # Red lion right
        game.make_move(Position(2, 6), Position(2, 5))  # Blue lion left
        game.make_move(Position(7, 1), Position(7, 0))  # Red dog left
        game.make_move(Position(1, 5), Position(1, 6))  # Blue dog right

        # Move red rat up column 1
        game.make_move(Position(8, 0), Position(8, 1))  # Red rat right
        game.make_move(Position(2, 5), Position(2, 4))  # Blue lion left
        game.make_move(Position(8, 1), Position(7, 1))  # Red rat up
        game.make_move(Position(2, 4), Position(2, 3))  # Blue lion left
        game.make_move(Position(7, 1), Position(6, 1))  # Red rat up (captures red lion)
        game.make_move(Position(2, 3), Position(3, 3))  # Blue lion down
        game.make_move(Position(6, 1), Position(5, 1))  # Red rat up

        # Red rat enters water at (4,1)
        game.make_move(Position(3, 3), Position(4, 3))  # Blue lion down
        game.make_move(Position(5, 1), Position(4, 1))  # Red rat into water
        self.assertTrue(game.board.is_water(Position(4, 1)))
        self.assertIsNotNone(game.board.get_piece(Position(4, 1)))

        # Continue in water
        game.make_move(Position(4, 3), Position(5, 3))  # Blue lion down
        game.make_move(Position(4, 1), Position(4, 2))  # Red rat moves in water
        self.assertTrue(game.board.is_water(Position(4, 2)))

    def test_lion_river_jump_sequence(self):
        """Test lion jumping over river vertically."""
        game = Game()

        # Position blue lion to jump vertically over water in column 1
        # Water is at rows 3,4,5 in column 1
        # Move blue cat out of the way first
        game.make_move(Position(6, 0), Position(5, 0))  # Red lion up
        game.make_move(Position(1, 1), Position(1, 0))  # Blue cat left
        game.make_move(Position(5, 0), Position(4, 0))  # Red lion up
        game.make_move(Position(1, 0), Position(2, 0))  # Blue cat down (captures blue tiger)

        # Move blue lion to column 1 for vertical jump
        game.make_move(Position(4, 0), Position(3, 0))  # Red lion up
        game.make_move(Position(2, 6), Position(2, 5))  # Blue lion left
        game.make_move(Position(3, 0), Position(2, 0))  # Red lion up (captures blue cat)
        game.make_move(Position(2, 5), Position(2, 4))  # Blue lion left
        game.make_move(Position(2, 0), Position(1, 0))  # Red lion up
        game.make_move(Position(2, 4), Position(2, 3))  # Blue lion left
        game.make_move(Position(1, 0), Position(0, 0))  # Red lion up (captures blue elephant)
        game.make_move(Position(2, 3), Position(2, 2))  # Blue lion left
        game.make_move(Position(0, 0), Position(0, 1))  # Red lion right
        game.make_move(Position(2, 2), Position(2, 1))  # Blue lion left

        # Blue lion at (2,1) jumps vertically to (6,1) over water at (3,1), (4,1), (5,1)
        game.make_move(Position(0, 1), Position(1, 1))  # Red lion down
        game.make_move(Position(2, 1), Position(6, 1))  # Blue lion jumps vertically!

        self.assertIsNone(game.board.get_piece(Position(2, 1)))
        self.assertIsNotNone(game.board.get_piece(Position(6, 1)))

    def test_trap_capture_sequence(self):
        """Test capturing pieces in traps."""
        game = Game()

        # Simple test: verify trap detection and piece movement into traps
        game.make_move(Position(7, 5), Position(7, 4))  # Red cat left (into red trap at 7,4)
        self.assertTrue(game.board.is_trap(Position(7, 4), game.players[0]))  # Red trap
        self.assertIsNotNone(game.board.get_piece(Position(7, 4)))  # Cat is in trap

        game.make_move(Position(1, 1), Position(1, 2))  # Blue cat right (into blue trap at 1,2)
        self.assertTrue(game.board.is_trap(Position(1, 2), game.players[1]))  # Blue trap
        self.assertIsNotNone(game.board.get_piece(Position(1, 2)))  # Cat is in trap

        # Move pieces out of traps
        game.make_move(Position(7, 4), Position(7, 3))  # Red cat left (out of trap)
        self.assertIsNone(game.board.get_piece(Position(7, 4)))

        game.make_move(Position(1, 2), Position(1, 3))  # Blue cat right (out of trap)
        self.assertIsNone(game.board.get_piece(Position(1, 2)))

    def test_multiple_undo_sequence(self):
        """Test multiple undo operations."""
        game = Game()

        # Make several moves along clear paths
        game.make_move(Position(6, 0), Position(5, 0))  # Red lion up
        game.make_move(Position(2, 0), Position(3, 0))  # Blue tiger down
        game.make_move(Position(5, 0), Position(4, 0))  # Red lion up

        # Undo moves
        self.assertTrue(game.can_undo())
        game.undo_move()
        self.assertIsNotNone(game.board.get_piece(Position(5, 0)))
        self.assertIsNone(game.board.get_piece(Position(4, 0)))

        game.undo_move()
        self.assertIsNone(game.board.get_piece(Position(3, 0)))
        self.assertIsNotNone(game.board.get_piece(Position(2, 0)))

        game.undo_move()
        self.assertIsNone(game.board.get_piece(Position(5, 0)))
        self.assertIsNotNone(game.board.get_piece(Position(6, 0)))

        # No more undos available
        self.assertFalse(game.can_undo())


class TestSaveLoadRecordCombination(unittest.TestCase):
    """Test combinations of save, load, and record operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_load_then_record(self):
        """Test saving, loading, then creating a record."""
        # Create game and make moves
        game = Game("Alice", "Bob")
        game.make_move(Position(8, 0), Position(7, 0))
        game.make_move(Position(0, 6), Position(1, 6))

        # Save game
        save_path = self.temp_path / "game.jungle"
        FileManager.save_game(game, str(save_path))

        # Load game
        loaded_game = FileManager.load_game(str(save_path))

        # Continue playing
        loaded_game.make_move(Position(6, 0), Position(5, 0))  # Red lion up
        loaded_game.make_move(Position(2, 0), Position(3, 0))  # Blue tiger down

        # Create record
        record_path = self.temp_path / "game.record"
        FileManager.save_record(loaded_game, str(record_path))

        # Verify record was created
        self.assertTrue(record_path.exists())

    def test_replay_then_save(self):
        """Test replaying a record then saving the game."""
        # Create original game
        game = Game("Player1", "Player2")
        game.make_move(Position(8, 0), Position(7, 0))
        game.make_move(Position(0, 6), Position(1, 6))

        # Save record
        record_path = self.temp_path / "original.record"
        FileManager.save_record(game, str(record_path))

        # Replay record
        replayed_game = FileManager.replay_record(str(record_path))

        # Continue playing
        replayed_game.make_move(Position(6, 0), Position(5, 0))  # Red lion up

        # Save the replayed game
        save_path = self.temp_path / "replayed.jungle"
        result = FileManager.save_game(replayed_game, str(save_path))

        self.assertTrue(result)
        self.assertTrue(save_path.exists())


if __name__ == '__main__':
    unittest.main()
