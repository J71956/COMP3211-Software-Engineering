"""
Unit tests for Board class.
Tests board initialization, piece management, and terrain detection.
"""

import unittest
from model.board import Board
from model.position import Position
from model.enums import TerrainType, PlayerColor
from model.player import Player


class TestBoardInitialization(unittest.TestCase):
    """Test board initialization and basic properties."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_board_dimensions(self):
        """Test that board has correct dimensions."""
        self.assertEqual(Board.BOARD_HEIGHT, 9)
        self.assertEqual(Board.BOARD_WIDTH, 7)

    def test_board_grid_initialized(self):
        """Test that board grid is properly initialized with None values."""
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                self.assertIsNone(self.board.get_piece(pos))

    def test_terrain_map_initialized(self):
        """Test that terrain map is initialized with correct terrain types."""
        # Check that water squares are set
        self.assertEqual(self.board.get_terrain(Position(3, 1)), TerrainType.WATER)
        self.assertEqual(self.board.get_terrain(Position(4, 2)), TerrainType.WATER)

        # Check that dens are set
        self.assertEqual(self.board.get_terrain(Position(0, 3)), TerrainType.DEN)
        self.assertEqual(self.board.get_terrain(Position(8, 3)), TerrainType.DEN)

        # Check that traps are set
        self.assertEqual(self.board.get_terrain(Position(0, 2)), TerrainType.TRAP)
        self.assertEqual(self.board.get_terrain(Position(7, 4)), TerrainType.TRAP)

        # Check that land is default
        self.assertEqual(self.board.get_terrain(Position(4, 0)), TerrainType.LAND)


class TestPositionValidation(unittest.TestCase):
    """Test position validation and boundary checking."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_valid_positions(self):
        """Test that valid positions are recognized."""
        self.assertTrue(self.board.is_valid_position(Position(0, 0)))
        self.assertTrue(self.board.is_valid_position(Position(8, 6)))
        self.assertTrue(self.board.is_valid_position(Position(4, 3)))

    def test_invalid_positions_negative(self):
        """Test that negative positions are invalid."""
        self.assertFalse(self.board.is_valid_position(Position(-1, 0)))
        self.assertFalse(self.board.is_valid_position(Position(0, -1)))
        self.assertFalse(self.board.is_valid_position(Position(-1, -1)))

    def test_invalid_positions_out_of_bounds(self):
        """Test that out-of-bounds positions are invalid."""
        self.assertFalse(self.board.is_valid_position(Position(9, 0)))
        self.assertFalse(self.board.is_valid_position(Position(0, 7)))
        self.assertFalse(self.board.is_valid_position(Position(10, 10)))

    def test_boundary_positions(self):
        """Test positions at the boundaries."""
        # Top-left corner
        self.assertTrue(self.board.is_valid_position(Position(0, 0)))
        # Bottom-right corner
        self.assertTrue(self.board.is_valid_position(Position(8, 6)))
        # Just outside boundaries
        self.assertFalse(self.board.is_valid_position(Position(9, 6)))
        self.assertFalse(self.board.is_valid_position(Position(8, 7)))


