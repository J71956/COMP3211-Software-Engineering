"""
Exception classes for Jungle Game.
Defines the exception hierarchy for game-related errors.
"""


class JungleGameException(Exception):
    """Base exception for all game-related errors."""
    pass


class InvalidMoveException(JungleGameException):
    """Raised when a move violates game rules."""
    pass


class InvalidPositionException(JungleGameException):
    """Raised when position is outside board bounds."""
    pass


class GameOverException(JungleGameException):
    """Raised when attempting to play after game ends."""
    pass


class FileOperationException(JungleGameException):
    """Raised when file save/load operations fail."""
    pass


class InvalidInputException(JungleGameException):
    """Raised when user input is invalid or malformed."""
    pass


class PieceNotFoundException(JungleGameException):
    """Raised when no piece is found at the specified position."""
    pass


class WrongPlayerException(JungleGameException):
    """Raised when a player tries to move opponent's piece."""
    pass


class InvalidCaptureException(JungleGameException):
    """Raised when a capture attempt violates game rules."""
    pass


class ValidationException(JungleGameException):
    """Raised when data validation fails."""
    pass
