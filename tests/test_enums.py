"""
Unit tests for enum types.
"""

import unittest
from model.enums import TerrainType, PlayerColor, GameStatus, Direction


class TestEnums(unittest.TestCase):
    """Test cases for enum types."""
    
    def test_terrain_type_values(self):
        """Test TerrainType enum has correct values."""
        self.assertEqual(TerrainType.LAND.value, "land")
        self.assertEqual(TerrainType.WATER.value, "water")
        self.assertEqual(TerrainType.DEN.value, "den")
        self.assertEqual(TerrainType.TRAP.value, "trap")
    
    def test_player_color_values(self):
        """Test PlayerColor enum has correct values."""
        self.assertEqual(PlayerColor.RED.value, "red")
        self.assertEqual(PlayerColor.BLUE.value, "blue")
    
    def test_game_status_values(self):
        """Test GameStatus enum has correct values."""
        self.assertEqual(GameStatus.ONGOING.value, "ongoing")
        self.assertEqual(GameStatus.PLAYER_ONE_WINS.value, "player_one_wins")
        self.assertEqual(GameStatus.PLAYER_TWO_WINS.value, "player_two_wins")
        self.assertEqual(GameStatus.DRAW.value, "draw")
    
    def test_direction_values(self):
        """Test Direction enum has correct tuple values."""
        self.assertEqual(Direction.NORTH.value, (-1, 0))
        self.assertEqual(Direction.SOUTH.value, (1, 0))
        self.assertEqual(Direction.EAST.value, (0, 1))
        self.assertEqual(Direction.WEST.value, (0, -1))
    
    def test_direction_row_delta(self):
        """Test Direction row_delta property."""
        self.assertEqual(Direction.NORTH.row_delta, -1)
        self.assertEqual(Direction.SOUTH.row_delta, 1)
        self.assertEqual(Direction.EAST.row_delta, 0)
        self.assertEqual(Direction.WEST.row_delta, 0)
    
    def test_direction_col_delta(self):
        """Test Direction col_delta property."""
        self.assertEqual(Direction.NORTH.col_delta, 0)
        self.assertEqual(Direction.SOUTH.col_delta, 0)
        self.assertEqual(Direction.EAST.col_delta, 1)
        self.assertEqual(Direction.WEST.col_delta, -1)


if __name__ == '__main__':
    unittest.main()
