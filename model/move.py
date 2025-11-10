"""
Move and MoveResult classes for Jungle Game.
Handles move tracking and operation feedback.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING

from model.position import Position

if TYPE_CHECKING:
    from model.piece import Piece


@dataclass
class MoveResult:
    """
    Result of a move operation.

    Provides feedback about whether a move was successful and includes
    relevant information about the move outcome.

    Attributes:
        success: Whether the move was successful
        message: Descriptive message about the move result
        captured_piece: The piece that was captured, if any
    """
    success: bool
    message: str
    captured_piece: Optional['Piece'] = None


@dataclass
class Move:
    """
    Immutable move record with timestamp.

    Records all information about a move for history tracking,
    undo functionality, and game replay.

    Attributes:
        piece: The piece that moved
        from_pos: The starting position
        to_pos: The destination position
        captured_piece: The piece that was captured, if any
        timestamp: When the move was made
    """
    piece: 'Piece'
    from_pos: Position
    to_pos: Position
    captured_piece: Optional['Piece']
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the move to a dictionary for file operations.

        Returns:
            Dictionary representation of the move
        """
        return {
            'piece_type': self.piece.__class__.__name__,
            'piece_rank': self.piece.rank,
            'owner_color': self.piece.owner.color.value,
            'from_row': self.from_pos.row,
            'from_col': self.from_pos.col,
            'to_row': self.to_pos.row,
            'to_col': self.to_pos.col,
            'captured_piece_type': (
                self.captured_piece.__class__.__name__
                if self.captured_piece else None
            ),
            'captured_piece_rank': (
                self.captured_piece.rank
                if self.captured_piece else None
            ),
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any], game: 'Game') -> 'Move':
        """
        Deserialize a move from a dictionary.

        Args:
            data: Dictionary containing move data
            game: The game instance to resolve piece references

        Returns:
            Move instance reconstructed from the dictionary

        Raises:
            ValueError: If the data is invalid or incomplete
        """
        try:
            from_pos = Position(data['from_row'], data['from_col'])
            to_pos = Position(data['to_row'], data['to_col'])

            # Find the piece at the from_pos in the game
            piece = game.board.get_piece(from_pos)
            if piece is None:
                raise ValueError(f"No piece found at position {from_pos}")

            # Validate piece type and rank match
            if piece.__class__.__name__ != data['piece_type']:
                raise ValueError(
                    f"Piece type mismatch: expected {data['piece_type']}, "
                    f"found {piece.__class__.__name__}"
                )

            if piece.rank != data['piece_rank']:
                raise ValueError(
                    f"Piece rank mismatch: expected {data['piece_rank']}, "
                    f"found {piece.rank}"
                )

            # Handle captured piece
            captured_piece = None
            if data.get('captured_piece_type'):
                captured_piece = game.board.get_piece(to_pos)

            # Parse timestamp
            timestamp = datetime.fromisoformat(data['timestamp'])

            return Move(
                piece=piece,
                from_pos=from_pos,
                to_pos=to_pos,
                captured_piece=captured_piece,
                timestamp=timestamp
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in move data: {e}") from e

    def to_record_string(self) -> str:
        """
        Convert the move to a human-readable string for record files.

        Returns:
            Formatted string representation for .record files
        """
        move_str = (
            f"{self.piece.owner.name} - {self.piece.__class__.__name__} "
            f"from {self.from_pos} to {self.to_pos}"
        )

        if self.captured_piece:
            move_str += f" (captured {self.captured_piece.__class__.__name__})"

        return move_str

    @staticmethod
    def parse_record_string(record_str: str) -> Dict[str, Any]:
        """
        Parse a move from a record file string.

        Args:
            record_str: String in the format produced by to_record_string()

        Returns:
            Dictionary containing parsed move information

        Raises:
            ValueError: If the string format is invalid
        """
        import re

        # Pattern: "Player - PieceType from (row,col) to (row,col) [(captured PieceType)]"
        pattern = (
            r"(.+?) - (\w+) from \((\d+),(\d+)\) to \((\d+),(\d+)\)"
            r"(?: \(captured (\w+)\))?"
        )

        match = re.match(pattern, record_str)
        if not match:
            raise ValueError(f"Invalid record string format: {record_str}")

        player_name, piece_type, from_row, from_col, to_row, to_col, captured = match.groups()

        return {
            'player_name': player_name,
            'piece_type': piece_type,
            'from_row': int(from_row),
            'from_col': int(from_col),
            'to_row': int(to_row),
            'to_col': int(to_col),
            'captured_piece_type': captured
        }

    def __str__(self) -> str:
        """String representation of the move."""
        return self.to_record_string()

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Move(piece={self.piece.__class__.__name__}, "
            f"from={self.from_pos}, to={self.to_pos}, "
            f"captured={self.captured_piece.__class__.__name__ if self.captured_piece else None}, "
            f"timestamp={self.timestamp.isoformat()})"
        )
