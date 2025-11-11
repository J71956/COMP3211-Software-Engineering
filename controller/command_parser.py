"""
CommandParser for Jungle Game.
Handles parsing and validation of user input commands.
"""

import re
from typing import Tuple
from model.position import Position
from model.exceptions import InvalidPositionException, InvalidInputException


class CommandParser:
    """
    Parses and validates user input commands.

    Handles move command parsing with position validation,
    command format validation, and input sanitization.
    """

    # Board dimensions
    BOARD_ROWS = 9
    BOARD_COLS = 7

    # Regular expressions for parsing
    MOVE_PATTERN = re.compile(
        r'^\s*(?:move\s+)?'  # Optional "move" prefix
        r'(?:from\s+)?'  # Optional "from" keyword
        r'([a-gA-G])?([0-8])'  # From position: column (letter) and row (number)
        r'\s*(?:to\s+)?'  # Optional "to" keyword
        r'([a-gA-G])?([0-8])'  # To position: column (letter) and row (number)
        r'\s*$',
        re.IGNORECASE
    )

    # Alternative pattern for numeric-only positions (row,col)
    NUMERIC_PATTERN = re.compile(
        r'^\s*(?:move\s+)?'
        r'(?:from\s+)?'
        r'\(?([0-8])\s*,?\s*([0-6])\)?'  # From position: (row,col) or row,col or row col
        r'\s*(?:to\s+)?'
        r'\(?([0-8])\s*,?\s*([0-6])\)?'  # To position: (row,col) or row,col or row col
        r'\s*$',
        re.IGNORECASE
    )

    @staticmethod
    def parse_move_command(input_str: str) -> Tuple[Position, Position]:
        """
        Parse a move command string into from and to positions.

        Supports multiple input formats:
        - "a0 b1" or "A0 B1" (chess-like notation)
        - "0,0 1,0" or "(0,0) (1,0)" (coordinate notation)
        - "move from a0 to b1" (verbose format)
        - "from 0,0 to 1,0" (verbose coordinate format)

        Args:
            input_str: The command string to parse

        Returns:
            A tuple of (from_position, to_position)

        Raises:
            InvalidInputException: If the command format is invalid
            InvalidPositionException: If positions are out of bounds
        """
        if not input_str or not input_str.strip():
            raise InvalidInputException(
                "Command cannot be empty. "
                "Use format like 'a0 b1' or '0,0 1,0' or type 'help' for more info."
            )

        # Sanitize input
        sanitized = CommandParser._sanitize_input(input_str)

        # Try chess-like notation first (e.g., "a0 b1")
        match = CommandParser.MOVE_PATTERN.match(sanitized)
        if match:
            from_col_letter, from_row_str, to_col_letter, to_row_str = match.groups()

            # If column letters are missing, try numeric pattern
            if from_col_letter is None or to_col_letter is None:
                return CommandParser._parse_numeric_format(sanitized)

            try:
                from_pos = CommandParser._parse_chess_position(from_col_letter, from_row_str)
                to_pos = CommandParser._parse_chess_position(to_col_letter, to_row_str)
                return (from_pos, to_pos)
            except InvalidPositionException:
                raise
            except (ValueError, Exception) as e:
                raise InvalidInputException(
                    f"Invalid position in command: {e}. "
                    f"Use format like 'a0 b1' (columns a-g, rows 0-8)"
                ) from e

        # Try numeric format (e.g., "0,0 1,0")
        return CommandParser._parse_numeric_format(sanitized)

    @staticmethod
    def _parse_numeric_format(input_str: str) -> Tuple[Position, Position]:
        """
        Parse numeric format commands like "0,0 1,0" or "(0,0) (1,0)".

        Args:
            input_str: The sanitized command string

        Returns:
            A tuple of (from_position, to_position)

        Raises:
            InvalidInputException: If the format is invalid
            InvalidPositionException: If positions are out of bounds
        """
        match = CommandParser.NUMERIC_PATTERN.match(input_str)
        if not match:
            raise InvalidInputException(
                "Invalid command format. "
                "Use formats like 'a0 b1', '0,0 1,0', or 'move from a0 to b1'. "
                "Type 'help' for more examples."
            )

        from_row_str, from_col_str, to_row_str, to_col_str = match.groups()

        try:
            from_row = int(from_row_str)
            from_col = int(from_col_str)
            to_row = int(to_row_str)
            to_col = int(to_col_str)

            from_pos = CommandParser.parse_position(from_row, from_col)
            to_pos = CommandParser.parse_position(to_row, to_col)

            return (from_pos, to_pos)
        except InvalidPositionException:
            raise
        except (ValueError, Exception) as e:
            raise InvalidInputException(
                f"Invalid position in command: {e}. "
                f"Rows must be 0-8, columns must be 0-6."
            ) from e

    @staticmethod
    def _parse_chess_position(col_letter: str, row_str: str) -> Position:
        """
        Parse a chess-like position (e.g., "a0", "B3").

        Args:
            col_letter: Column letter (a-g or A-G)
            row_str: Row number as string (0-8)

        Returns:
            A Position object

        Raises:
            InvalidInputException: If the position format is invalid
            InvalidPositionException: If the position is out of bounds
        """
        try:
            col = ord(col_letter.lower()) - ord('a')
            row = int(row_str)
            return CommandParser.parse_position(row, col)
        except (ValueError, AttributeError) as e:
            raise InvalidInputException(
                f"Invalid position format: {col_letter}{row_str}. "
                f"Use column letters a-g and row numbers 0-8."
            ) from e

    @staticmethod
    def parse_position(row: int, col: int) -> Position:
        """
        Create and validate a Position object.

        Args:
            row: Row index (0-8)
            col: Column index (0-6)

        Returns:
            A validated Position object

        Raises:
            InvalidPositionException: If the position is out of bounds
        """
        if not CommandParser.is_valid_position(row, col):
            raise InvalidPositionException(
                f"Position ({row},{col}) is out of bounds. "
                f"Valid range: rows 0-{CommandParser.BOARD_ROWS-1}, "
                f"cols 0-{CommandParser.BOARD_COLS-1}"
            )

        return Position(row, col)

    @staticmethod
    def is_valid_position(row: int, col: int) -> bool:
        """
        Check if a position is within board bounds.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is valid, False otherwise
        """
        return (0 <= row < CommandParser.BOARD_ROWS and
                0 <= col < CommandParser.BOARD_COLS)

    @staticmethod
    def validate_command_format(command: str) -> bool:
        """
        Validate if a command string has a valid format.

        Args:
            command: The command string to validate

        Returns:
            True if the format is valid, False otherwise
        """
        if not command or not command.strip():
            return False

        sanitized = CommandParser._sanitize_input(command)

        # Check if it matches either pattern
        return (CommandParser.MOVE_PATTERN.match(sanitized) is not None or
                CommandParser.NUMERIC_PATTERN.match(sanitized) is not None)

    @staticmethod
    def _sanitize_input(input_str: str) -> str:
        """
        Sanitize and normalize user input.

        Removes extra whitespace, normalizes case for keywords,
        and cleans up the input string.

        Args:
            input_str: The raw input string

        Returns:
            Sanitized input string
        """
        # Strip leading/trailing whitespace
        sanitized = input_str.strip()

        # Normalize multiple spaces to single space
        sanitized = re.sub(r'\s+', ' ', sanitized)

        return sanitized

    @staticmethod
    def format_position(position: Position) -> str:
        """
        Format a Position object as a human-readable string.

        Args:
            position: The position to format

        Returns:
            Formatted string like "a0" or "(0,0)"
        """
        col_letter = chr(ord('a') + position.col)
        return f"{col_letter}{position.row}"
