"""
MessageDisplay class for Jungle Game.
Handles error message formatting, informational messages, and user prompts.
"""

from typing import Optional


class MessageDisplay:
    """
    Handles user communication through formatted messages.

    Provides methods for:
    - Error message formatting and display
    - Informational message handling
    - User feedback and confirmation displays
    - Input prompts with validation

    All methods return formatted strings for display.
    """

    # Message formatting constants
    ERROR_PREFIX = "ERROR: "
    INFO_PREFIX = "INFO: "
    WARNING_PREFIX = "WARNING: "
    SUCCESS_PREFIX = "✓ "
    FAILURE_PREFIX = "✗ "
    PROMPT_SUFFIX = ": "

    def __init__(self):
        """Initialize the MessageDisplay."""

    def show_error(self, message: str) -> str:
        """
        Format and return an error message.

        Args:
            message: The error message to display

        Returns:
            Formatted error message string
        """
        return f"{self.ERROR_PREFIX}{message}"

    def show_info(self, message: str) -> str:
        """
        Format and return an informational message.

        Args:
            message: The informational message to display

        Returns:
            Formatted info message string
        """
        return f"{self.INFO_PREFIX}{message}"

    def show_warning(self, message: str) -> str:
        """
        Format and return a warning message.

        Args:
            message: The warning message to display

        Returns:
            Formatted warning message string
        """
        return f"{self.WARNING_PREFIX}{message}"

    def show_success(self, message: str) -> str:
        """
        Format and return a success message.

        Args:
            message: The success message to display

        Returns:
            Formatted success message string with checkmark
        """
        return f"{self.SUCCESS_PREFIX}{message}"

    def show_failure(self, message: str) -> str:
        """
        Format and return a failure message.

        Args:
            message: The failure message to display

        Returns:
            Formatted failure message string with X mark
        """
        return f"{self.FAILURE_PREFIX}{message}"

    def prompt_for_input(self, prompt: str) -> str:
        """
        Format a prompt for user input.

        Args:
            prompt: The prompt message to display

        Returns:
            Formatted prompt string
        """
        return f"{prompt}{self.PROMPT_SUFFIX}"

    def confirm_action(self, action: str) -> str:
        """
        Format a confirmation prompt for an action.

        Args:
            action: The action to confirm

        Returns:
            Formatted confirmation prompt
        """
        return f"Are you sure you want to {action}? (yes/no){self.PROMPT_SUFFIX}"

    def show_validation_error(self, field: str, reason: str) -> str:
        """
        Format a validation error message.

        Args:
            field: The field that failed validation
            reason: The reason for validation failure

        Returns:
            Formatted validation error message
        """
        return f"{self.ERROR_PREFIX}Invalid {field}: {reason}"

    def show_file_error(self, filename: str, operation: str, reason: str) -> str:
        """
        Format a file operation error message.

        Args:
            filename: The file that caused the error
            operation: The operation that failed (e.g., "save", "load")
            reason: The reason for the failure

        Returns:
            Formatted file error message
        """
        return f"{self.ERROR_PREFIX}Failed to {operation} file '{filename}': {reason}"

    def show_file_success(self, filename: str, operation: str) -> str:
        """
        Format a file operation success message.

        Args:
            filename: The file that was operated on
            operation: The operation that succeeded (e.g., "saved", "loaded")

        Returns:
            Formatted file success message
        """
        return f"{self.SUCCESS_PREFIX}File '{filename}' {operation} successfully"

    def show_game_action(self, action: str, details: Optional[str] = None) -> str:
        """
        Format a game action message.

        Args:
            action: The action that occurred
            details: Optional additional details about the action

        Returns:
            Formatted game action message
        """
        if details:
            return f"{self.INFO_PREFIX}{action} - {details}"
        return f"{self.INFO_PREFIX}{action}"

    def show_invalid_command(self, command: str, reason: Optional[str] = None) -> str:
        """
        Format an invalid command error message.

        Args:
            command: The invalid command
            reason: Optional reason why the command is invalid

        Returns:
            Formatted invalid command error message
        """
        if reason:
            return f"{self.ERROR_PREFIX}Invalid command '{command}': {reason}"
        return f"{self.ERROR_PREFIX}Invalid command '{command}'"

    def show_help_message(self) -> str:
        """
        Format and return a help message with available commands.

        Returns:
            Formatted help message
        """
        lines = [
            "Available Commands:",
            "  move <from_row> <from_col> <to_row> <to_col> - Make a move",
            "  undo - Undo the last move (up to 3 moves)",
            "  save <filename> - Save the current game",
            "  load <filename> - Load a saved game",
            "  record <filename> - Save game record",
            "  replay <filename> - Replay a game from record",
            "  help - Show this help message",
            "  quit - Exit the game"
        ]
        return "\n".join(lines)

    def format_list(self, items: list, title: Optional[str] = None) -> str:
        """
        Format a list of items for display.

        Args:
            items: List of items to display
            title: Optional title for the list

        Returns:
            Formatted list string
        """
        lines = []
        if title:
            lines.append(f"{title}:")
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item}")
        return "\n".join(lines)

    def format_key_value_pairs(self, pairs: dict, title: Optional[str] = None) -> str:
        """
        Format key-value pairs for display.

        Args:
            pairs: Dictionary of key-value pairs
            title: Optional title for the pairs

        Returns:
            Formatted key-value string
        """
        lines = []
        if title:
            lines.append(f"{title}:")
        for key, value in pairs.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def show_separator(self, char: str = "-", length: int = 50) -> str:
        """
        Create a separator line.

        Args:
            char: Character to use for the separator
            length: Length of the separator line

        Returns:
            Separator string
        """
        return char * length

    def show_header(self, text: str, char: str = "=", length: int = 50) -> str:
        """
        Create a header with text centered between separator lines.

        Args:
            text: Header text
            char: Character to use for the separator
            length: Length of the separator lines

        Returns:
            Formatted header string
        """
        separator = char * length
        return f"{separator}\n{text.center(length)}\n{separator}"
