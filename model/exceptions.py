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
