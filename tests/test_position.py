"""
Unit tests for Position class.
"""

import unittest
from model.position import Position
from model.enums import Direction


class TestPosition(unittest.TestCase):
    """Test cases for Position class."""
    
    def test_position_creation(self):
        """Test creating a position with row and column."""
        pos = Position(3, 4)
        self.assertEqual(pos.row, 3)
        self.assertEqual(pos.col, 4)
    
    def test_position_immutability(self):
        """Test that position attributes cannot be modified."""
        pos = Position(2, 5)
        with self.assertRaises(AttributeError):
            pos.row = 10
        with self.assertRaises(AttributeError):
            pos.col = 10
    
    def test_position_equality(self):
        """Test position equality comparison."""
        pos1 = Position(1, 2)
        pos2 = Position(1, 2)
        pos3 = Position(1, 3)
        
        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)
    
    def test_position_hash(self):
        """Test that positions can be used in sets and as dict keys."""
        pos1 = Position(0, 0)
        pos2 = Position(0, 0)
        pos3 = Position(1, 1)
        
        position_set = {pos1, pos2, pos3}
        self.assertEqual(len(position_set), 2)
        
        position_dict = {pos1: "value1", pos3: "value2"}
        self.assertEqual(position_dict[pos2], "value1")
    
    def test_is_adjacent_horizontal(self):
        """Test adjacency for horizontally adjacent positions."""
        pos1 = Position(2, 3)
        pos2 = Position(2, 4)
        pos3 = Position(2, 2)
        
        self.assertTrue(pos1.is_adjacent(pos2))
        self.assertTrue(pos1.is_adjacent(pos3))
        self.assertTrue(pos2.is_adjacent(pos1))
    
    def test_is_adjacent_vertical(self):
        """Test adjacency for vertically adjacent positions."""
        pos1 = Position(2, 3)
        pos2 = Position(3, 3)
        pos3 = Position(1, 3)
        
        self.assertTrue(pos1.is_adjacent(pos2))
        self.assertTrue(pos1.is_adjacent(pos3))
        self.assertTrue(pos2.is_adjacent(pos1))
    
    def test_is_not_adjacent_diagonal(self):
        """Test that diagonal positions are not adjacent."""
        pos1 = Position(2, 3)
        pos2 = Position(3, 4)
        
        self.assertFalse(pos1.is_adjacent(pos2))
    
    def test_is_not_adjacent_far(self):
        """Test that distant positions are not adjacent."""
        pos1 = Position(0, 0)
        pos2 = Position(5, 5)
        
        self.assertFalse(pos1.is_adjacent(pos2))
    
    def test_get_direction_north(self):
        """Test getting direction for northward movement."""
        pos1 = Position(3, 2)
        pos2 = Position(2, 2)
        
        self.assertEqual(pos1.get_direction(pos2), Direction.NORTH)
    
    def test_get_direction_south(self):
        """Test getting direction for southward movement."""
        pos1 = Position(3, 2)
        pos2 = Position(4, 2)
        
        self.assertEqual(pos1.get_direction(pos2), Direction.SOUTH)
    
    def test_get_direction_east(self):
        """Test getting direction for eastward movement."""
        pos1 = Position(3, 2)
        pos2 = Position(3, 3)
        
        self.assertEqual(pos1.get_direction(pos2), Direction.EAST)
    
    def test_get_direction_west(self):
        """Test getting direction for westward movement."""
        pos1 = Position(3, 2)
        pos2 = Position(3, 1)
        
        self.assertEqual(pos1.get_direction(pos2), Direction.WEST)
    
    def test_get_direction_not_adjacent(self):
        """Test that non-adjacent positions return None."""
        pos1 = Position(0, 0)
        pos2 = Position(5, 5)
        
        self.assertIsNone(pos1.get_direction(pos2))
    
    def test_move_north(self):
        """Test moving in the north direction."""
        pos = Position(3, 2)
        new_pos = pos.move(Direction.NORTH)
        
        self.assertEqual(new_pos, Position(2, 2))
        self.assertEqual(pos, Position(3, 2))  # Original unchanged
    
    def test_move_south(self):
        """Test moving in the south direction."""
        pos = Position(3, 2)
        new_pos = pos.move(Direction.SOUTH)
        
        self.assertEqual(new_pos, Position(4, 2))
    
    def test_move_east(self):
        """Test moving in the east direction."""
        pos = Position(3, 2)
        new_pos = pos.move(Direction.EAST)
        
        self.assertEqual(new_pos, Position(3, 3))
    
    def test_move_west(self):
        """Test moving in the west direction."""
        pos = Position(3, 2)
        new_pos = pos.move(Direction.WEST)
        
        self.assertEqual(new_pos, Position(3, 1))
    
    def test_str_representation(self):
        """Test string representation of position."""
        pos = Position(2, 5)
        self.assertEqual(str(pos), "(2,5)")
    
    def test_repr_representation(self):
        """Test repr representation of position."""
        pos = Position(2, 5)
        self.assertEqual(repr(pos), "Position(row=2, col=5)")


if __name__ == '__main__':
    unittest.main()
