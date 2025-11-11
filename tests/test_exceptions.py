"""
Unit tests for exception classes.
"""

import unittest
from model.exceptions import (
    JungleGameException,
    InvalidMoveException,
    InvalidPositionException,
    GameOverException,
    FileOperationException,
    InvalidInputException,
    PieceNotFoundException,
    WrongPlayerException,
    InvalidCaptureException,
    ValidationException
)


class TestExceptions(unittest.TestCase):
    """Test cases for exception hierarchy."""
    
    def test_jungle_game_exception_is_base(self):
        """Test that JungleGameException is the base exception."""
        exc = JungleGameException("Test error")
        self.assertIsInstance(exc, Exception)
        self.assertEqual(str(exc), "Test error")
    
    def test_invalid_move_exception_inheritance(self):
        """Test InvalidMoveException inherits from JungleGameException."""
        exc = InvalidMoveException("Invalid move")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_invalid_position_exception_inheritance(self):
        """Test InvalidPositionException inherits from JungleGameException."""
        exc = InvalidPositionException("Invalid position")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_game_over_exception_inheritance(self):
        """Test GameOverException inherits from JungleGameException."""
        exc = GameOverException("Game is over")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_file_operation_exception_inheritance(self):
        """Test FileOperationException inherits from JungleGameException."""
        exc = FileOperationException("File error")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_invalid_input_exception_inheritance(self):
        """Test InvalidInputException inherits from JungleGameException."""
        exc = InvalidInputException("Invalid input")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_piece_not_found_exception_inheritance(self):
        """Test PieceNotFoundException inherits from JungleGameException."""
        exc = PieceNotFoundException("Piece not found")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_wrong_player_exception_inheritance(self):
        """Test WrongPlayerException inherits from JungleGameException."""
        exc = WrongPlayerException("Wrong player")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_invalid_capture_exception_inheritance(self):
        """Test InvalidCaptureException inherits from JungleGameException."""
        exc = InvalidCaptureException("Invalid capture")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_validation_exception_inheritance(self):
        """Test ValidationException inherits from JungleGameException."""
        exc = ValidationException("Validation failed")
        self.assertIsInstance(exc, JungleGameException)
        self.assertIsInstance(exc, Exception)
    
    def test_exception_can_be_raised_and_caught(self):
        """Test that exceptions can be raised and caught."""
        with self.assertRaises(InvalidMoveException):
            raise InvalidMoveException("Test move error")
        
        with self.assertRaises(JungleGameException):
            raise InvalidPositionException("Test position error")
    
    def test_all_exceptions_can_be_caught_as_base(self):
        """Test that all custom exceptions can be caught as JungleGameException."""
        exceptions = [
            InvalidMoveException("test"),
            InvalidPositionException("test"),
            GameOverException("test"),
            FileOperationException("test"),
            InvalidInputException("test"),
            PieceNotFoundException("test"),
            WrongPlayerException("test"),
            InvalidCaptureException("test"),
            ValidationException("test")
        ]
        
        for exc in exceptions:
            with self.assertRaises(JungleGameException):
                raise exc


if __name__ == '__main__':
    unittest.main()
