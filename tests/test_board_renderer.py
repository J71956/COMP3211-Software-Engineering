"""
Unit tests for BoardRenderer class.
Tests board rendering with various game states.
"""

import unittest
from model.board import Board
from model.player import Player
from model.piece import Rat, Cat, Dog, Wolf, Leopard, Tiger, Lion, Elephant
from model.enums import PlayerColor
from model.position import Position
from view.board_renderer import BoardRenderer


class TestBoardRenderer(unittest.TestCase):
    """Test cases for BoardRenderer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.renderer = BoardRenderer()
        self.board = Board()
        self.red_player = Player("Red", PlayerColor.RED)
        self.blue_player = Player("Blue", PlayerColor.BLUE)

    def test_render_empty_board(self):
        """Test rendering an empty board shows terrain markers."""
        result = self.renderer.render_board(self.board)

        # Check that result is a string
        self.assertIsInstance(result, str)

        # Check for column numbers
        self.assertIn("0 1 2 3 4 5 6", result)

        # Check for row numbers
        for i in range(9):
            self.assertIn(f"{i} |", result)

        # Check for terrain markers
        self.assertIn("~", result)  # Water
        self.assertIn("#", result)  # Den
        self.assertIn("*", result)  # Trap
        self.assertIn(".", result)  # Land

    def test_render_piece_red_player(self):
        """Test rendering pieces for red player shows lowercase symbols."""
        rat = Rat(self.red_player, Position(0, 0))
        self.red_player.add_piece(rat)

        symbol = self.renderer.render_piece(rat)
        self.assertEqual(symbol, "r")

        cat = Cat(self.red_player, Position(0, 0))
        symbol = self.renderer.render_piece(cat)
        self.assertEqual(symbol, "c")

    def test_render_piece_blue_player(self):
        """Test rendering pieces for blue player shows uppercase symbols."""
        rat = Rat(self.blue_player, Position(0, 0))
        self.blue_player.add_piece(rat)

        symbol = self.renderer.render_piece(rat)
        self.assertEqual(symbol, "R")

        elephant = Elephant(self.blue_player, Position(0, 0))
        symbol = self.renderer.render_piece(elephant)
        self.assertEqual(symbol, "E")

    def test_render_all_piece_types(self):
        """Test that all piece types have correct symbols."""
        pieces = [
            (Rat, 'r', 'R'),
            (Cat, 'c', 'C'),
            (Dog, 'd', 'D'),
            (Wolf, 'w', 'W'),
            (Leopard, 'p', 'P'),
            (Tiger, 't', 'T'),
            (Lion, 'l', 'L'),
            (Elephant, 'e', 'E')
        ]

        for piece_class, red_symbol, blue_symbol in pieces:
            red_piece = piece_class(self.red_player, Position(0, 0))
            blue_piece = piece_class(self.blue_player, Position(0, 0))

            self.assertEqual(self.renderer.render_piece(red_piece), red_symbol)
            self.assertEqual(self.renderer.render_piece(blue_piece), blue_symbol)

    def test_render_board_with_pieces(self):
        """Test rendering board with pieces placed."""
        # Place some pieces on the board
        rat = Rat(self.red_player, Position(2, 0))
        self.board.set_piece(Position(2, 0), rat)

        elephant = Elephant(self.blue_player, Position(0, 6))
        self.board.set_piece(Position(0, 6), elephant)

        result = self.renderer.render_board(self.board)

        # Check that pieces appear in the output
        self.assertIn("r", result)  # Red rat
        self.assertIn("E", result)  # Blue elephant

    def test_render_none_piece(self):
        """Test rendering None returns empty marker."""
        symbol = self.renderer.render_piece(None)
        self.assertEqual(symbol, ".")

    def test_render_terrain_markers_legend(self):
        """Test terrain markers legend is properly formatted."""
        legend = self.renderer.render_terrain_markers()

        # Check for terrain explanations
        self.assertIn("Land", legend)
        self.assertIn("Water", legend)
        self.assertIn("Den", legend)
        self.assertIn("Trap", legend)

        # Check for piece explanations
        self.assertIn("Rat", legend)
        self.assertIn("Elephant", legend)
        self.assertIn("UPPERCASE", legend)
        self.assertIn("lowercase", legend)

    def test_board_structure(self):
        """Test that rendered board has correct structure."""
        result = self.renderer.render_board(self.board)
        lines = result.split("\n")

        # Should have header + 9 rows + footer = 12 lines
        self.assertEqual(len(lines), 12)

        # Check borders
        self.assertTrue(lines[1].startswith("  +"))
        self.assertTrue(lines[-1].startswith("  +"))

    def test_water_terrain_rendering(self):
        """Test that water squares are rendered correctly."""
        result = self.renderer.render_board(self.board)

        # Water should be at rows 3-5, columns 1-2 and 4-5
        lines = result.split("\n")

        # Check row 3 (index 5 in output: header line + border + rows 0-2 + row 3)
        row_3 = lines[5]
        # Water should appear at positions for columns 1, 2, 4, 5
        self.assertIn("~", row_3)

    def test_den_terrain_rendering(self):
        """Test that dens are rendered correctly."""
        result = self.renderer.render_board(self.board)

        # Dens should be at (0, 3) for blue and (8, 3) for red
        lines = result.split("\n")

        # Check row 0 (index 2 in output)
        row_0 = lines[2]
        self.assertIn("#", row_0)

        # Check row 8 (index 10 in output)
        row_8 = lines[10]
        self.assertIn("#", row_8)

    def test_trap_terrain_rendering(self):
        """Test that traps are rendered correctly."""
        result = self.renderer.render_board(self.board)

        # Traps should appear in the output
        self.assertIn("*", result)

        lines = result.split("\n")

        # Blue traps at rows 0-1
        row_0 = lines[2]
        row_1 = lines[3]
        self.assertIn("*", row_0)
        self.assertIn("*", row_1)

        # Red traps at rows 7-8
        row_7 = lines[9]
        row_8 = lines[10]
        self.assertIn("*", row_7)
        self.assertIn("*", row_8)

    def test_piece_on_special_terrain(self):
        """Test that pieces override terrain markers when placed."""
        # Place a piece on a trap
        rat = Rat(self.red_player, Position(0, 2))
        self.board.set_piece(Position(0, 2), rat)

        result = self.renderer.render_board(self.board)

        # The piece symbol should appear, not the trap marker
        self.assertIn("r", result)


if __name__ == '__main__':
    unittest.main()
