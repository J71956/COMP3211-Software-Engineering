"""
GameState class for Jungle Game.
Represents an immutable snapshot of the game state for undo functionality.
"""

from typing import Dict, Optional, TYPE_CHECKING
from model.position import Position

if TYPE_CHECKING:
    from model.piece import Piece


class GameState:
    """
    Immutable game state snapshot for undo functionality.

    This class captures the complete state of the game at a specific point,
    allowing the game to be restored to this state later.

    Attributes:
        board_state: Dictionary mapping positions to pieces (or None for empty)
        current_player_index: Index of the current player
        move_count: Number of moves made so far
    """

    def __init__(
        self,
        board_state: Dict[Position, Optional['Piece']],
        current_player_index: int,
        move_count: int
    ):
        """
        Initialize a game state snapshot.

        Args:
            board_state: Dictionary mapping positions to pieces
            current_player_index: Index of the current player (0 or 1)
            move_count: Number of moves made so far
        """
        # Store a deep copy of the board state to ensure immutability
        self._board_state = board_state.copy()
        self._current_player_index = current_player_index
        self._move_count = move_count

    @property
    def board_state(self) -> Dict[Position, Optional['Piece']]:
        """Get the board state (returns a copy to maintain immutability)."""
        return self._board_state.copy()

    @property
    def current_player_index(self) -> int:
        """Get the current player index."""
        return self._current_player_index

    @property
    def move_count(self) -> int:
        """Get the move count."""
        return self._move_count

    @staticmethod
    def capture_from_board(board: 'Board', current_player_index: int, move_count: int) -> 'GameState':
        """
        Create a game state snapshot from a board.

        Args:
            board: The board to capture state from
            current_player_index: Index of the current player
            move_count: Number of moves made so far

        Returns:
            A new GameState instance
        """
        from model.board import Board

        board_state: Dict[Position, Optional['Piece']] = {}

        # Capture all pieces on the board
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                piece = board.get_piece(pos)
                if piece is not None:
                    board_state[pos] = piece

        return GameState(board_state, current_player_index, move_count)

    def restore_to_board(self, board: 'Board') -> None:
        """
        Restore this game state to a board.

        Args:
            board: The board to restore state to
        """
        from model.board import Board

        # Clear the board first
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                board.set_piece(pos, None)

        # Restore pieces from the saved state
        for pos, piece in self._board_state.items():
            if piece is not None:
                # Update piece position to match the saved position
                piece.position = pos
                board.set_piece(pos, piece)

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another game state.

        Args:
            other: The other object to compare with

        Returns:
            True if states are equal, False otherwise
        """
        if not isinstance(other, GameState):
            return False

        return (
            self._current_player_index == other._current_player_index
            and self._move_count == other._move_count
            and self._board_state == other._board_state
        )

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"GameState(current_player={self._current_player_index}, "
            f"move_count={self._move_count}, "
            f"pieces={len(self._board_state)})"
        )
