"""
FileManager class for Jungle Game.
Handles file operations for save/load and record functionality.
"""

import json
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from model.game import Game
from model.position import Position
from model.enums import PlayerColor, GameStatus
from model.exceptions import FileOperationException, ValidationException
from utils.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class FileManager:
    """
    Handles file operations for save/load and records.

    Manages serialization and deserialization of game states to .jungle files
    and move history to .record files.
    """

    JUNGLE_VERSION = "1.0"
    RECORD_VERSION = "1.0"

    @staticmethod
    def validate_filename(filename: str, expected_extension: str) -> Path:
        """
        Validate and normalize a filename.

        Args:
            filename: The filename to validate
            expected_extension: Expected file extension (e.g., '.jungle')

        Returns:
            Path object with validated filename

        Raises:
            ValidationException: If filename is invalid
        """
        if not filename or not filename.strip():
            raise ValidationException(
                f"Filename cannot be empty. Please provide a valid filename with {expected_extension} extension."
            )

        filepath = Path(filename.strip())

        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in filepath.name for char in invalid_chars):
            raise ValidationException(
                f"Filename contains invalid characters. "
                f"Avoid using: {', '.join(invalid_chars)}"
            )

        # Ensure correct extension
        if filepath.suffix != expected_extension:
            filepath = filepath.with_suffix(expected_extension)

        return filepath

    @staticmethod
    def save_game(game: Game, filename: str) -> bool:
        """
        Save the current game state to a .jungle file.

        Args:
            game: The game instance to save
            filename: Path to the save file (should end with .jungle)

        Returns:
            True if save was successful, False otherwise

        Raises:
            FileOperationException: If file operation fails
        """
        try:
            logger.info(f"Saving game to {filename}")
            
            # Ensure filename has .jungle extension
            filepath = Path(filename)
            if filepath.suffix != '.jungle':
                filepath = filepath.with_suffix('.jungle')
                logger.debug(f"Added .jungle extension: {filepath}")

            # Build game state dictionary
            game_data = {
                'version': FileManager.JUNGLE_VERSION,
                'players': [
                    {
                        'name': player.name,
                        'color': player.color.value
                    }
                    for player in game.players
                ],
                'current_player': game.current_player_index,
                'board_state': FileManager._serialize_board(game),
                'move_history': [
                    move.to_dict() for move in game.move_history
                ],
                'game_status': game.game_status.value
            }
            
            logger.debug(f"Serialized game data: {len(game_data['move_history'])} moves, "
                        f"{len(game_data['board_state'])} pieces")

            # Write to file with backup
            if filepath.exists():
                backup_path = filepath.with_suffix('.jungle.bak')
                filepath.rename(backup_path)
                logger.debug(f"Created backup: {backup_path}")

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=2)

            # Remove backup if save successful
            backup_path = filepath.with_suffix('.jungle.bak')
            if backup_path.exists():
                backup_path.unlink()
                logger.debug("Removed backup file")

            logger.info(f"Game saved successfully to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save game to {filename}: {e}", exc_info=True)
            raise FileOperationException(
                f"Failed to save game to {filename}: {str(e)}"
            ) from e

    @staticmethod
    def _serialize_board(game: Game) -> Dict[str, Dict[str, Any]]:
        """
        Serialize the board state to a dictionary.

        Args:
            game: The game instance

        Returns:
            Dictionary mapping position strings to piece data
        """
        board_state = {}

        for row in range(game.board.BOARD_HEIGHT):
            for col in range(game.board.BOARD_WIDTH):
                pos = Position(row, col)
                piece = game.board.get_piece(pos)

                if piece is not None:
                    pos_key = f"{row},{col}"
                    board_state[pos_key] = {
                        'piece': piece.__class__.__name__,
                        'owner': piece.owner.color.value,
                        'rank': piece.rank
                    }

        return board_state

    @staticmethod
    def load_game(filename: str) -> Optional[Game]:
        """
        Load a game state from a .jungle file.

        Args:
            filename: Path to the save file

        Returns:
            Game instance if load was successful, None otherwise

        Raises:
            FileOperationException: If file operation or validation fails
        """
        try:
            filepath = Path(filename)

            if not filepath.exists():
                raise FileOperationException(f"File not found: {filename}")

            if filepath.suffix != '.jungle':
                raise FileOperationException(
                    f"Invalid file extension: expected .jungle, got {filepath.suffix}"
                )

            with open(filepath, 'r', encoding='utf-8') as f:
                game_data = json.load(f)

            # Validate version
            if game_data.get('version') != FileManager.JUNGLE_VERSION:
                raise FileOperationException(
                    f"Unsupported file version: {game_data.get('version')}"
                )

            # Create game with player names
            player_data = game_data['players']
            game = Game(
                player1_name=player_data[0]['name'],
                player2_name=player_data[1]['name']
            )

            # Clear the board (we'll restore from saved state)
            FileManager._clear_board(game)

            # Restore board state
            FileManager._deserialize_board(game, game_data['board_state'])

            # Restore current player
            game._current_player_index = game_data['current_player']

            # Restore game status
            game._game_status = GameStatus(game_data['game_status'])

            # Note: We don't restore move_history or game_states for undo
            # as those are for the current session only

            return game

        except json.JSONDecodeError as e:
            raise FileOperationException(
                f"Invalid JSON in file {filename}: {str(e)}"
            ) from e
        except Exception as e:
            raise FileOperationException(
                f"Failed to load game from {filename}: {str(e)}"
            ) from e

    @staticmethod
    def _clear_board(game: Game) -> None:
        """
        Clear all pieces from the board and player collections.

        Args:
            game: The game instance
        """
        # Clear board grid
        for row in range(game.board.BOARD_HEIGHT):
            for col in range(game.board.BOARD_WIDTH):
                pos = Position(row, col)
                game.board.set_piece(pos, None)

        # Clear player piece collections
        for player in game.players:
            player._pieces.clear()

    @staticmethod
    def _deserialize_board(game: Game, board_state: Dict[str, Dict[str, Any]]) -> None:
        """
        Restore the board state from a dictionary.

        Args:
            game: The game instance
            board_state: Dictionary mapping position strings to piece data

        Raises:
            FileOperationException: If piece data is invalid
        """
        from model.piece import (
            Rat, Cat, Dog, Wolf, Leopard, Tiger, Lion, Elephant
        )

        piece_classes = {
            'Rat': Rat,
            'Cat': Cat,
            'Dog': Dog,
            'Wolf': Wolf,
            'Leopard': Leopard,
            'Tiger': Tiger,
            'Lion': Lion,
            'Elephant': Elephant
        }

        for pos_key, piece_data in board_state.items():
            # Parse position
            row, col = map(int, pos_key.split(','))
            pos = Position(row, col)

            # Get piece class
            piece_name = piece_data['piece']
            if piece_name not in piece_classes:
                raise FileOperationException(f"Unknown piece type: {piece_name}")

            # Get owner
            owner_color = PlayerColor(piece_data['owner'])
            owner = None
            for player in game.players:
                if player.color == owner_color:
                    owner = player
                    break

            if owner is None:
                raise FileOperationException(f"Invalid owner color: {owner_color}")

            # Create piece
            piece_class = piece_classes[piece_name]
            piece = piece_class(owner, pos)

            # Validate rank
            if piece.rank != piece_data['rank']:
                raise FileOperationException(
                    f"Rank mismatch for {piece_name}: "
                    f"expected {piece_data['rank']}, got {piece.rank}"
                )

            # Place piece on board and add to player
            game.board.set_piece(pos, piece)
            owner.add_piece(piece)

    @staticmethod
    def save_record(game: Game, filename: str) -> bool:
        """
        Save the game record (move history) to a .record file.

        Args:
            game: The game instance to record
            filename: Path to the record file (should end with .record)

        Returns:
            True if save was successful, False otherwise

        Raises:
            FileOperationException: If file operation fails
        """
        try:
            # Ensure filename has .record extension
            filepath = Path(filename)
            if filepath.suffix != '.record':
                filepath = filepath.with_suffix('.record')

            # Build record content
            lines = []
            lines.append(f"JUNGLE_GAME_RECORD_V{FileManager.RECORD_VERSION}")
            lines.append(
                f"Players: {game.players[0].name} ({game.players[0].color.value.title()}), "
                f"{game.players[1].name} ({game.players[1].color.value.title()})"
            )

            # Add start time (use first move timestamp or current time)
            if game.move_history:
                start_time = game.move_history[0].timestamp
            else:
                start_time = datetime.now()
            lines.append(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Add moves
            for i, move in enumerate(game.move_history, 1):
                lines.append(f"Move {i}: {move.to_record_string()}")

            # Add game result
            if game.is_game_over():
                winner = game.get_winner()
                if winner:
                    lines.append(f"Game Result: {winner.name} Wins")
                else:
                    lines.append("Game Result: Draw")

                # Add end time (use last move timestamp)
                if game.move_history:
                    end_time = game.move_history[-1].timestamp
                    lines.append(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                lines.append("Game Result: In Progress")

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            return True

        except Exception as e:
            raise FileOperationException(
                f"Failed to save record to {filename}: {str(e)}"
            ) from e

    @staticmethod
    def load_record(filename: str) -> Optional[List[Dict[str, Any]]]:
        """
        Load a game record from a .record file.

        Args:
            filename: Path to the record file

        Returns:
            List of move dictionaries if load was successful, None otherwise

        Raises:
            FileOperationException: If file operation or validation fails
        """
        try:
            filepath = Path(filename)

            if not filepath.exists():
                raise FileOperationException(f"File not found: {filename}")

            if filepath.suffix != '.record':
                raise FileOperationException(
                    f"Invalid file extension: expected .record, got {filepath.suffix}"
                )

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines:
                raise FileOperationException("Record file is empty")

            # Validate version
            version_line = lines[0].strip()
            if not version_line.startswith("JUNGLE_GAME_RECORD_V"):
                raise FileOperationException("Invalid record file format")

            # Parse moves
            moves = []
            for line in lines:
                line = line.strip()
                if line.startswith("Move "):
                    # Extract move number and move string
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        move_str = parts[1]
                        try:
                            from model.move import Move
                            move_data = Move.parse_record_string(move_str)
                            moves.append(move_data)
                        except ValueError as e:
                            raise FileOperationException(
                                f"Invalid move format: {move_str}"
                            ) from e

            return moves

        except Exception as e:
            if isinstance(e, FileOperationException):
                raise
            raise FileOperationException(
                f"Failed to load record from {filename}: {str(e)}"
            ) from e

    @staticmethod
    def replay_record(filename: str, player1_name: str = None,
                      player2_name: str = None) -> Optional[Game]:
        """
        Replay a game from a .record file.

        Creates a new game and replays all moves from the record file.

        Args:
            filename: Path to the record file
            player1_name: Optional name for player 1 (defaults to name from record)
            player2_name: Optional name for player 2 (defaults to name from record)

        Returns:
            Game instance with all moves replayed, or None if replay fails

        Raises:
            FileOperationException: If file operation or replay fails
        """
        try:
            filepath = Path(filename)

            if not filepath.exists():
                raise FileOperationException(f"File not found: {filename}")

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines:
                raise FileOperationException("Record file is empty")

            # Parse player names from file if not provided
            if player1_name is None or player2_name is None:
                for line in lines:
                    if line.startswith("Players:"):
                        # Format: "Players: Name1 (Color1), Name2 (Color2)"
                        players_str = line.split(":", 1)[1].strip()
                        player_parts = players_str.split(", ")

                        if len(player_parts) == 2:
                            # Extract names (remove color in parentheses)
                            import re
                            name1 = re.sub(r'\s*\([^)]*\)', '', player_parts[0]).strip()
                            name2 = re.sub(r'\s*\([^)]*\)', '', player_parts[1]).strip()

                            if player1_name is None:
                                player1_name = name1
                            if player2_name is None:
                                player2_name = name2
                        break

            # Use default names if still not found
            if player1_name is None:
                player1_name = "Player 1"
            if player2_name is None:
                player2_name = "Player 2"

            # Create new game
            game = Game(player1_name, player2_name)

            # Parse and replay moves
            for line in lines:
                line = line.strip()
                if line.startswith("Move "):
                    # Extract move string
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        move_str = parts[1]
                        try:
                            from model.move import Move
                            move_data = Move.parse_record_string(move_str)

                            # Execute the move
                            from_pos = Position(
                                move_data['from_row'],
                                move_data['from_col']
                            )
                            to_pos = Position(
                                move_data['to_row'],
                                move_data['to_col']
                            )

                            result = game.make_move(from_pos, to_pos)
                            if not result.success:
                                raise FileOperationException(
                                    f"Failed to replay move: {result.message}"
                                )

                        except ValueError as e:
                            raise FileOperationException(
                                f"Invalid move format: {move_str}"
                            ) from e

            return game

        except Exception as e:
            if isinstance(e, FileOperationException):
                raise
            raise FileOperationException(
                f"Failed to replay record from {filename}: {str(e)}"
            ) from e
