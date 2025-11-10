"""
Player class for Jungle Game.
Represents a player with name, color, and piece ownership.
"""

from typing import List, Set, TYPE_CHECKING
from model.enums import PlayerColor
from model.position import Position

if TYPE_CHECKING:
    from model.piece import Piece


class Player:
    """
    Represents a player in the Jungle Game.

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
            color: The player's color (RED or BLUE)
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
        return self._pieces.copy()

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

    def get_den_position(self) -> Position:
        """
        Get the position of this player's den.

        Returns:
            Position of the player's den
        """
        if self.color == PlayerColor.RED:
            return Position(8, 3)  # Red den at bottom
        return Position(0, 3)  # Blue den at top

    def get_trap_positions(self) -> List[Position]:
        """
        Get the positions of this player's traps.

        Returns:
            List of trap positions for this player
        """
        if self.color == PlayerColor.RED:
            # Red traps at bottom
            return [
                Position(7, 2),
                Position(7, 4),
                Position(8, 2),
                Position(8, 4)
            ]
        # Blue traps at top
        return [
            Position(0, 2),
            Position(0, 4),
            Position(1, 2),
            Position(1, 4)
        ]

    def __str__(self) -> str:
        """String representation of the player."""
        return f"{self.name} ({self.color.value})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Player(name='{self.name}', color={self.color.value}, pieces={len(self._pieces)})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another player."""
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.color == other.color

    def __hash__(self) -> int:
        """Generate hash for use in sets and dictionaries."""
        return hash((self.name, self.color))
