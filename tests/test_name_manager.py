"""
Unit tests for NameManager class.
"""

import unittest
from unittest.mock import patch
from controller.name_manager import NameManager


class TestNameManager(unittest.TestCase):
    """Test cases for NameManager class."""

    def test_validate_name_valid_simple(self):
        """Test validation of simple valid names."""
        self.assertTrue(NameManager.validate_name("Alice"))
        self.assertTrue(NameManager.validate_name("Bob"))
        self.assertTrue(NameManager.validate_name("Player1"))

    def test_validate_name_valid_with_spaces(self):
        """Test validation of names with spaces."""
        self.assertTrue(NameManager.validate_name("Alice Smith"))
        self.assertTrue(NameManager.validate_name("The Great Player"))

    def test_validate_name_valid_with_hyphens(self):
        """Test validation of names with hyphens."""
        self.assertTrue(NameManager.validate_name("Jean-Luc"))
        self.assertTrue(NameManager.validate_name("Player-One"))

    def test_validate_name_valid_with_underscores(self):
        """Test validation of names with underscores."""
        self.assertTrue(NameManager.validate_name("Player_1"))
        self.assertTrue(NameManager.validate_name("Cool_Name"))

    def test_validate_name_valid_mixed(self):
        """Test validation of names with mixed valid characters."""
        self.assertTrue(NameManager.validate_name("Player-1_A"))
        self.assertTrue(NameManager.validate_name("The_Best-Player 123"))

    def test_validate_name_empty_string(self):
        """Test validation rejects empty string."""
        self.assertFalse(NameManager.validate_name(""))

    def test_validate_name_whitespace_only(self):
        """Test validation rejects whitespace-only strings."""
        self.assertFalse(NameManager.validate_name("   "))
        self.assertFalse(NameManager.validate_name("\t"))
        self.assertFalse(NameManager.validate_name("\n"))

    def test_validate_name_too_long(self):
        """Test validation rejects names longer than 30 characters."""
        long_name = "A" * 31
        self.assertFalse(NameManager.validate_name(long_name))

    def test_validate_name_max_length(self):
        """Test validation accepts names exactly 30 characters."""
        max_name = "A" * 30
        self.assertTrue(NameManager.validate_name(max_name))

    def test_validate_name_invalid_characters(self):
        """Test validation rejects names with invalid characters."""
        self.assertFalse(NameManager.validate_name("Player@123"))
        self.assertFalse(NameManager.validate_name("Name!"))
        self.assertFalse(NameManager.validate_name("Test#Name"))
        self.assertFalse(NameManager.validate_name("Player$"))

    def test_validate_name_with_special_chars(self):
        """Test validation rejects various special characters."""
        invalid_names = [
            "Player*", "Name&", "Test%", "User^",
            "Name()", "Test[]", "User{}", "Name<>",
            "Test/", "User\\", "Name|", "Test+"
        ]
        for name in invalid_names:
            self.assertFalse(NameManager.validate_name(name))

    def test_validate_name_strips_whitespace(self):
        """Test validation handles leading/trailing whitespace."""
        self.assertTrue(NameManager.validate_name("  Alice  "))
        self.assertTrue(NameManager.validate_name("\tBob\t"))

    def test_generate_random_name_format(self):
        """Test that generated names follow the expected format."""
        name = NameManager.generate_random_name()

        # Should be a string
        self.assertIsInstance(name, str)

        # Should contain a space (adjective + animal)
        self.assertIn(" ", name)

        # Should have two parts
        parts = name.split()
        self.assertEqual(len(parts), 2)

    def test_generate_random_name_uses_valid_words(self):
        """Test that generated names use words from the predefined lists."""
        name = NameManager.generate_random_name()
        adjective, animal = name.split()

        self.assertIn(adjective, NameManager.ADJECTIVES)
        self.assertIn(animal, NameManager.ANIMALS)

    def test_generate_random_name_multiple_calls(self):
        """Test generating multiple random names."""
        names = [NameManager.generate_random_name() for _ in range(10)]

        # All should be valid
        for name in names:
            self.assertTrue(NameManager.validate_name(name))

        # Should have at least some variety (not all the same)
        unique_names = set(names)
        self.assertGreater(len(unique_names), 1)

    @patch('builtins.input', return_value='Alice')
    def test_get_player_name_with_valid_input(self, mock_input):
        """Test getting player name with valid user input."""
        name = NameManager.get_player_name("Enter name: ")

        self.assertEqual(name, "Alice")
        mock_input.assert_called_once()

    @patch('builtins.input', return_value='')
    @patch('controller.name_manager.NameManager.generate_random_name',
           return_value='Brave Tiger')
    def test_get_player_name_empty_input_generates_random(
            self, mock_generate, mock_input):
        """Test that empty input generates a random name."""
        with patch('builtins.print'):
            name = NameManager.get_player_name("Enter name: ")

        self.assertEqual(name, 'Brave Tiger')
        mock_generate.assert_called_once()

    @patch('builtins.input', return_value='')
    def test_get_player_name_empty_input_uses_default(self, mock_input):
        """Test that empty input uses default name if provided."""
        name = NameManager.get_player_name("Enter name: ", default_name="DefaultPlayer")

        self.assertEqual(name, "DefaultPlayer")

    @patch('builtins.input', side_effect=['Invalid@Name', 'ValidName'])
    def test_get_player_name_retries_on_invalid(self, mock_input):
        """Test that invalid names prompt for retry."""
        with patch('builtins.print'):
            name = NameManager.get_player_name("Enter name: ")

        self.assertEqual(name, "ValidName")
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['', '', ''])
    @patch('controller.name_manager.NameManager.generate_random_name',
           side_effect=['Random1', 'Random2', 'Random3'])
    def test_get_player_name_multiple_empty_inputs(
            self, mock_generate, mock_input):
        """Test multiple empty inputs generate different random names."""
        with patch('builtins.print'):
            name1 = NameManager.get_player_name("Enter name: ")
            name2 = NameManager.get_player_name("Enter name: ")
            name3 = NameManager.get_player_name("Enter name: ")

        self.assertEqual(name1, 'Random1')
        self.assertEqual(name2, 'Random2')
        self.assertEqual(name3, 'Random3')

    @patch('builtins.input', side_effect=['Alice', 'Bob'])
    def test_get_player_names_both_valid(self, mock_input):
        """Test getting both player names with valid inputs."""
        with patch('builtins.print'):
            player1, player2 = NameManager.get_player_names()

        self.assertEqual(player1, 'Alice')
        self.assertEqual(player2, 'Bob')

    @patch('builtins.input', side_effect=['Alice', 'Alice', 'Bob'])
    def test_get_player_names_rejects_duplicate(self, mock_input):
        """Test that duplicate names are rejected."""
        with patch('builtins.print'):
            player1, player2 = NameManager.get_player_names()

        self.assertEqual(player1, 'Alice')
        self.assertEqual(player2, 'Bob')
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=['', ''])
    @patch('controller.name_manager.NameManager.generate_random_name',
           side_effect=['Random1', 'Random2'])
    def test_get_player_names_both_random(self, mock_generate, mock_input):
        """Test getting both player names with random generation."""
        with patch('builtins.print'):
            player1, player2 = NameManager.get_player_names()

        self.assertEqual(player1, 'Random1')
        self.assertEqual(player2, 'Random2')

    @patch('builtins.input', side_effect=['Alice', ''])
    @patch('controller.name_manager.NameManager.generate_random_name',
           return_value='Random Player')
    def test_get_player_names_mixed_input(self, mock_generate, mock_input):
        """Test getting player names with one input and one random."""
        with patch('builtins.print'):
            player1, player2 = NameManager.get_player_names()

        self.assertEqual(player1, 'Alice')
        self.assertEqual(player2, 'Random Player')

    def test_adjectives_list_not_empty(self):
        """Test that the adjectives list is not empty."""
        self.assertGreater(len(NameManager.ADJECTIVES), 0)

    def test_animals_list_not_empty(self):
        """Test that the animals list is not empty."""
        self.assertGreater(len(NameManager.ANIMALS), 0)

    def test_adjectives_all_valid(self):
        """Test that all adjectives are valid name components."""
        for adjective in NameManager.ADJECTIVES:
            self.assertTrue(NameManager.validate_name(adjective))

    def test_animals_all_valid(self):
        """Test that all animals are valid name components."""
        for animal in NameManager.ANIMALS:
            self.assertTrue(NameManager.validate_name(animal))


if __name__ == '__main__':
    unittest.main()
