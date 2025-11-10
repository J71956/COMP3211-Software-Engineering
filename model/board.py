"""
Board class for Jungle Game.
Represents the 7x9 game board with terrain and piece management.
"""

from typing import Optional, Dict, TYPE_CHECKING
from model.position import Position
from model.enums import TerrainType

if TYPE_CHECKING:
    from model.piece import Piece
    from model.player import Player


class Board:
    """
    7x9 game board with terrain and piece management.
    
    Attributes:
        grid: 2D list representing the board (9 rows x 7 columns)
        terrain_map: Mapping of positions to terrain types
    """
    
    BOARD_HEIGHT = 9
    BOARD_WIDTH = 7
    
    def __init__(self):
        """Initialize an empty board with terrain."""
        # Create empty grid (9 rows x 7 columns)
        self._grid: list[list[Optional['Piece']]] = [
            [None for _ in range(self.BOARD_WIDTH)] 
            for _ in range(self.BOARD_HEIGHT)
        ]
        
        # Initialize terrain map
        self._terrain_map: Dict[Position, TerrainType] = {}
        self._initialize_terrain()
    
    def _initialize_terrain(self) -> None:
        """Initialize the terrain map with dens, traps, and water."""
        # Water squares (river in the middle, rows 3-5, columns 1-2 and 4-5)
        for row in range(3, 6):
            for col in [1, 2, 4, 5]:
                self._terrain_map[Position(row, col)] = TerrainType.WATER
        
        # Red player (bottom) - den and traps
        self._terrain_map[Position(8, 3)] = TerrainType.DEN  # Red den
        self._terrain_map[Position(7, 2)] = TerrainType.TRAP  # Red trap left
        self._terrain_map[Position(7, 4)] = TerrainType.TRAP  # Red trap right
        self._terrain_map[Position(8, 2)] = TerrainType.TRAP  # Red trap bottom-left
        self._terrain_map[Position(8, 4)] = TerrainType.TRAP  # Red trap bottom-right
        
        # Blue player (top) - den and traps
        self._terrain_map[Position(0, 3)] = TerrainType.DEN  # Blue den
        self._terrain_map[Position(1, 2)] = TerrainType.TRAP  # Blue trap left
        self._terrain_map[Position(1, 4)] = TerrainType.TRAP  # Blue trap right
        self._terrain_map[Position(0, 2)] = TerrainType.TRAP  # Blue trap top-left
        self._terrain_map[Position(0, 4)] = TerrainType.TRAP  # Blue trap top-right
    
    def get_piece(self, pos: Position) -> Optional['Piece']:
        """
        Get the piece at the specified position.
        
        Args:
            pos: The position to check
            
        Returns:
            The piece at the position, or None if empty
        """
        if not self.is_valid_position(pos):
            return None
        return self._grid[pos.row][pos.col]
    
    def set_piece(self, pos: Position, piece: Optional['Piece']) -> None:
        """
        Set a piece at the specified position.
        
        Args:
            pos: The position to set
            piece: The piece to place, or None to clear
        """
        if self.is_valid_position(pos):
            self._grid[pos.row][pos.col] = piece
    
    def is_valid_position(self, pos: Position) -> bool:
        """
        Check if a position is within board bounds.
        
        Args:
            pos: The position to check
            
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= pos.row < self.BOARD_HEIGHT and 0 <= pos.col < self.BOARD_WIDTH
    
    def get_terrain(self, pos: Position) -> TerrainType:
        """
        Get the terrain type at the specified position.
        
        Args:
            pos: The position to check
            
        Returns:
            The terrain type at the position (defaults to LAND)
        """
        return self._terrain_map.get(pos, TerrainType.LAND)
    
    def is_den(self, pos: Position, player: Optional['Player'] = None) -> bool:
        """
        Check if a position is a den.
        
        Args:
            pos: The position to check
            player: Optional player to check for specific den
            
        Returns:
            True if position is a den, False otherwise
        """
        terrain = self.get_terrain(pos)
        if terrain != TerrainType.DEN:
            return False
        
        if player is None:
            return True
        
        # Red player's den is at row 8, Blue player's den is at row 0
        from model.enums import PlayerColor
        if player.color == PlayerColor.RED:
            return pos.row == 8
        else:
            return pos.row == 0
    
    def is_trap(self, pos: Position, player: Optional['Player'] = None) -> bool:
        """
        Check if a position is a trap.
        
        Args:
            pos: The position to check
            player: Optional player to check for specific trap
            
        Returns:
            True if position is a trap, False otherwise
        """
        terrain = self.get_terrain(pos)
        if terrain != TerrainType.TRAP:
            return False
        
        if player is None:
            return True
        
        # Red player's traps are at rows 7-8, Blue player's traps are at rows 0-1
        from model.enums import PlayerColor
        if player.color == PlayerColor.RED:
            return pos.row >= 7
        else:
            return pos.row <= 1
    
    def is_water(self, pos: Position) -> bool:
        """
        Check if a position is water.
        
        Args:
            pos: The position to check
            
        Returns:
            True if position is water, False otherwise
        """
        return self.get_terrain(pos) == TerrainType.WATER