class TestPiecePlacement(unittest.TestCase):
    """Test piece placement and retrieval."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()
        self.player = Player("Test Player", PlayerColor.RED)

    def test_set_and_get_piece(self):
        """Test setting and getting a piece."""
        from model.piece import Rat
        pos = Position(2, 3)
        piece = Rat(self.player, pos)

        self.board.set_piece(pos, piece)
        retrieved_piece = self.board.get_piece(pos)

        self.assertIsNotNone(retrieved_piece)
        self.assertEqual(retrieved_piece, piece)

    def test_clear_piece(self):
        """Test clearing a piece from the board."""
        from model.piece import Cat
        pos = Position(3, 4)
        piece = Cat(self.player, pos)

        self.board.set_piece(pos, piece)
        self.assertIsNotNone(self.board.get_piece(pos))

        self.board.set_piece(pos, None)
        self.assertIsNone(self.board.get_piece(pos))

    def test_get_piece_invalid_position(self):
        """Test getting piece from invalid position returns None."""
        invalid_pos = Position(-1, 5)
        self.assertIsNone(self.board.get_piece(invalid_pos))

        invalid_pos2 = Position(10, 10)
        self.assertIsNone(self.board.get_piece(invalid_pos2))

    def test_set_piece_invalid_position(self):
        """Test setting piece at invalid position does nothing."""
        from model.piece import Dog
        invalid_pos = Position(15, 15)
        piece = Dog(self.player, invalid_pos)

        # Should not raise an error, just do nothing
        self.board.set_piece(invalid_pos, piece)
        self.assertIsNone(self.board.get_piece(invalid_pos))


class TestTerrainDetection(unittest.TestCase):
    """Test terrain type detection methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_water_detection(self):
        """Test water square detection."""
        # Water squares in the river
        self.assertTrue(self.board.is_water(Position(3, 1)))
        self.assertTrue(self.board.is_water(Position(4, 2)))
        self.assertTrue(self.board.is_water(Position(5, 4)))
        self.assertTrue(self.board.is_water(Position(3, 5)))

        # Non-water squares
        self.assertFalse(self.board.is_water(Position(0, 0)))
        self.assertFalse(self.board.is_water(Position(4, 3)))
        self.assertFalse(self.board.is_water(Position(8, 6)))

    def test_all_water_squares(self):
        """Test all water squares are correctly identified."""
        water_positions = [
            Position(3, 1), Position(3, 2), Position(3, 4), Position(3, 5),
            Position(4, 1), Position(4, 2), Position(4, 4), Position(4, 5),
            Position(5, 1), Position(5, 2), Position(5, 4), Position(5, 5),
        ]

        for pos in water_positions:
            self.assertTrue(self.board.is_water(pos),
                          f"Position {pos} should be water")

    def test_den_detection_without_player(self):
        """Test den detection without specifying player."""
        # Both dens should be detected
        self.assertTrue(self.board.is_den(Position(0, 3)))
        self.assertTrue(self.board.is_den(Position(8, 3)))

        # Non-den positions
        self.assertFalse(self.board.is_den(Position(0, 0)))
        self.assertFalse(self.board.is_den(Position(4, 3)))

    def test_den_detection_with_player(self):
        """Test player-specific den detection."""
        red_player = Player("Red", PlayerColor.RED)
        blue_player = Player("Blue", PlayerColor.BLUE)

        # Red player's den
        self.assertTrue(self.board.is_den(Position(8, 3), red_player))
        self.assertFalse(self.board.is_den(Position(0, 3), red_player))

        # Blue player's den
        self.assertTrue(self.board.is_den(Position(0, 3), blue_player))
        self.assertFalse(self.board.is_den(Position(8, 3), blue_player))

    def test_trap_detection_without_player(self):
        """Test trap detection without specifying player."""
        # Red traps
        self.assertTrue(self.board.is_trap(Position(7, 2)))
        self.assertTrue(self.board.is_trap(Position(8, 4)))

        # Blue traps
        self.assertTrue(self.board.is_trap(Position(0, 2)))
        self.assertTrue(self.board.is_trap(Position(1, 4)))

        # Non-trap positions
        self.assertFalse(self.board.is_trap(Position(4, 3)))

    def test_trap_detection_with_player(self):
        """Test player-specific trap detection."""
        red_player = Player("Red", PlayerColor.RED)
        blue_player = Player("Blue", PlayerColor.BLUE)

        # Red player's traps (rows 7-8)
        self.assertTrue(self.board.is_trap(Position(7, 2), red_player))
        self.assertTrue(self.board.is_trap(Position(8, 4), red_player))
        self.assertFalse(self.board.is_trap(Position(0, 2), red_player))
        self.assertFalse(self.board.is_trap(Position(1, 4), red_player))

        # Blue player's traps (rows 0-1)
        self.assertTrue(self.board.is_trap(Position(0, 2), blue_player))
        self.assertTrue(self.board.is_trap(Position(1, 4), blue_player))
        self.assertFalse(self.board.is_trap(Position(7, 2), blue_player))
        self.assertFalse(self.board.is_trap(Position(8, 4), blue_player))

    def test_all_red_traps(self):
        """Test all red player traps are correctly identified."""
        red_player = Player("Red", PlayerColor.RED)
        red_trap_positions = [
            Position(7, 2), Position(7, 4),
            Position(8, 2), Position(8, 4),
        ]

        for pos in red_trap_positions:
            self.assertTrue(self.board.is_trap(pos, red_player),
                          f"Position {pos} should be a red trap")

    def test_all_blue_traps(self):
        """Test all blue player traps are correctly identified."""
        blue_player = Player("Blue", PlayerColor.BLUE)
        blue_trap_positions = [
            Position(0, 2), Position(0, 4),
            Position(1, 2), Position(1, 4),
        ]

        for pos in blue_trap_positions:
            self.assertTrue(self.board.is_trap(pos, blue_player),
                          f"Position {pos} should be a blue trap")

    def test_get_terrain_default_land(self):
        """Test that positions without special terrain return LAND."""
        # Test various positions that should be land
        land_positions = [
            Position(0, 0), Position(2, 3), Position(6, 5), Position(8, 0)
        ]

        for pos in land_positions:
            self.assertEqual(self.board.get_terrain(pos), TerrainType.LAND,
                           f"Position {pos} should be LAND")


