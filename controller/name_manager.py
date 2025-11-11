"""
NameManager class for Jungle Game.
Handles player name input, validation, and random name generation.
"""

import random
from typing import Optional


class NameManager:
    """
    Manages player name input, validation, and random generation.

    Provides functionality to get player names from user input or generate
    random names when no input is provided.
    """

    # Lists for random name generation
    ADJECTIVES = [
        "Brave", "Swift", "Clever", "Mighty", "Fierce",
        "Noble", "Cunning", "Bold", "Wise", "Strong",
        "Quick", "Silent", "Fearless", "Agile", "Sharp"
    ]

    ANIMALS = [
        "Tiger", "Lion", "Elephant", "Leopard", "Wolf",
        "Dog", "Cat", "Rat", "Eagle", "Bear",
        "Fox", "Hawk", "Panther", "Jaguar", "Cheetah"
    ]

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate a player name.

        A valid name must:
        - Not be empty after stripping whitespace
        - Be between 1 and 30 characters
        - Contain only alphanumeric characters, spaces, hyphens, and underscores

        Args:
            name: The name to validate

        Returns:
            True if name is valid, False otherwise
        """
        if not name or not name.strip():
            return False

        name = name.strip()

        # Check length
        if len(name) < 1 or len(name) > 30:
            return False

        # Check characters (alphanumeric, spaces, hyphens, underscores)
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_")
        if not all(c in allowed_chars for c in name):
            return False

        return True

    @staticmethod
    def generate_random_name() -> str:
        """
        Generate a random player name.

        Combines a random adjective with a random animal name.

        Returns:
            A randomly generated player name (e.g., "Brave Tiger")
        """
        adjective = random.choice(NameManager.ADJECTIVES)
        animal = random.choice(NameManager.ANIMALS)
        return f"{adjective} {animal}"

    @staticmethod
    def get_player_name(prompt: str, default_name: Optional[str] = None) -> str:
        """
        Get a player name from user input or generate a random one.

        Prompts the user for a name. If no input is provided:
        - Uses default_name if provided
        - Otherwise generates a random name

        Args:
            prompt: The prompt to display to the user
            default_name: Optional default name to use if no input provided

        Returns:
            A valid player name (either from input, default, or randomly generated)
        """
        while True:
            user_input = input(prompt).strip()

            # If no input provided
            if not user_input:
                if default_name:
                    return default_name
                # Generate random name
                random_name = NameManager.generate_random_name()
                print(f"No name provided. Using random name: {random_name}")
                return random_name

            # Validate the input
            if NameManager.validate_name(user_input):
                return user_input

            # Invalid name, ask again
            print("Invalid name. Name must be 1-30 characters and contain only "
                  "letters, numbers, spaces, hyphens, and underscores.")

    @staticmethod
    def get_player_names() -> tuple[str, str]:
        """
        Get names for both players.

        Prompts for both player names and returns them as a tuple.
        If no names are provided, random names are generated.

        Returns:
            Tuple of (player1_name, player2_name)
        """
        print("\n=== Player Name Setup ===")
        print("Press Enter without typing to get a random name.\n")

        player1_name = NameManager.get_player_name(
            "Enter name for Player 1 (Red): "
        )

        player2_name = NameManager.get_player_name(
            "Enter name for Player 2 (Blue): "
        )

        # Ensure names are different
        while player1_name == player2_name:
            print(f"\nBoth players cannot have the same name: '{player1_name}'")
            player2_name = NameManager.get_player_name(
                "Enter a different name for Player 2 (Blue): "
            )

        print(f"\nPlayer 1 (Red): {player1_name}")
        print(f"Player 2 (Blue): {player2_name}\n")

        return player1_name, player2_name
