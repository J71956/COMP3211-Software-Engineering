"""
Unit tests for CommandParser class.
"""

import unittest
from controller.command_parser import CommandParser
from model.position import Position
from model.exceptions import InvalidPositionException


class TestCommandParser(unittest.TestCase):
    """Test cases for CommandParser class."""

    def test_parse_chess_notation_lowercase(self):
        """Test parsing chess-like notation with lowercase letters."""
        from_pos, to_pos = CommandParser.parse_move_command("a0 b1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_chess_notation_uppercase(self):
        """Test parsing chess-like notation with uppercase letters."""
        from_pos, to_pos = CommandParser.parse_move_command("A0 B1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_chess_notation_mixed_case(self):
        """Test parsing chess-like notation with mixed case."""
        from_pos, to_pos = CommandParser.parse_move_command("a0 B1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_numeric_notation_comma(self):
        """Test parsing numeric notation with commas."""
        from_pos, to_pos = CommandParser.parse_move_command("0,0 1,1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_numeric_notation_parentheses(self):
        """Test parsing numeric notation with parentheses."""
        from_pos, to_pos = CommandParser.parse_move_command("(0,0) (1,1)")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_numeric_notation_space_separated(self):
        """Test parsing numeric notation with spaces instead of commas."""
        from_pos, to_pos = CommandParser.parse_move_command("0 0 1 1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_verbose_chess_notation(self):
        """Test parsing verbose format with 'move from to' keywords."""
        from_pos, to_pos = CommandParser.parse_move_command("move from a0 to b1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_verbose_numeric_notation(self):
        """Test parsing verbose numeric format."""
        from_pos, to_pos = CommandParser.parse_move_command("move from 0,0 to 1,1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_with_extra_whitespace(self):
        """Test parsing with extra whitespace."""
        from_pos, to_pos = CommandParser.parse_move_command("  a0   b1  ")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_parse_edge_positions(self):
        """Test parsing positions at board edges."""
        from_pos, to_pos = CommandParser.parse_move_command("g8 a0")
        self.assertEqual(from_pos, Position(8, 6))
        self.assertEqual(to_pos, Position(0, 0))

    def test_parse_invalid_empty_command(self):
        """Test that empty command raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException) as context:
            CommandParser.parse_move_command("")
        self.assertIn("empty", str(context.exception).lower())

    def test_parse_invalid_whitespace_only(self):
        """Test that whitespace-only command raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException) as context:
            CommandParser.parse_move_command("   ")
        self.assertIn("empty", str(context.exception).lower())

    def test_parse_invalid_format(self):
        """Test that invalid format raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException) as context:
            CommandParser.parse_move_command("invalid command")
        self.assertIn("Invalid command format", str(context.exception))

    def test_parse_invalid_column_letter(self):
        """Test that invalid column letter raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException):
            CommandParser.parse_move_command("h0 a1")  # h is out of range (only a-g)

    def test_parse_invalid_row_number_too_high(self):
        """Test that row number too high raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException):
            CommandParser.parse_move_command("a9 b0")  # row 9 is out of range (only 0-8)

    def test_parse_invalid_numeric_column_too_high(self):
        """Test that numeric column too high raises InvalidInputException."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException):
            CommandParser.parse_move_command("0,7 1,0")  # col 7 is out of range (only 0-6)

    def test_parse_invalid_negative_position(self):
        """Test that negative positions are rejected."""
        from model.exceptions import InvalidInputException
        with self.assertRaises(InvalidInputException):
            CommandParser.parse_move_command("0,-1 1,0")

    def test_parse_position_valid(self):
        """Test creating a valid position."""
        pos = CommandParser.parse_position(3, 4)
        self.assertEqual(pos.row, 3)
        self.assertEqual(pos.col, 4)

    def test_parse_position_invalid_row_negative(self):
        """Test that negative row raises InvalidPositionException."""
        with self.assertRaises(InvalidPositionException):
            CommandParser.parse_position(-1, 0)

    def test_parse_position_invalid_row_too_high(self):
        """Test that row too high raises InvalidPositionException."""
        with self.assertRaises(InvalidPositionException):
            CommandParser.parse_position(9, 0)

    def test_parse_position_invalid_col_negative(self):
        """Test that negative column raises InvalidPositionException."""
        with self.assertRaises(InvalidPositionException):
            CommandParser.parse_position(0, -1)

    def test_parse_position_invalid_col_too_high(self):
        """Test that column too high raises InvalidPositionException."""
        with self.assertRaises(InvalidPositionException):
            CommandParser.parse_position(0, 7)

    def test_is_valid_position_valid(self):
        """Test valid position check."""
        self.assertTrue(CommandParser.is_valid_position(0, 0))
        self.assertTrue(CommandParser.is_valid_position(8, 6))
        self.assertTrue(CommandParser.is_valid_position(4, 3))

    def test_is_valid_position_invalid(self):
        """Test invalid position check."""
        self.assertFalse(CommandParser.is_valid_position(-1, 0))
        self.assertFalse(CommandParser.is_valid_position(0, -1))
        self.assertFalse(CommandParser.is_valid_position(9, 0))
        self.assertFalse(CommandParser.is_valid_position(0, 7))
        self.assertFalse(CommandParser.is_valid_position(10, 10))

    def test_validate_command_format_valid_chess(self):
        """Test command format validation for chess notation."""
        self.assertTrue(CommandParser.validate_command_format("a0 b1"))
        self.assertTrue(CommandParser.validate_command_format("A0 B1"))
        self.assertTrue(CommandParser.validate_command_format("move from a0 to b1"))

    def test_validate_command_format_valid_numeric(self):
        """Test command format validation for numeric notation."""
        self.assertTrue(CommandParser.validate_command_format("0,0 1,1"))
        self.assertTrue(CommandParser.validate_command_format("(0,0) (1,1)"))
        self.assertTrue(CommandParser.validate_command_format("move from 0,0 to 1,1"))

    def test_validate_command_format_invalid(self):
        """Test command format validation for invalid formats."""
        self.assertFalse(CommandParser.validate_command_format(""))
        self.assertFalse(CommandParser.validate_command_format("   "))
        self.assertFalse(CommandParser.validate_command_format("invalid"))
        self.assertFalse(CommandParser.validate_command_format("a0"))  # Missing destination

    def test_sanitize_input_strips_whitespace(self):
        """Test that sanitization removes leading/trailing whitespace."""
        # Test via parse_move_command which uses _sanitize_input internally
        from_pos, to_pos = CommandParser.parse_move_command("  a0   b1  ")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_sanitize_input_normalizes_spaces(self):
        """Test that sanitization normalizes multiple spaces."""
        # Test via parse_move_command which uses _sanitize_input internally
        from_pos, to_pos = CommandParser.parse_move_command("a0    b1")
        self.assertEqual(from_pos, Position(0, 0))
        self.assertEqual(to_pos, Position(1, 1))

    def test_format_position(self):
        """Test formatting a position as chess notation."""
        pos = Position(0, 0)
        self.assertEqual(CommandParser.format_position(pos), "a0")

        pos = Position(8, 6)
        self.assertEqual(CommandParser.format_position(pos), "g8")

        pos = Position(3, 2)
        self.assertEqual(CommandParser.format_position(pos), "c3")

    def test_parse_all_valid_columns(self):
        """Test parsing all valid column letters."""
        for col_idx, col_letter in enumerate('abcdefg'):
            from_pos, _ = CommandParser.parse_move_command(f"{col_letter}0 a1")
            self.assertEqual(from_pos.col, col_idx)

    def test_parse_all_valid_rows(self):
        """Test parsing all valid row numbers."""
        for row in range(9):
            from_pos, _ = CommandParser.parse_move_command(f"a{row} b0")
            self.assertEqual(from_pos.row, row)

    def test_parse_case_insensitive_keywords(self):
        """Test that keywords are case insensitive."""
        from_pos1, to_pos1 = CommandParser.parse_move_command("MOVE FROM a0 TO b1")
        from_pos2, to_pos2 = CommandParser.parse_move_command("move from a0 to b1")
        from_pos3, to_pos3 = CommandParser.parse_move_command("MoVe FrOm a0 To b1")

        self.assertEqual(from_pos1, from_pos2)
        self.assertEqual(from_pos1, from_pos3)
        self.assertEqual(to_pos1, to_pos2)
        self.assertEqual(to_pos1, to_pos3)


if __name__ == '__main__':
    unittest.main()
