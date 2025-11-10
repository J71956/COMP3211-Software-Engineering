"""
GameView class for Jungle Game.
Handles comprehensive game state display including current player,
move history, and game information presentation.
"""

from typing import TYPE_CHECKING
from view.board_renderer import BoardRenderer

if TYPE_CHECKING:
    from model.game import Game


class GameView:
    """
    Main view coordinator for displaying complete game state.

    Provides comprehensive game status display including:
    - Current board state with pieces and terrain
    - Current player information
    - Move history
    - Game status and winner information
    - Formatted output for different game phases

    Attributes:
        board_renderer: BoardRenderer instance for board visualization
    """

    def __init__(self):
        """Initialize the GameView with a BoardRenderer."""
        self.board_renderer = BoardRenderer()

    def display_game_state(self, game: 'Game') -> str:
        """
        Display the complete game state.

        Shows the board, current player, game status, and move history.

        Args:
            game: The game instance to display

        Returns:
            Formatted string representation of the complete game state
        """
        lines = []

        # Display game header
        lines.append("=" * 50)
        lines.append("JUNGLE GAME")
        lines.append("=" * 50)
        lines.append("")

        # Display current game status
        lines.append(self._format_game_status(game))
        lines.append("")

        # Display the board
        lines.append(self.board_renderer.render_board(game.board))
        lines.append("")

        # Display move history if any moves have been made
        if len(game.move_history) > 0:
            lines.append(self._format_move_history(game))
            lines.append("")

        # Display undo availability
        if game.can_undo():
            # Count available undo moves from move history (max 3)
            undo_count = min(len(game.move_history), game.MAX_UNDO_MOVES)
            lines.append(f"Undo available: {undo_count} move(s) can be undone")
        else:
            lines.append("Undo not available")

        lines.append("")

        return "\n".join(lines)

    def _format_game_status(self, game: 'Game') -> str:
        """
        Format the current game status.

        Args:
            game: The game instance

        Returns:
            Formatted game status string
        """
        lines = []

        # Display players
        players = game.players
        lines.append(f"Players: {players[0]} vs {players[1]}")

        # Display current player or winner
        if game.is_game_over():
            winner = game.get_winner()
            if winner:
                lines.append(f"Game Over - Winner: {winner}")
            else:
                lines.append("Game Over - Draw")
        else:
            current_player = game.get_current_player()
            lines.append(f"Current Turn: {current_player}")

            # Display piece counts
            red_pieces = len(players[0].get_active_pieces())
            blue_pieces = len(players[1].get_active_pieces())
            lines.append(f"Pieces Remaining: {players[0].name}={red_pieces}, {players[1].name}={blue_pieces}")

        return "\n".join(lines)

    def _format_move_history(self, game: 'Game', max_recent_moves: int = 5) -> str:
        """
        Format the move history for display.

        Args:
            game: The game instance
            max_recent_moves: Maximum number of recent moves to display

        Returns:
            Formatted move history string
        """
        lines = []
        lines.append("Recent Moves:")
        lines.append("-" * 50)

        move_history = game.move_history
        total_moves = len(move_history)

        # Show only the most recent moves
        start_index = max(0, total_moves - max_recent_moves)
        recent_moves = move_history[start_index:]

        for i, move in enumerate(recent_moves, start=start_index + 1):
            move_str = f"{i}. {move.to_record_string()}"
            lines.append(move_str)

        if total_moves > max_recent_moves:
            lines.append(f"... ({total_moves - max_recent_moves} earlier moves)")

        return "\n".join(lines)

    def display_welcome_message(self) -> str:
        """
        Display welcome message at game start.

        Returns:
            Formatted welcome message
        """
        lines = []
        lines.append("=" * 50)
        lines.append("WELCOME TO JUNGLE GAME")
        lines.append("=" * 50)
        lines.append("")
        lines.append("A strategic board game where animals battle for territory!")
        lines.append("")
        lines.append(self.board_renderer.render_terrain_markers())
        lines.append("")
        lines.append("Commands:")
        lines.append("  move <from_row> <from_col> <to_row> <to_col> - Make a move")
        lines.append("  undo - Undo the last move")
        lines.append("  save <filename> - Save the game")
        lines.append("  load <filename> - Load a saved game")
        lines.append("  quit - Exit the game")
        lines.append("")
        lines.append("=" * 50)
        lines.append("")

        return "\n".join(lines)

    def display_game_over(self, game: 'Game') -> str:
        """
        Display game over message with winner information.

        Args:
            game: The game instance

        Returns:
            Formatted game over message
        """
        lines = []
        lines.append("")
        lines.append("=" * 50)
        lines.append("GAME OVER")
        lines.append("=" * 50)
        lines.append("")

        winner = game.get_winner()
        if winner:
            lines.append(f"🏆 Winner: {winner} 🏆")
        else:
            lines.append("Game ended in a draw")

        lines.append("")
        lines.append(f"Total moves: {len(game.move_history)}")
        lines.append("")

        # Display final board state
        lines.append("Final Board State:")
        lines.append(self.board_renderer.render_board(game.board))
        lines.append("")

        lines.append("=" * 50)
        lines.append("")

        return "\n".join(lines)

    def display_move_result(self, result: 'MoveResult') -> str:
        """
        Display the result of a move attempt.

        Args:
            result: The MoveResult from a move attempt

        Returns:
            Formatted move result message
        """
        if result.success:
            return f"✓ {result.message}"
        return f"✗ {result.message}"

    def display_error(self, message: str) -> str:
        """
        Display an error message.

        Args:
            message: The error message to display

        Returns:
            Formatted error message
        """
        return f"ERROR: {message}"

    def display_info(self, message: str) -> str:
        """
        Display an informational message.

        Args:
            message: The informational message to display

        Returns:
            Formatted info message
        """
        return f"INFO: {message}"

    def display_undo_result(self, success: bool) -> str:
        """
        Display the result of an undo operation.

        Args:
            success: Whether the undo was successful

        Returns:
            Formatted undo result message
        """
        if success:
            return "✓ Move undone successfully"
        return "✗ No moves to undo"
