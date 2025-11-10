"""
Game class for Jungle Game.
Central game state manager and rule enforcer.
"""

from typing import List, Optional
from datetime import datetime

from model.board import Board
from model.player import Player
from model.position import Position
from model.enums import PlayerColor, GameStatus
from model.exceptions import GameOverException
from model.game_state import GameState
from model.move import Move, MoveResult


class Game:
    """
    Central game state manager and rule enforcer.

    Manages the complete game state including board, players, turn management,
    move history, and game status.

    Attributes:
        board: The game board
        players: List of players (2 players)
        current_player_index: Index of the current player (0 or 1)
        move_history: List of all moves made in the game
        game_states: List of game states for undo functionality
        game_status: Current status of the game
    """

    MAX_UNDO_MOVES = 3

    def __init__(self, player1_name: str = "Player 1", player2_name: str = "Player 2"):
        """
        Initialize a new game.

        Args:
            player1_name: Name for player 1 (Red)
            player2_name: Name for player 2 (Blue)
        """
        self._board = Board()
        self._players: List[Player] = [
            Player(player1_name, PlayerColor.RED),
            Player(player2_name, PlayerColor.BLUE)
        ]
        self._current_player_index = 0  # Player 1 (Red) starts
        self._move_history: List[Move] = []
        self._game_states: List[GameState] = []
        self._game_status = GameStatus.ONGOING

        # Initialize pieces on the board
        self._initialize_pieces()

    def _initialize_pieces(self) -> None:
        """Initialize all pieces in their starting positions."""
        from model.piece import Rat, Cat, Dog, Wolf, Leopard, Tiger, Lion, Elephant

        # Red player pieces (bottom, rows 6-8)
        red_player = self._players[0]
        red_pieces = [
            # Row 6
            Lion(red_player, Position(6, 0)),
            Tiger(red_player, Position(6, 6)),
            # Row 7
            Dog(red_player, Position(7, 1)),
            Cat(red_player, Position(7, 5)),
            # Row 8
            Rat(red_player, Position(8, 0)),
            Leopard(red_player, Position(8, 2)),
            Wolf(red_player, Position(8, 4)),
            Elephant(red_player, Position(8, 6)),
        ]

        # Blue player pieces (top, rows 0-2)
        blue_player = self._players[1]
        blue_pieces = [
            # Row 0
            Elephant(blue_player, Position(0, 0)),
            Wolf(blue_player, Position(0, 2)),
            Leopard(blue_player, Position(0, 4)),
            Rat(blue_player, Position(0, 6)),
            # Row 1
            Cat(blue_player, Position(1, 1)),
            Dog(blue_player, Position(1, 5)),
            # Row 2
            Tiger(blue_player, Position(2, 0)),
            Lion(blue_player, Position(2, 6)),
        ]

        # Place pieces on board and add to players
        for piece in red_pieces:
            self._board.set_piece(piece.position, piece)
            red_player.add_piece(piece)

        for piece in blue_pieces:
            self._board.set_piece(piece.position, piece)
            blue_player.add_piece(piece)

    @property
    def board(self) -> Board:
        """Get the game board."""
        return self._board

    @property
    def players(self) -> List[Player]:
        """Get the list of players."""
        return self._players.copy()

    @property
    def current_player_index(self) -> int:
        """Get the current player index."""
        return self._current_player_index

    @property
    def move_history(self) -> List[Move]:
        """Get the move history."""
        return self._move_history.copy()

    @property
    def game_status(self) -> GameStatus:
        """Get the current game status."""
        return self._game_status

    def get_current_player(self) -> Player:
        """
        Get the current player.

        Returns:
            The player whose turn it is
        """
        return self._players[self._current_player_index]

    def get_opponent_player(self) -> Player:
        """
        Get the opponent of the current player.

        Returns:
            The player who is not currently playing
        """
        opponent_index = 1 - self._current_player_index
        return self._players[opponent_index]

    def _switch_turn(self) -> None:
        """Switch to the next player's turn."""
        self._current_player_index = 1 - self._current_player_index

    def is_game_over(self) -> bool:
        """
        Check if the game is over.

        Returns:
            True if game is over, False otherwise
        """
        return self._game_status != GameStatus.ONGOING

    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game.

        Returns:
            The winning player, or None if game is ongoing or draw
        """
        if self._game_status == GameStatus.PLAYER_ONE_WINS:
            return self._players[0]
        elif self._game_status == GameStatus.PLAYER_TWO_WINS:
            return self._players[1]
        return None

    def can_undo(self) -> bool:
        """
        Check if undo is available.

        Returns:
            True if there are moves to undo, False otherwise
        """
        return len(self._game_states) > 0

    def undo_move(self) -> bool:
        """
        Undo the last move and restore the previous game state.

        This method restores the board state, current player, and removes
        the last move from history. Can undo up to MAX_UNDO_MOVES moves.

        Returns:
            True if undo was successful, False if no moves to undo

        Raises:
            GameOverException: If attempting to undo after game is over
        """
        # Cannot undo after game is over
        if self.is_game_over():
            raise GameOverException("Cannot undo moves after game is over")

        # Check if there are moves to undo
        if not self.can_undo():
            return False

        # Get the last saved state
        last_state = self._game_states.pop()

        # Restore the board state
        last_state.restore_to_board(self._board)

        # Restore current player
        self._current_player_index = last_state.current_player_index

        # Remove the last move from history
        if len(self._move_history) > 0:
            removed_move = self._move_history.pop()

            # If a piece was captured, restore it to the opponent's collection
            if removed_move.captured_piece is not None:
                opponent = self.get_opponent_player()
                opponent.add_piece(removed_move.captured_piece)

        return True

    def make_move(self, from_pos: Position, to_pos: Position) -> MoveResult:
        """
        Execute a move from one position to another.

        This method performs comprehensive validation and executes the move
        if valid, including capturing pieces and updating game state.

        Args:
            from_pos: The source position
            to_pos: The target position

        Returns:
            MoveResult indicating success or failure with a message

        Raises:
            GameOverException: If attempting to move after game is over
        """
        # Check if game is over
        if self.is_game_over():
            raise GameOverException("Cannot make moves after game is over")

        # Validate source position
        if not self._board.is_valid_position(from_pos):
            return MoveResult(False, f"Invalid source position: {from_pos}")

        # Validate target position
        if not self._board.is_valid_position(to_pos):
            return MoveResult(False, f"Invalid target position: {to_pos}")

        # Get the piece at source position
        piece = self._board.get_piece(from_pos)
        if piece is None:
            return MoveResult(False, f"No piece at position {from_pos}")

        # Check if piece belongs to current player
        current_player = self.get_current_player()
        if piece.owner != current_player:
            return MoveResult(
                False,
                f"Piece at {from_pos} belongs to {piece.owner.name}, "
                f"not {current_player.name}"
            )

        # Check if the piece can move to target position
        if not piece.can_move_to(self._board, to_pos):
            return MoveResult(
                False,
                f"{piece.__class__.__name__} at {from_pos} cannot move to {to_pos}"
            )

        # Check if there's a piece at target position
        target_piece = self._board.get_piece(to_pos)
        captured_piece = None

        if target_piece is not None:
            # Cannot capture own pieces (should be caught by can_move_to, but double-check)
            if target_piece.owner == current_player:
                return MoveResult(False, "Cannot capture your own piece")

            # Check if capture is allowed
            if not piece.can_capture(target_piece, self._board):
                return MoveResult(
                    False,
                    f"{piece.__class__.__name__} cannot capture "
                    f"{target_piece.__class__.__name__}"
                )

            captured_piece = target_piece

        # Save current game state for undo functionality
        self._save_game_state()

        # Execute the move
        self._board.set_piece(from_pos, None)
        self._board.set_piece(to_pos, piece)
        piece.position = to_pos

        # Handle capture
        if captured_piece is not None:
            opponent = self.get_opponent_player()
            opponent.remove_piece(captured_piece)

        # Record the move
        move = Move(
            piece=piece,
            from_pos=from_pos,
            to_pos=to_pos,
            captured_piece=captured_piece,
            timestamp=datetime.now()
        )
        self._move_history.append(move)

        # Check for victory conditions before switching turn
        self._check_victory_conditions(to_pos, current_player)

        # Switch turn (only if game is not over)
        if not self.is_game_over():
            self._switch_turn()

        # Build success message
        message = f"{piece.__class__.__name__} moved from {from_pos} to {to_pos}"
        if captured_piece is not None:
            message += f" (captured {captured_piece.__class__.__name__})"

        return MoveResult(True, message, captured_piece)

    def _save_game_state(self) -> None:
        """
        Save the current game state for undo functionality.

        Maintains a maximum of MAX_UNDO_MOVES states.
        """
        state = GameState.capture_from_board(
            self._board,
            self._current_player_index,
            len(self._move_history)
        )
        self._game_states.append(state)

        # Keep only the last MAX_UNDO_MOVES states
        if len(self._game_states) > self.MAX_UNDO_MOVES:
            self._game_states.pop(0)

    def _check_victory_conditions(self, last_move_pos: Position, current_player: Player) -> None:
        """
        Check if victory conditions are met after a move.

        Victory conditions:
        1. A piece reaches the opponent's den
        2. All opponent pieces are captured

        Args:
            last_move_pos: The position where the piece just moved
            current_player: The player who just made the move
        """
        opponent = self.get_opponent_player()

        # Check if piece reached opponent's den
        if self._board.is_den(last_move_pos, opponent):
            # Current player wins by reaching opponent's den
            if current_player == self._players[0]:
                self._game_status = GameStatus.PLAYER_ONE_WINS
            else:
                self._game_status = GameStatus.PLAYER_TWO_WINS
            return

        # Check if opponent has no pieces left
        if not opponent.has_pieces():
            # Current player wins by capturing all opponent pieces
            if current_player == self._players[0]:
                self._game_status = GameStatus.PLAYER_ONE_WINS
            else:
                self._game_status = GameStatus.PLAYER_TWO_WINS
            return

    def __str__(self) -> str:
        """String representation of the game."""
        return (
            f"Game(current_player={self.get_current_player()}, "
            f"status={self._game_status.value}, "
            f"moves={len(self._move_history)})"
        )

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return self.__str__()
