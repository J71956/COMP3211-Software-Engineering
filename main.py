#!/usr/bin/env python3
"""
Main entry point for the Jungle Game application.

This module provides the command-line interface for starting and managing
the Jungle Game, including options for loading saved games and replaying
game records.
"""

import sys
import argparse
import logging
from typing import Optional

from controller.game_controller import GameController
from controller.file_manager import FileManager
from model.exceptions import FileOperationException
from utils.logger import GameLogger, get_logger

# Initialize logger for this module
logger = get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Jungle Game - A strategic board game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start a new game
  python main.py --load game.jungle # Load a saved game
  python main.py --replay game.record # Replay a game record
  python main.py --debug            # Enable debug logging
        """
    )

    # Game options
    game_group = parser.add_mutually_exclusive_group()
    game_group.add_argument(
        '--load', '-l',
        metavar='FILE',
        help='Load a saved game from a .jungle file'
    )
    game_group.add_argument(
        '--replay', '-r',
        metavar='FILE',
        help='Replay a game from a .record file'
    )

    # Player names
    parser.add_argument(
        '--player1',
        metavar='NAME',
        help='Name for player 1 (Red)'
    )
    parser.add_argument(
        '--player2',
        metavar='NAME',
        help='Name for player 2 (Blue)'
    )

    # Logging options
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--log-file',
        action='store_true',
        default=True,
        help='Enable logging to file (default: enabled)'
    )
    parser.add_argument(
        '--no-log-file',
        action='store_false',
        dest='log_file',
        help='Disable logging to file'
    )

    # Version
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Jungle Game 1.0'
    )

    return parser.parse_args()


def initialize_game(args: argparse.Namespace) -> Optional[GameController]:
    """
    Initialize the game based on command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Initialized GameController, or None if initialization failed
    """
    file_manager = FileManager()

    try:
        # Load saved game
        if args.load:
            logger.info(f"Loading game from {args.load}")
            print(f"Loading game from {args.load}...")
            game = file_manager.load_game(args.load)
            if game is None:
                logger.error(f"Failed to load game from {args.load}")
                print(f"Error: Failed to load game from {args.load}")
                return None
            logger.info("Game loaded successfully")
            print("Game loaded successfully!")
            return GameController(game)

        # Replay game record
        if args.replay:
            logger.info(f"Replaying game from {args.replay}")
            print(f"Replaying game from {args.replay}...")
            game = file_manager.replay_record(args.replay)
            if game is None:
                logger.error(f"Failed to replay game from {args.replay}")
                print(f"Error: Failed to replay game from {args.replay}")
                return None
            logger.info("Game replay loaded successfully")
            print("Game replay loaded successfully!")
            return GameController(game)

        # Start new game
        logger.info("Starting new game")
        return GameController()

    except FileOperationException as e:
        logger.error(f"File operation error: {e}", exc_info=True)
        print(f"Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {e}", exc_info=True)
        print(f"Unexpected error during initialization: {e}")
        return None


def main() -> int:
    """
    Main application entry point.

    Handles application startup, initialization, and cleanup.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Initialize logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    GameLogger.initialize(
        level=log_level,
        log_to_file=args.log_file,
        log_to_console=False,  # Don't log to console to avoid cluttering game output
        detailed=args.debug
    )
    
    logger.info("=" * 60)
    logger.info("Jungle Game application started")
    logger.info(f"Log level: {'DEBUG' if args.debug else 'INFO'}")
    logger.info(f"Log to file: {args.log_file}")
    if args.log_file:
        log_file = GameLogger.get_log_file()
        logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    # Display welcome banner
    print("=" * 60)
    print("JUNGLE GAME".center(60))
    print("A Strategic Board Game".center(60))
    print("=" * 60)
    print()

    # Initialize game controller
    controller = initialize_game(args)
    if controller is None:
        logger.error("Failed to initialize game controller")
        return 1

    # Set player names if provided
    if args.player1 or args.player2:
        # Only set names for new games, not loaded/replayed games
        if not args.load and not args.replay:
            from controller.name_manager import NameManager
            player1_name = args.player1 if args.player1 else NameManager.generate_random_name()
            player2_name = args.player2 if args.player2 else NameManager.generate_random_name()
            
            logger.info(f"Setting player names: {player1_name} vs {player2_name}")
            
            # Create new game with specified names
            from model.game import Game
            controller.game = Game(player1_name, player2_name)

    try:
        # Run the game loop
        logger.info("Starting game loop")
        controller.run_game_loop()
        logger.info("Game loop ended normally")
        return 0

    except KeyboardInterrupt:
        logger.info("Game interrupted by user (KeyboardInterrupt)")
        print("\n\nGame interrupted by user.")
        return 0

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        logger.info("Application shutting down")
        print("\nThank you for playing Jungle Game!")
        
        # Clean up old log files (keep last 7 days)
        if args.log_file:
            deleted = GameLogger.cleanup_old_logs(keep_days=7)
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} old log file(s)")


if __name__ == "__main__":
    sys.exit(main())
