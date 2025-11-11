"""
GameController class for Jungle Game.
Main game controller and command processor.
"""

from typing import Optional
from model.game import Game
from model.exceptions import (
    JungleGameException,
    GameOverException,
    FileOperationException,
    InvalidInputException,
    InvalidPositionException,
    PieceNotFoundException,
    WrongPlayerException,
    InvalidMoveException,
    InvalidCaptureException,
    ValidationException
)
from view.game_view import GameView
from controller.command_parser import CommandParser
from controller.file_manager import FileManager
from controller.name_manager import NameManager
from utils.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class GameController:
    """
    Main game controller and command processor.

    Manages the game loop, processes user commands, and coordinates
    between the model (Game) and view (GameView).

    Attributes:
        game: The current game instance
        view: The game view for display
        command_parser: Parser for user input
        file_manager: Manager for file operations
        running: Flag indicating if the game loop is running
    """

    def __init__(self, game: Optional[Game] = None):
        """
        Initialize the GameController.

        Args:
            game: Optional existing game instance. If None, a new game will be created.
        """
        self.game = game
        self.view = GameView()
        self.command_parser = CommandParser()
        self.file_manager = FileManager()
        self.running = False

    def run_game_loop(self) -> None:
        """
        Run the main game loop.

        Displays the welcome message, processes commands, and handles
        game flow until the user quits or the game ends.
        """
        self.running = True
        logger.info("Game loop started")

        # Display welcome message
        print(self.view.display_welcome_message())

        # Create new game if not already loaded
        if self.game is None:
            logger.info("Creating new game - prompting for player names")
            player1_name, player2_name = NameManager.get_player_names()
            self.game = Game(player1_name, player2_name)
            logger.info(f"New game created: {player1_name} vs {player2_name}")

        # Main game loop
        while self.running:
            try:
                # Display current game state
                print(self.view.display_game_state(self.game))

                # Check if game is over
                if self.game.is_game_over():
                    logger.info(f"Game over detected: {self.game.game_status}")
                    print(self.view.display_game_over(self.game))
                    self._handle_game_over()
                    continue

                # Get user input
                command = input(f"{self.game.get_current_player().name}> ").strip()

                if not command:
                    continue

                logger.debug(f"Processing command: {command}")
                # Process command
                self.process_command(command)

            except KeyboardInterrupt:
                logger.info("Game interrupted by user (KeyboardInterrupt)")
                print("\n")
                print(self.view.display_info("Game interrupted by user"))
                self._handle_quit_command()
                break
            except Exception as e:
                logger.error(f"Unexpected error in game loop: {e}", exc_info=True)
                print(self.view.display_error(f"Unexpected error: {str(e)}"))

        logger.info("Game loop ended")
        print(self.view.display_info("Thank you for playing Jungle Game!"))

    def process_command(self, command: str) -> bool:
        """
        Process a user command.

        Routes the command to the appropriate handler method.

        Args:
            command: The command string to process

        Returns:
            True if command was processed successfully, False otherwise
        """
        if not command:
            return False

        # Parse command into parts
        parts = command.lower().split()
        cmd = parts[0]

        try:
            # Route to appropriate handler
            if cmd in ['move', 'm'] or self.command_parser.validate_command_format(command):
                return self._handle_move_command(command)
            elif cmd in ['undo', 'u']:
                return self._handle_undo_command()
            elif cmd in ['save', 's']:
                return self._handle_save_command(parts)
            elif cmd in ['load', 'l']:
                return self._handle_load_command(parts)
            elif cmd in ['record', 'rec']:
                return self._handle_record_command(parts)
            elif cmd in ['replay', 'rep']:
                return self._handle_replay_command(parts)
            elif cmd in ['quit', 'q', 'exit']:
                return self._handle_quit_command()
            elif cmd in ['help', 'h', '?']:
                return self._handle_help_command()
            else:
                print(self.view.display_error(
                    f"Unknown command: {cmd}. Type 'help' for available commands."
                ))
                return False

        except JungleGameException as e:
            print(self.view.display_error(str(e)))
            return False

    def _handle_move_command(self, command: str) -> bool:
        """
        Handle a move command with comprehensive error handling.

        Args:
            command: The move command string

        Returns:
            True if move was successful, False otherwise
        """
        try:
            # Parse the move command
            from_pos, to_pos = self.command_parser.parse_move_command(command)
            logger.debug(f"Parsed move: {from_pos} -> {to_pos}")

            # Execute the move
            result = self.game.make_move(from_pos, to_pos)
            
            if result.success:
                logger.info(f"Move executed: {result.message}")
            else:
                logger.warning(f"Move failed: {result.message}")

            # Display result
            print(self.view.display_move_result(result))

            return result.success

        except InvalidInputException as e:
            logger.debug(f"Invalid input: {e}")
            print(self.view.display_error(f"Invalid input: {e}"))
            return False
        except InvalidPositionException as e:
            logger.debug(f"Invalid position: {e}")
            print(self.view.display_error(f"Invalid position: {e}"))
            return False
        except PieceNotFoundException as e:
            logger.debug(f"No piece found: {e}")
            print(self.view.display_error(f"No piece found: {e}"))
            return False
        except WrongPlayerException as e:
            logger.debug(f"Wrong player: {e}")
            print(self.view.display_error(f"Wrong player: {e}"))
            return False
        except InvalidMoveException as e:
            logger.debug(f"Invalid move: {e}")
            print(self.view.display_error(f"Invalid move: {e}"))
            return False
        except InvalidCaptureException as e:
            logger.debug(f"Invalid capture: {e}")
            print(self.view.display_error(f"Invalid capture: {e}"))
            return False
        except GameOverException as e:
            logger.warning(f"Game over exception: {e}")
            print(self.view.display_error(str(e)))
            return False
        except ValueError as e:
            logger.debug(f"Value error: {e}")
            print(self.view.display_error(f"Input error: {e}"))
            return False

    def _handle_undo_command(self) -> bool:
        """
        Handle an undo command.

        Returns:
            True if undo was successful, False otherwise
        """
        try:
            success = self.game.undo_move()
            print(self.view.display_undo_result(success))
            return success

        except GameOverException as e:
            print(self.view.display_error(str(e)))
            return False

    def _handle_save_command(self, parts: list) -> bool:
        """
        Handle a save command with validation.

        Args:
            parts: Command parts (e.g., ['save', 'filename'])

        Returns:
            True if save was successful, False otherwise
        """
        if len(parts) < 2:
            print(self.view.display_error(
                "Usage: save <filename>\n"
                "Example: save mygame.jungle"
            ))
            return False

        filename = parts[1]

        try:
            success = self.file_manager.save_game(self.game, filename)
            if success:
                print(self.view.display_info(f"Game saved to {filename}"))
            return success

        except ValidationException as e:
            print(self.view.display_error(f"Validation error: {e}"))
            return False
        except FileOperationException as e:
            print(self.view.display_error(f"File operation failed: {e}"))
            return False

    def _handle_load_command(self, parts: list) -> bool:
        """
        Handle a load command with validation.

        Args:
            parts: Command parts (e.g., ['load', 'filename'])

        Returns:
            True if load was successful, False otherwise
        """
        if len(parts) < 2:
            print(self.view.display_error(
                "Usage: load <filename>\n"
                "Example: load mygame.jungle"
            ))
            return False

        filename = parts[1]

        try:
            loaded_game = self.file_manager.load_game(filename)
            if loaded_game:
                self.game = loaded_game
                print(self.view.display_info(f"Game loaded from {filename}"))
                return True
            return False

        except ValidationException as e:
            print(self.view.display_error(f"Validation error: {e}"))
            return False
        except FileOperationException as e:
            print(self.view.display_error(f"File operation failed: {e}"))
            return False

    def _handle_record_command(self, parts: list) -> bool:
        """
        Handle a record command to save game history with validation.

        Args:
            parts: Command parts (e.g., ['record', 'filename'])

        Returns:
            True if record was saved successfully, False otherwise
        """
        if len(parts) < 2:
            print(self.view.display_error(
                "Usage: record <filename>\n"
                "Example: record mygame.record"
            ))
            return False

        filename = parts[1]

        try:
            success = self.file_manager.save_record(self.game, filename)
            if success:
                print(self.view.display_info(f"Game record saved to {filename}"))
            return success

        except ValidationException as e:
            print(self.view.display_error(f"Validation error: {e}"))
            return False
        except FileOperationException as e:
            print(self.view.display_error(f"File operation failed: {e}"))
            return False

    def _handle_replay_command(self, parts: list) -> bool:
        """
        Handle a replay command to load and replay a game record with validation.

        Args:
            parts: Command parts (e.g., ['replay', 'filename'])

        Returns:
            True if replay was successful, False otherwise
        """
        if len(parts) < 2:
            print(self.view.display_error(
                "Usage: replay <filename>\n"
                "Example: replay mygame.record"
            ))
            return False

        filename = parts[1]

        try:
            replayed_game = self.file_manager.replay_record(filename)
            if replayed_game:
                self.game = replayed_game
                print(self.view.display_info(f"Game replayed from {filename}"))
                return True
            return False

        except ValidationException as e:
            print(self.view.display_error(f"Validation error: {e}"))
            return False
        except FileOperationException as e:
            print(self.view.display_error(f"File operation failed: {e}"))
            return False

    def _handle_quit_command(self) -> bool:
        """
        Handle a quit command.

        Returns:
            True (always successful)
        """
        # Ask for confirmation if game is in progress
        if self.game and not self.game.is_game_over() and len(self.game.move_history) > 0:
            response = input("Game in progress. Are you sure you want to quit? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                print(self.view.display_info("Quit cancelled"))
                return False

        self.running = False
        return True

    def _handle_help_command(self) -> bool:
        """
        Handle a help command to display available commands.

        Returns:
            True (always successful)
        """
        help_text = """
Available Commands:
  move <from> <to>  - Make a move (e.g., 'move a0 b0' or 'move 0,0 1,0')
  undo              - Undo the last move (up to 3 moves)
  save <filename>   - Save the current game to a file
  load <filename>   - Load a saved game from a file
  record <filename> - Save the game record (move history) to a file
  replay <filename> - Replay a game from a record file
  help              - Display this help message
  quit              - Exit the game

Move Format Examples:
  - Chess notation: a0 b0, A0 B0
  - Coordinate notation: 0,0 1,0 or (0,0) (1,0)
  - Verbose: move from a0 to b0

Shortcuts:
  m - move, u - undo, s - save, l - load, q - quit, h - help
"""
        print(help_text)
        return True

    def _handle_game_over(self) -> None:
        """
        Handle game over state.

        Prompts user for actions after game ends.
        """
        response = input("Game over. Would you like to (s)ave record, (n)ew game, or (q)uit? ").strip().lower()

        if response in ['s', 'save']:
            filename = input("Enter filename for record: ").strip()
            if filename:
                self._handle_record_command(['record', filename])

        if response in ['n', 'new']:
            # Start a new game
            player1_name, player2_name = NameManager.get_player_names()
            self.game = Game(player1_name, player2_name)
            print(self.view.display_info("New game started!"))
        else:
            # Quit
            self.running = False
