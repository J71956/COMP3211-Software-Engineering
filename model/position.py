"""
Position class for Jungle Game.
Represents an immutable position on the game board.
"""

from typing import Optional
from model.enums import Direction


class Position:
    """
    Immutable position representation on the game board.
    
    Attributes:
        row: The row index (0-8 for a 9-row board)
        col: The column index (0-6 for a 7-column board)
    """
    
    def __init__(self, row: int, col: int):
        """
        Initialize a position.
        
        Args:
            row: The row index
            col: The column index
        """
        self._row = row
        self._col = col
    
    @property
    def row(self) -> int:
        """Get the row index."""
        return self._row
    
    @property
    def col(self) -> int:
        """Get the column index."""
        return self._col
    
    def is_adjacent(self, other: 'Position') -> bool:
        """
        Check if another position is adjacent (horizontally or vertically).
        
        Args:
            other: The other position to check
            
        Returns:
            True if positions are adjacent, False otherwise
        """
        row_diff = abs(self.row - other.row)
        col_diff = abs(self.col - other.col)
        
        # Adjacent means exactly one square away horizontally or vertically
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    
    def get_direction(self, other: 'Position') -> Optional[Direction]:
        """
        Get the direction from this position to another adjacent position.
        
        Args:
            other: The target position
            
        Returns:
            Direction enum if positions are adjacent, None otherwise
        """
        if not self.is_adjacent(other):
            return None
        
        row_diff = other.row - self.row
        col_diff = other.col - self.col
        
        if row_diff == -1:
            return Direction.NORTH
        elif row_diff == 1:
            return Direction.SOUTH
        elif col_diff == 1:
            return Direction.EAST
        elif col_diff == -1:
            return Direction.WEST
        
        return None
    
    def move(self, direction: Direction) -> 'Position':
        """
        Create a new position by moving in a direction.
        
        Args:
            direction: The direction to move
            
        Returns:
            A new Position object
        """
        return Position(
            self.row + direction.row_delta,
            self.col + direction.col_delta
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another position."""
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self) -> int:
        """Generate hash for use in sets and dictionaries."""
        return hash((self.row, self.col))
    
    def __str__(self) -> str:
        """String representation of the position."""
        return f"({self.row},{self.col})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Position(row={self.row}, col={self.col})"
