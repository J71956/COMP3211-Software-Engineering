"""
Enumeration types for Jungle Game.
Defines core enums used throughout the game.
"""

from enum import Enum


class TerrainType(Enum):
    """Types of terrain on the game board."""
    LAND = "land"
    WATER = "water"
    DEN = "den"
    TRAP = "trap"


class PlayerColor(Enum):
    """Player colors in the game."""
    RED = "red"
    BLUE = "blue"


class GameStatus(Enum):
    """Current status of the game."""
    ONGOING = "ongoing"
    PLAYER_ONE_WINS = "player_one_wins"
    PLAYER_TWO_WINS = "player_two_wins"
    DRAW = "draw"


class Direction(Enum):
    """Cardinal directions for piece movement."""
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    
    @property
    def row_delta(self) -> int:
        """Get the row change for this direction."""
        return self.value[0]
    
    @property
    def col_delta(self) -> int:
        """Get the column change for this direction."""
        return self.value[1]