class TestTerrainLayout(unittest.TestCase):
    """Test the complete terrain layout of the board."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_river_layout(self):
        """Test that river (water) is correctly positioned."""
        # River should be in rows 3-5, columns 1-2 and 4-5
        for row in range(3, 6):
            for col in range(7):
                pos = Position(row, col)
                if col in [1, 2, 4, 5]:
                    self.assertTrue(self.board.is_water(pos),
                                  f"Position {pos} should be water")
                else:
                    self.assertFalse(self.board.is_water(pos),
                                   f"Position {pos} should not be water")

    def test_den_positions(self):
        """Test that dens are at correct positions."""
        # Blue den at top center
        self.assertTrue(self.board.is_den(Position(0, 3)))
        self.assertEqual(self.board.get_terrain(Position(0, 3)), TerrainType.DEN)

        # Red den at bottom center
        self.assertTrue(self.board.is_den(Position(8, 3)))
        self.assertEqual(self.board.get_terrain(Position(8, 3)), TerrainType.DEN)

        # Only these two positions should be dens
        den_count = 0
        for row in range(9):
            for col in range(7):
                if self.board.is_den(Position(row, col)):
                    den_count += 1
        self.assertEqual(den_count, 2)

    def test_trap_positions(self):
        """Test that traps are at correct positions."""
        # Blue traps (top)
        blue_traps = [
            Position(0, 2), Position(0, 4),
            Position(1, 2), Position(1, 4)
        ]
        for pos in blue_traps:
            self.assertTrue(self.board.is_trap(pos))
            self.assertEqual(self.board.get_terrain(pos), TerrainType.TRAP)

        # Red traps (bottom)
        red_traps = [
            Position(7, 2), Position(7, 4),
            Position(8, 2), Position(8, 4)
        ]
        for pos in red_traps:
            self.assertTrue(self.board.is_trap(pos))
            self.assertEqual(self.board.get_terrain(pos), TerrainType.TRAP)

        # Count total traps
        trap_count = 0
        for row in range(9):
            for col in range(7):
                if self.board.is_trap(Position(row, col)):
                    trap_count += 1
        self.assertEqual(trap_count, 8)


if __name__ == '__main__':
    unittest.main()
