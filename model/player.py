"""
Player class for Jungle Game.
Represents a player in the game.
"""

from typing import Set, List, TYPE_CHECKING
from model.enums import PlayerColor

if TYPE_CHECKING:
    from model.piece import Piece


class Player:
    """
    Player information and piece ownership.
    
    Attributes:
        name: The player's name
        color: The player's color (RED or BLUE)
        pieces: Set of pieces owned by this player
    """
    
    def __init__(self, name: str, color: PlayerColor):
        """
        Initialize a player.
        
        Args:
            name: The player's name
            color: The player's color
        """
        self._name = name
        self._color = color
        self._pieces: Set['Piece'] = set()
    
    @property
    def name(self) -> str:
        """Get the player's name."""
        return self._name
    
    @property
    def color(self) -> PlayerColor:
        """Get the player's color."""
        return self._color
    
    @property
    def pieces(self) -> Set['Piece']:
        """Get the set of pieces owned by this player."""
        return self._pieces
    
    def add_piece(self, piece: 'Piece') -> None:
        """
        Add a piece to this player's collection.
        
        Args:
            piece: The piece to add
        """
        self._pieces.add(piece)
    
    def remove_piece(self, piece: 'Piece') -> None:
        """
        Remove a piece from this player's collection.
        
        Args:
            piece: The piece to remove
        """
        self._pieces.discard(piece)
    
    def get_active_pieces(self) -> List['Piece']:
        """
        Get all active pieces owned by this player.
        
        Returns:
            List of active pieces
        """
        return list(self._pieces)
    
    def has_pieces(self) -> bool:
        """
        Check if the player has any pieces remaining.
        
        Returns:
            True if player has pieces, False otherwise
        """
        return len(self._pieces) > 0
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"{self.name} ({self.color.value})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Player(name='{self.name}', color={self.color.value}, pieces={len(self._pieces)})"
