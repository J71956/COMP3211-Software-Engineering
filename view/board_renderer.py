"""
BoardRenderer class for Jungle Game.
Handles ASCII art board rendering with piece symbols and terrain markers.
"""

from typing import Optional, TYPE_CHECKING
from model.enums import TerrainType, PlayerColor
from model.position import Position

if TYPE_CHECKING:
    from model.board import Board
    from model.piece import Piece


class BoardRenderer:
    """
    Renders the game board as ASCII art with piece symbols and terrain markers.

    The board is displayed with:
    - Row and column coordinates
    - Piece symbols (R=Rat, C=Cat, D=Dog, W=Wolf, P=Leopard, T=Tiger, L=Lion, E=Elephant)
    - Player ownership (lowercase=RED, uppercase=BLUE)
    - Terrain markers (~ for water, # for dens, * for traps)
    """

    # Piece type to symbol mapping
    PIECE_SYMBOLS = {
        'Rat': 'R',
        'Cat': 'C',
        'Dog': 'D',
        'Wolf': 'W',
        'Leopard': 'P',
        'Tiger': 'T',
        'Lion': 'L',
        'Elephant': 'E'
    }

    def __init__(self):
        """Initialize the BoardRenderer."""

    def render_board(self, board: 'Board') -> str:
        """
        Render the complete board as ASCII art.

        Args:
            board: The game board to render

        Returns:
            String representation of the board
        """
        lines = []

        # Add top border with column numbers
        lines.append("    " + " ".join(str(i) for i in range(board.BOARD_WIDTH)))
        lines.append("  +" + "-" * (board.BOARD_WIDTH * 2 - 1) + "+")

        # Render each row
        for row in range(board.BOARD_HEIGHT):
            row_str = f"{row} |"

            for col in range(board.BOARD_WIDTH):
                pos = Position(row, col)
                piece = board.get_piece(pos)
                terrain = board.get_terrain(pos)

                # Render the cell content
                cell_content = self._render_cell(piece, terrain)
                row_str += cell_content

                # Add separator between columns
                if col < board.BOARD_WIDTH - 1:
                    row_str += " "

            row_str += "|"
            lines.append(row_str)

        # Add bottom border
        lines.append("  +" + "-" * (board.BOARD_WIDTH * 2 - 1) + "+")

        return "\n".join(lines)

    def _render_cell(self, piece: Optional['Piece'], terrain: TerrainType) -> str:
        """
        Render a single cell with piece or terrain marker.

        Args:
            piece: The piece at this position (if any)
            terrain: The terrain type at this position

        Returns:
            Single character representing the cell
        """
        if piece is not None:
            return self.render_piece(piece)

        # Show terrain markers for special areas
        if terrain == TerrainType.WATER:
            return "~"
        elif terrain == TerrainType.DEN:
            return "#"
        elif terrain == TerrainType.TRAP:
            return "*"

        # Empty land square
        return "."

    def render_piece(self, piece: Optional['Piece']) -> str:
        """
        Render a piece as a symbol.

        Args:
            piece: The piece to render (or None for empty)

        Returns:
            Single character representing the piece
        """
        if piece is None:
            return "."

        # Get the piece type name
        piece_type = piece.__class__.__name__

        # Get the base symbol
        symbol = self.PIECE_SYMBOLS.get(piece_type, "?")

        # Use case to indicate ownership:
        # lowercase = RED player
        # uppercase = BLUE player
        if piece.owner.color == PlayerColor.RED:
            return symbol.lower()
        else:
            return symbol.upper()

    def render_terrain_markers(self) -> str:
        """
        Render a legend explaining terrain markers.

        Returns:
            String with terrain marker explanations
        """
        legend = [
            "Terrain Legend:",
            "  . = Land",
            "  ~ = Water",
            "  # = Den",
            "  * = Trap",
            "",
            "Piece Legend:",
            "  R/r = Rat (1)",
            "  C/c = Cat (2)",
            "  D/d = Dog (3)",
            "  W/w = Wolf (4)",
            "  P/p = Leopard (5)",
            "  T/t = Tiger (6)",
            "  L/l = Lion (7)",
            "  E/e = Elephant (8)",
            "",
            "  UPPERCASE = Blue Player",
            "  lowercase = Red Player"
        ]
        return "\n".join(legend)
