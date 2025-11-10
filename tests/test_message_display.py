"""
Unit tests for MessageDisplay class.
Tests message formatting and display functionality.
"""

import unittest
from view.message_display import MessageDisplay


class TestMessageDisplay(unittest.TestCase):
    """Test cases for MessageDisplay class."""

    def setUp(self):
        """Set up test fixtures."""
        self.display = MessageDisplay()

    def test_initialization(self):
        """Test MessageDisplay initializes correctly."""
        self.assertIsNotNone(self.display)

    def test_show_error(self):
        """Test error message formatting."""
        result = self.display.show_error("Something went wrong")

        self.assertIn("ERROR:", result)
        self.assertIn("Something went wrong", result)
        self.assertTrue(result.startswith("ERROR:"))

    def test_show_info(self):
        """Test info message formatting."""
        result = self.display.show_info("Game saved successfully")

        self.assertIn("INFO:", result)
        self.assertIn("Game saved successfully", result)
        self.assertTrue(result.startswith("INFO:"))

    def test_show_warning(self):
        """Test warning message formatting."""
        result = self.display.show_warning("This action cannot be undone")

        self.assertIn("WARNING:", result)
        self.assertIn("This action cannot be undone", result)
        self.assertTrue(result.startswith("WARNING:"))

    def test_show_success(self):
        """Test success message formatting."""
        result = self.display.show_success("Move completed")

        self.assertIn("✓", result)
        self.assertIn("Move completed", result)
        self.assertTrue(result.startswith("✓"))

    def test_show_failure(self):
        """Test failure message formatting."""
        result = self.display.show_failure("Move failed")

        self.assertIn("✗", result)
        self.assertIn("Move failed", result)
        self.assertTrue(result.startswith("✗"))

    def test_prompt_for_input(self):
        """Test input prompt formatting."""
        result = self.display.prompt_for_input("Enter your move")

        self.assertIn("Enter your move", result)
        self.assertTrue(result.endswith(": "))

    def test_confirm_action(self):
        """Test confirmation prompt formatting."""
        result = self.display.confirm_action("quit the game")

        self.assertIn("Are you sure", result)
        self.assertIn("quit the game", result)
        self.assertIn("yes/no", result)
        self.assertTrue(result.endswith(": "))

    def test_show_validation_error(self):
        """Test validation error message formatting."""
        result = self.display.show_validation_error("position", "out of bounds")

        self.assertIn("ERROR:", result)
        self.assertIn("Invalid position", result)
        self.assertIn("out of bounds", result)

    def test_show_file_error(self):
        """Test file error message formatting."""
        result = self.display.show_file_error("game.jungle", "save", "permission denied")

        self.assertIn("ERROR:", result)
        self.assertIn("Failed to save", result)
        self.assertIn("game.jungle", result)
        self.assertIn("permission denied", result)

    def test_show_file_success(self):
        """Test file success message formatting."""
        result = self.display.show_file_success("game.jungle", "saved")

        self.assertIn("✓", result)
        self.assertIn("game.jungle", result)
        self.assertIn("saved successfully", result)

    def test_show_game_action_with_details(self):
        """Test game action message with details."""
        result = self.display.show_game_action("Move made", "Rat from (8,0) to (7,0)")

        self.assertIn("INFO:", result)
        self.assertIn("Move made", result)
        self.assertIn("Rat from (8,0) to (7,0)", result)

    def test_show_game_action_without_details(self):
        """Test game action message without details."""
        result = self.display.show_game_action("Game started")

        self.assertIn("INFO:", result)
        self.assertIn("Game started", result)
        self.assertNotIn(" - ", result)

    def test_show_invalid_command_with_reason(self):
        """Test invalid command message with reason."""
        result = self.display.show_invalid_command("mov", "unknown command")

        self.assertIn("ERROR:", result)
        self.assertIn("Invalid command", result)
        self.assertIn("mov", result)
        self.assertIn("unknown command", result)

    def test_show_invalid_command_without_reason(self):
        """Test invalid command message without reason."""
        result = self.display.show_invalid_command("xyz")

        self.assertIn("ERROR:", result)
        self.assertIn("Invalid command", result)
        self.assertIn("xyz", result)

    def test_show_help_message(self):
        """Test help message formatting."""
        result = self.display.show_help_message()

        self.assertIn("Available Commands", result)
        self.assertIn("move", result)
        self.assertIn("undo", result)
        self.assertIn("save", result)
        self.assertIn("load", result)
        self.assertIn("quit", result)
        self.assertIn("help", result)

    def test_format_list_with_title(self):
        """Test list formatting with title."""
        items = ["Item 1", "Item 2", "Item 3"]
        result = self.display.format_list(items, "My List")

        self.assertIn("My List:", result)
        self.assertIn("1. Item 1", result)
        self.assertIn("2. Item 2", result)
        self.assertIn("3. Item 3", result)

    def test_format_list_without_title(self):
        """Test list formatting without title."""
        items = ["Item A", "Item B"]
        result = self.display.format_list(items)

        self.assertIn("1. Item A", result)
        self.assertIn("2. Item B", result)
        self.assertNotIn(":", result.split("\n")[0])

    def test_format_empty_list(self):
        """Test formatting empty list."""
        result = self.display.format_list([])

        self.assertEqual(result, "")

    def test_format_key_value_pairs_with_title(self):
        """Test key-value pairs formatting with title."""
        pairs = {"Player 1": "Alice", "Player 2": "Bob"}
        result = self.display.format_key_value_pairs(pairs, "Players")

        self.assertIn("Players:", result)
        self.assertIn("Player 1: Alice", result)
        self.assertIn("Player 2: Bob", result)

    def test_format_key_value_pairs_without_title(self):
        """Test key-value pairs formatting without title."""
        pairs = {"Score": "100", "Level": "5"}
        result = self.display.format_key_value_pairs(pairs)

        self.assertIn("Score: 100", result)
        self.assertIn("Level: 5", result)

    def test_format_empty_key_value_pairs(self):
        """Test formatting empty key-value pairs."""
        result = self.display.format_key_value_pairs({})

        self.assertEqual(result, "")

    def test_show_separator_default(self):
        """Test separator with default parameters."""
        result = self.display.show_separator()

        self.assertEqual(result, "-" * 50)
        self.assertEqual(len(result), 50)

    def test_show_separator_custom(self):
        """Test separator with custom parameters."""
        result = self.display.show_separator("=", 30)

        self.assertEqual(result, "=" * 30)
        self.assertEqual(len(result), 30)

    def test_show_header_default(self):
        """Test header with default parameters."""
        result = self.display.show_header("GAME TITLE")

        self.assertIn("GAME TITLE", result)
        self.assertIn("=" * 50, result)
        lines = result.split("\n")
        self.assertEqual(len(lines), 3)

    def test_show_header_custom(self):
        """Test header with custom parameters."""
        result = self.display.show_header("TEST", "-", 20)

        self.assertIn("TEST", result)
        self.assertIn("-" * 20, result)
        lines = result.split("\n")
        self.assertEqual(len(lines), 3)

    def test_all_methods_return_strings(self):
        """Test that all display methods return strings."""
        self.assertIsInstance(self.display.show_error("test"), str)
        self.assertIsInstance(self.display.show_info("test"), str)
        self.assertIsInstance(self.display.show_warning("test"), str)
        self.assertIsInstance(self.display.show_success("test"), str)
        self.assertIsInstance(self.display.show_failure("test"), str)
        self.assertIsInstance(self.display.prompt_for_input("test"), str)
        self.assertIsInstance(self.display.confirm_action("test"), str)
        self.assertIsInstance(self.display.show_validation_error("field", "reason"), str)
        self.assertIsInstance(self.display.show_file_error("file", "op", "reason"), str)
        self.assertIsInstance(self.display.show_file_success("file", "op"), str)
        self.assertIsInstance(self.display.show_game_action("action"), str)
        self.assertIsInstance(self.display.show_invalid_command("cmd"), str)
        self.assertIsInstance(self.display.show_help_message(), str)
        self.assertIsInstance(self.display.format_list([]), str)
        self.assertIsInstance(self.display.format_key_value_pairs({}), str)
        self.assertIsInstance(self.display.show_separator(), str)
        self.assertIsInstance(self.display.show_header("test"), str)

    def test_message_consistency(self):
        """Test that message formatting is consistent."""
        error1 = self.display.show_error("Error 1")
        error2 = self.display.show_error("Error 2")

        self.assertTrue(error1.startswith("ERROR:"))
        self.assertTrue(error2.startswith("ERROR:"))

        info1 = self.display.show_info("Info 1")
        info2 = self.display.show_info("Info 2")

        self.assertTrue(info1.startswith("INFO:"))
        self.assertTrue(info2.startswith("INFO:"))


if __name__ == '__main__':
    unittest.main()
