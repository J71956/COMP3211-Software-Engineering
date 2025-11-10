"""
Unit tests for Game class.
Tests game initialization, turn management, and core game functionality.
"""

import unittest
from model.game import Game, MoveResult, Move
from model.board import Board
from model.player import Player
from model.position import Position
from model.enums import PlayerColor, GameStatus
from model.piece import Rat, Cat, Dog, Wolf, Leopard, Tiger, Lion, Elephant


class TestGameInitialization(unittest.TestCase):
    """Test game initialization and setup."""

    def test_game_creation_default_names(self):
        """Test creating a game with default player names."""
        game = Game()

        self.assertIsNotNone(game)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0].name, "Player 1")
        self.assertEqual(game.players[1].name, "Player 2")

    def test_game_creation_custom_names(self):
        """Test creating a game with custom player names."""
        game = Game("Alice", "Bob")

        self.assertEqual(game.players[0].name, "Alice")
        self.assertEqual(game.players[1].name, "Bob")

    def test_player_colors(self):
        """Test that players have correct colors."""
        game = Game()

        self.assertEqual(game.players[0].color, PlayerColor.RED)
        self.assertEqual(game.players[1].color, PlayerColor.BLUE)

    def test_initial_game_status(self):
        """Test that game starts with ONGOING status."""
        game = Game()

        self.assertEqual(game.game_status, GameStatus.ONGOING)
        self.assertFalse(game.is_game_over())

    def test_initial_current_player(self):
        """Test that player 1 (Red) starts first."""
        game = Game()

        self.assertEqual(game.current_player_index, 0)
        self.assertEqual(game.get_current_player(), game.players[0])
        self.assertEqual(game.get_current_player().color, PlayerColor.RED)

    def test_board_initialized(self):
        """Test that board is properly initialized."""
        game = Game()

        self.assertIsNotNone(game.board)
        self.assertIsInstance(game.board, Board)

    def test_empty_move_history(self):
        """Test that move history starts empty."""
        game = Game()

        self.assertEqual(len(game.move_history), 0)

    def test_no_undo_available_initially(self):
        """Test that undo is not available at game start."""
        game = Game()

        self.assertFalse(game.can_undo())


class TestPieceInitialization(unittest.TestCase):
    """Test that pieces are correctly initialized on the board."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_red_pieces_count(self):
        """Test that red player has 8 pieces."""
        red_player = self.game.players[0]
        self.assertEqual(len(red_player.get_active_pieces()), 8)

    def test_blue_pieces_count(self):
        """Test that blue player has 8 pieces."""
        blue_player = self.game.players[1]
        self.assertEqual(len(blue_player.get_active_pieces()), 8)

    def test_total_pieces_on_board(self):
        """Test that all 16 pieces are placed on the board."""
        piece_count = 0
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                if self.game.board.get_piece(pos) is not None:
                    piece_count += 1

        self.assertEqual(piece_count, 16)

    def test_red_piece_positions(self):
        """Test that red pieces are in correct starting positions."""
        board = self.game.board

        # Row 6
        self.assertIsInstance(board.get_piece(Position(6, 0)), Lion)
        self.assertIsInstance(board.get_piece(Position(6, 6)), Tiger)

        # Row 7
        self.assertIsInstance(board.get_piece(Position(7, 1)), Dog)
        self.assertIsInstance(board.get_piece(Position(7, 5)), Cat)

        # Row 8
        self.assertIsInstance(board.get_piece(Position(8, 0)), Rat)
        self.assertIsInstance(board.get_piece(Position(8, 2)), Leopard)
        self.assertIsInstance(board.get_piece(Position(8, 4)), Wolf)
        self.assertIsInstance(board.get_piece(Position(8, 6)), Elephant)

    def test_blue_piece_positions(self):
        """Test that blue pieces are in correct starting positions."""
        board = self.game.board

        # Row 0
        self.assertIsInstance(board.get_piece(Position(0, 0)), Elephant)
        self.assertIsInstance(board.get_piece(Position(0, 2)), Wolf)
        self.assertIsInstance(board.get_piece(Position(0, 4)), Leopard)
        self.assertIsInstance(board.get_piece(Position(0, 6)), Rat)

        # Row 1
        self.assertIsInstance(board.get_piece(Position(1, 1)), Cat)
        self.assertIsInstance(board.get_piece(Position(1, 5)), Dog)

        # Row 2
        self.assertIsInstance(board.get_piece(Position(2, 0)), Tiger)
        self.assertIsInstance(board.get_piece(Position(2, 6)), Lion)

    def test_red_piece_ownership(self):
        """Test that red pieces belong to red player."""
        red_player = self.game.players[0]
        board = self.game.board

        red_positions = [
            Position(6, 0), Position(6, 6),
            Position(7, 1), Position(7, 5),
            Position(8, 0), Position(8, 2), Position(8, 4), Position(8, 6)
        ]

        for pos in red_positions:
            piece = board.get_piece(pos)
            self.assertIsNotNone(piece)
            self.assertEqual(piece.owner, red_player)
            self.assertEqual(piece.owner.color, PlayerColor.RED)

    def test_blue_piece_ownership(self):
        """Test that blue pieces belong to blue player."""
        blue_player = self.game.players[1]
        board = self.game.board

        blue_positions = [
            Position(0, 0), Position(0, 2), Position(0, 4), Position(0, 6),
            Position(1, 1), Position(1, 5),
            Position(2, 0), Position(2, 6)
        ]

        for pos in blue_positions:
            piece = board.get_piece(pos)
            self.assertIsNotNone(piece)
            self.assertEqual(piece.owner, blue_player)
            self.assertEqual(piece.owner.color, PlayerColor.BLUE)

    def test_middle_rows_empty(self):
        """Test that middle rows (3-5) are empty except for river."""
        board = self.game.board

        for row in range(3, 6):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                self.assertIsNone(board.get_piece(pos))

    def test_piece_ranks(self):
        """Test that pieces have correct ranks."""
        board = self.game.board

        # Test a few specific pieces
        rat = board.get_piece(Position(8, 0))
        self.assertEqual(rat.rank, 1)

        cat = board.get_piece(Position(7, 5))
        self.assertEqual(cat.rank, 2)

        elephant = board.get_piece(Position(8, 6))
        self.assertEqual(elephant.rank, 8)

        lion = board.get_piece(Position(6, 0))
        self.assertEqual(lion.rank, 7)


class TestTurnManagement(unittest.TestCase):
    """Test turn management and player switching."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game("Player 1", "Player 2")

    def test_initial_turn(self):
        """Test that player 1 (Red) has the first turn."""
        self.assertEqual(self.game.current_player_index, 0)
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

    def test_get_current_player(self):
        """Test getting the current player."""
        current = self.game.get_current_player()

        self.assertIsNotNone(current)
        self.assertEqual(current, self.game.players[0])
        self.assertEqual(current.name, "Player 1")

    def test_get_opponent_player(self):
        """Test getting the opponent player."""
        opponent = self.game.get_opponent_player()

        self.assertIsNotNone(opponent)
        self.assertEqual(opponent, self.game.players[1])
        self.assertEqual(opponent.name, "Player 2")

    def test_switch_turn(self):
        """Test switching turns between players."""
        # Initially player 1
        self.assertEqual(self.game.current_player_index, 0)

        # Switch to player 2
        self.game._switch_turn()
        self.assertEqual(self.game.current_player_index, 1)
        self.assertEqual(self.game.get_current_player().color, PlayerColor.BLUE)

        # Switch back to player 1
        self.game._switch_turn()
        self.assertEqual(self.game.current_player_index, 0)
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

    def test_opponent_changes_with_turn(self):
        """Test that opponent changes when turn switches."""
        # Initially player 1 is current, player 2 is opponent
        self.assertEqual(self.game.get_current_player().name, "Player 1")
        self.assertEqual(self.game.get_opponent_player().name, "Player 2")

        # After switch, player 2 is current, player 1 is opponent
        self.game._switch_turn()
        self.assertEqual(self.game.get_current_player().name, "Player 2")
        self.assertEqual(self.game.get_opponent_player().name, "Player 1")


class TestGameStatus(unittest.TestCase):
    """Test game status and winner determination."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_initial_status_ongoing(self):
        """Test that game starts with ONGOING status."""
        self.assertEqual(self.game.game_status, GameStatus.ONGOING)
        self.assertFalse(self.game.is_game_over())

    def test_no_winner_initially(self):
        """Test that there is no winner at game start."""
        self.assertIsNone(self.game.get_winner())

    def test_player_one_wins_status(self):
        """Test player one wins status."""
        self.game._game_status = GameStatus.PLAYER_ONE_WINS

        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winner(), self.game.players[0])

    def test_player_two_wins_status(self):
        """Test player two wins status."""
        self.game._game_status = GameStatus.PLAYER_TWO_WINS

        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winner(), self.game.players[1])

    def test_draw_status(self):
        """Test draw status."""
        self.game._game_status = GameStatus.DRAW

        self.assertTrue(self.game.is_game_over())
        self.assertIsNone(self.game.get_winner())


class TestGameProperties(unittest.TestCase):
    """Test game property accessors."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game("Alice", "Bob")

    def test_board_property(self):
        """Test board property returns the game board."""
        board = self.game.board

        self.assertIsNotNone(board)
        self.assertIsInstance(board, Board)

    def test_players_property_returns_copy(self):
        """Test that players property returns a copy."""
        players1 = self.game.players
        players2 = self.game.players

        # Should be equal but not the same object
        self.assertEqual(players1, players2)
        self.assertIsNot(players1, players2)

    def test_move_history_property_returns_copy(self):
        """Test that move history property returns a copy."""
        history1 = self.game.move_history
        history2 = self.game.move_history

        # Should be equal but not the same object
        self.assertEqual(history1, history2)
        self.assertIsNot(history1, history2)

    def test_current_player_index_property(self):
        """Test current player index property."""
        self.assertEqual(self.game.current_player_index, 0)

        self.game._switch_turn()
        self.assertEqual(self.game.current_player_index, 1)

    def test_game_status_property(self):
        """Test game status property."""
        self.assertEqual(self.game.game_status, GameStatus.ONGOING)

        self.game._game_status = GameStatus.PLAYER_ONE_WINS
        self.assertEqual(self.game.game_status, GameStatus.PLAYER_ONE_WINS)


class TestGameStringRepresentation(unittest.TestCase):
    """Test string representations of the game."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game("Alice", "Bob")

    def test_str_representation(self):
        """Test __str__ method."""
        game_str = str(self.game)

        self.assertIn("Game", game_str)
        self.assertIn("Alice", game_str)
        self.assertIn("ongoing", game_str)

    def test_repr_representation(self):
        """Test __repr__ method."""
        game_repr = repr(self.game)

        self.assertIn("Game", game_repr)


if __name__ == '__main__':
    unittest.main()



class TestMoveValidation(unittest.TestCase):
    """Test move validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_move_from_invalid_source_position(self):
        """Test moving from an invalid position."""
        result = self.game.make_move(Position(-1, 0), Position(0, 0))

        self.assertFalse(result.success)
        self.assertIn("Invalid source position", result.message)

    def test_move_to_invalid_target_position(self):
        """Test moving to an invalid position."""
        result = self.game.make_move(Position(8, 0), Position(10, 10))

        self.assertFalse(result.success)
        self.assertIn("Invalid target position", result.message)

    def test_move_from_empty_square(self):
        """Test moving from an empty square."""
        result = self.game.make_move(Position(4, 3), Position(5, 3))

        self.assertFalse(result.success)
        self.assertIn("No piece at position", result.message)

    def test_move_opponent_piece(self):
        """Test trying to move opponent's piece."""
        # Red player tries to move blue piece
        result = self.game.make_move(Position(0, 0), Position(1, 0))

        self.assertFalse(result.success)
        self.assertIn("belongs to", result.message)

    def test_move_to_own_piece(self):
        """Test trying to move to a square occupied by own piece."""
        # Try to move red rat to red leopard's position
        result = self.game.make_move(Position(8, 0), Position(8, 2))

        self.assertFalse(result.success)

    def test_invalid_move_pattern(self):
        """Test moving with invalid pattern (e.g., diagonal)."""
        # Try to move rat diagonally
        result = self.game.make_move(Position(8, 0), Position(7, 1))

        self.assertFalse(result.success)
        self.assertIn("cannot move to", result.message)

    def test_move_to_own_den(self):
        """Test that pieces cannot move to their own den."""
        # Clear path and try to move red piece to red den
        self.game._board.set_piece(Position(7, 3), None)

        # Move red wolf towards its own den
        self.game._board.set_piece(Position(7, 3),
                                   self.game._board.get_piece(Position(8, 4)))
        self.game._board.get_piece(Position(7, 3)).position = Position(7, 3)
        self.game._board.set_piece(Position(8, 4), None)

        result = self.game.make_move(Position(7, 3), Position(8, 3))

        self.assertFalse(result.success)


class TestMoveExecution(unittest.TestCase):
    """Test move execution and state changes."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_valid_move_execution(self):
        """Test executing a valid move."""
        # Move red rat forward
        result = self.game.make_move(Position(8, 0), Position(7, 0))

        self.assertTrue(result.success)
        self.assertIn("moved", result.message)

    def test_piece_position_updated(self):
        """Test that piece position is updated after move."""
        from_pos = Position(8, 0)
        to_pos = Position(7, 0)

        piece = self.game.board.get_piece(from_pos)
        self.game.make_move(from_pos, to_pos)

        # Check piece is at new position
        self.assertEqual(piece.position, to_pos)
        self.assertEqual(self.game.board.get_piece(to_pos), piece)

    def test_source_square_cleared(self):
        """Test that source square is cleared after move."""
        from_pos = Position(8, 0)
        to_pos = Position(7, 0)

        self.game.make_move(from_pos, to_pos)

        # Source should be empty
        self.assertIsNone(self.game.board.get_piece(from_pos))

    def test_turn_switches_after_move(self):
        """Test that turn switches after a successful move."""
        # Initially red player's turn
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        # Should now be blue player's turn
        self.assertEqual(self.game.get_current_player().color, PlayerColor.BLUE)

    def test_move_recorded_in_history(self):
        """Test that moves are recorded in history."""
        initial_count = len(self.game.move_history)

        self.game.make_move(Position(8, 0), Position(7, 0))

        self.assertEqual(len(self.game.move_history), initial_count + 1)

    def test_move_history_contains_correct_info(self):
        """Test that move history contains correct information."""
        from_pos = Position(8, 0)
        to_pos = Position(7, 0)

        piece = self.game.board.get_piece(from_pos)
        self.game.make_move(from_pos, to_pos)

        last_move = self.game.move_history[-1]
        self.assertEqual(last_move.piece, piece)
        self.assertEqual(last_move.from_pos, from_pos)
        self.assertEqual(last_move.to_pos, to_pos)
        self.assertIsNone(last_move.captured_piece)

    def test_game_state_saved_for_undo(self):
        """Test that game state is saved after move."""
        initial_states = len(self.game._game_states)

        self.game.make_move(Position(8, 0), Position(7, 0))

        self.assertEqual(len(self.game._game_states), initial_states + 1)
        self.assertTrue(self.game.can_undo())


class TestCaptureMechanics(unittest.TestCase):
    """Test piece capture mechanics."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_capture_opponent_piece(self):
        """Test capturing an opponent's piece."""
        # Set up a capture scenario: red dog (rank 3) captures blue rat (rank 1)
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Red dog captures blue rat
        result = self.game.make_move(Position(7, 1), Position(6, 1))

        self.assertTrue(result.success)
        self.assertIsNotNone(result.captured_piece)
        self.assertEqual(result.captured_piece, blue_rat)

    def test_captured_piece_removed_from_board(self):
        """Test that captured piece is removed from board."""
        # Set up capture scenario: red dog captures blue rat
        blue_rat = self.game.board.get_piece(Position(0, 6))
        red_dog = self.game.board.get_piece(Position(7, 1))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Capture
        self.game.make_move(Position(7, 1), Position(6, 1))

        # Blue rat should not be on board, red dog should be there
        piece_at_pos = self.game.board.get_piece(Position(6, 1))
        self.assertIsNotNone(piece_at_pos)
        self.assertEqual(piece_at_pos, red_dog)
        self.assertNotEqual(piece_at_pos, blue_rat)

    def test_captured_piece_removed_from_player(self):
        """Test that captured piece is removed from player's collection."""
        blue_player = self.game.players[1]
        initial_count = len(blue_player.get_active_pieces())

        # Set up capture scenario: red dog captures blue rat
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Capture
        self.game.make_move(Position(7, 1), Position(6, 1))

        # Blue player should have one less piece
        self.assertEqual(len(blue_player.get_active_pieces()), initial_count - 1)
        self.assertNotIn(blue_rat, blue_player.get_active_pieces())

    def test_capture_message(self):
        """Test that capture is mentioned in result message."""
        # Set up capture scenario: red dog captures blue rat
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        result = self.game.make_move(Position(7, 1), Position(6, 1))

        self.assertIn("captured", result.message)

    def test_invalid_capture_rank_based(self):
        """Test that lower rank cannot capture higher rank."""
        # Set up: red cat vs blue elephant
        red_cat = self.game.board.get_piece(Position(7, 5))
        blue_elephant = self.game.board.get_piece(Position(0, 0))

        # Move blue elephant to be capturable position
        self.game._board.set_piece(Position(0, 0), None)
        self.game._board.set_piece(Position(6, 5), blue_elephant)
        blue_elephant.position = Position(6, 5)

        # Try to capture with cat (rank 2 vs rank 8)
        result = self.game.make_move(Position(7, 5), Position(6, 5))

        self.assertFalse(result.success)
        self.assertIn("cannot capture", result.message)

    def test_move_history_records_capture(self):
        """Test that move history records captured piece."""
        # Set up capture scenario: red dog captures blue rat
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        self.game.make_move(Position(7, 1), Position(6, 1))

        last_move = self.game.move_history[-1]
        self.assertEqual(last_move.captured_piece, blue_rat)


class TestGameOverRestrictions(unittest.TestCase):
    """Test that moves cannot be made after game is over."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_cannot_move_after_game_over(self):
        """Test that moves are rejected after game is over."""
        from model.exceptions import GameOverException

        # Set game to over
        self.game._game_status = GameStatus.PLAYER_ONE_WINS

        # Try to make a move
        with self.assertRaises(GameOverException):
            self.game.make_move(Position(8, 0), Position(7, 0))


class TestMultipleMoves(unittest.TestCase):
    """Test sequences of multiple moves."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_alternating_turns(self):
        """Test that players alternate turns."""
        # Red move
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)
        self.game.make_move(Position(8, 0), Position(7, 0))

        # Blue move
        self.assertEqual(self.game.get_current_player().color, PlayerColor.BLUE)
        self.game.make_move(Position(0, 6), Position(1, 6))

        # Red move again
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

    def test_multiple_moves_recorded(self):
        """Test that multiple moves are all recorded."""
        # Make several moves
        self.game.make_move(Position(8, 0), Position(7, 0))  # Red rat forward
        self.game.make_move(Position(0, 6), Position(1, 6))  # Blue rat forward
        self.game.make_move(Position(8, 2), Position(7, 2))  # Red leopard forward

        self.assertEqual(len(self.game.move_history), 3)

    def test_max_undo_states_maintained(self):
        """Test that only MAX_UNDO_MOVES states are kept."""
        # Make more than MAX_UNDO_MOVES moves
        moves = [
            (Position(8, 0), Position(7, 0)),  # Red rat
            (Position(0, 6), Position(1, 6)),  # Blue rat
            (Position(7, 0), Position(6, 0)),  # Red rat
            (Position(1, 6), Position(2, 6)),  # Blue rat
            (Position(6, 0), Position(5, 0)),  # Red rat
        ]

        for from_pos, to_pos in moves:
            self.game.make_move(from_pos, to_pos)

        # Should have at most MAX_UNDO_MOVES states
        self.assertLessEqual(len(self.game._game_states), Game.MAX_UNDO_MOVES)



class TestVictoryConditions(unittest.TestCase):
    """Test victory condition detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_victory_by_reaching_opponent_den(self):
        """Test victory when a piece reaches opponent's den."""
        # Clear the path and move red rat to blue den
        red_rat = self.game.board.get_piece(Position(8, 0))

        # Move rat directly to blue den (position 0, 3)
        self.game._board.set_piece(Position(8, 0), None)
        self.game._board.set_piece(Position(1, 3), red_rat)
        red_rat.position = Position(1, 3)

        # Make the winning move
        result = self.game.make_move(Position(1, 3), Position(0, 3))

        self.assertTrue(result.success)
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.PLAYER_ONE_WINS)
        self.assertEqual(self.game.get_winner(), self.game.players[0])

    def test_victory_by_capturing_all_opponent_pieces(self):
        """Test victory when all opponent pieces are captured."""
        # Remove all blue pieces except one rat
        blue_player = self.game.players[1]
        blue_pieces = list(blue_player.get_active_pieces())

        # Find blue rat and keep it, remove all others
        blue_rat = None
        for piece in blue_pieces:
            if piece.rank == 1:  # Rat
                blue_rat = piece
            else:
                self.game._board.set_piece(piece.position, None)
                blue_player.remove_piece(piece)

        # Set up the blue rat to be captured by red dog
        self.game._board.set_piece(blue_rat.position, None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Red dog captures the last blue piece (rat)
        result = self.game.make_move(Position(7, 1), Position(6, 1))

        self.assertTrue(result.success)
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.PLAYER_ONE_WINS)
        self.assertEqual(self.game.get_winner(), self.game.players[0])

    def test_blue_player_victory_by_den(self):
        """Test blue player victory by reaching red den."""
        # Move blue rat to red den
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(7, 3), blue_rat)
        blue_rat.position = Position(7, 3)

        # Switch to blue player's turn
        self.game._switch_turn()

        # Make the winning move
        result = self.game.make_move(Position(7, 3), Position(8, 3))

        self.assertTrue(result.success)
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.PLAYER_TWO_WINS)
        self.assertEqual(self.game.get_winner(), self.game.players[1])

    def test_blue_player_victory_by_capture_all(self):
        """Test blue player victory by capturing all red pieces."""
        # Remove all red pieces except one rat
        red_player = self.game.players[0]
        red_pieces = list(red_player.get_active_pieces())

        # Find red rat and keep it, remove all others
        red_rat = None
        for piece in red_pieces:
            if piece.rank == 1:  # Rat
                red_rat = piece
            else:
                self.game._board.set_piece(piece.position, None)
                red_player.remove_piece(piece)

        # Set up the red rat to be captured by blue cat
        self.game._board.set_piece(red_rat.position, None)
        self.game._board.set_piece(Position(2, 1), red_rat)
        red_rat.position = Position(2, 1)

        # Switch to blue player's turn
        self.game._switch_turn()

        # Blue cat captures the last red piece (rat)
        result = self.game.make_move(Position(1, 1), Position(2, 1))

        self.assertTrue(result.success)
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.PLAYER_TWO_WINS)
        self.assertEqual(self.game.get_winner(), self.game.players[1])

    def test_no_turn_switch_after_victory(self):
        """Test that turn doesn't switch after game ends."""
        # Set up victory scenario
        red_rat = self.game.board.get_piece(Position(8, 0))
        self.game._board.set_piece(Position(8, 0), None)
        self.game._board.set_piece(Position(1, 3), red_rat)
        red_rat.position = Position(1, 3)

        # Current player should be red
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

        # Make winning move
        self.game.make_move(Position(1, 3), Position(0, 3))

        # Turn should not have switched (still red player)
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

    def test_game_continues_without_victory(self):
        """Test that game continues when no victory condition is met."""
        # Make a normal move
        result = self.game.make_move(Position(8, 0), Position(7, 0))

        self.assertTrue(result.success)
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.ONGOING)
        self.assertIsNone(self.game.get_winner())

    def test_capture_without_eliminating_all_pieces(self):
        """Test that capturing a piece doesn't end game if opponent has more pieces."""
        # Set up a capture that doesn't eliminate all pieces
        blue_rat = self.game.board.get_piece(Position(0, 6))
        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Red dog captures blue rat
        result = self.game.make_move(Position(7, 1), Position(6, 1))

        self.assertTrue(result.success)
        self.assertFalse(self.game.is_game_over())
        self.assertEqual(self.game.game_status, GameStatus.ONGOING)


class TestGameEndingBehavior(unittest.TestCase):
    """Test game behavior after ending."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_winner_determination_player_one(self):
        """Test correct winner determination for player one."""
        self.game._game_status = GameStatus.PLAYER_ONE_WINS

        winner = self.game.get_winner()
        self.assertEqual(winner, self.game.players[0])
        self.assertEqual(winner.color, PlayerColor.RED)

    def test_winner_determination_player_two(self):
        """Test correct winner determination for player two."""
        self.game._game_status = GameStatus.PLAYER_TWO_WINS

        winner = self.game.get_winner()
        self.assertEqual(winner, self.game.players[1])
        self.assertEqual(winner.color, PlayerColor.BLUE)

    def test_no_winner_for_draw(self):
        """Test that draw status returns no winner."""
        self.game._game_status = GameStatus.DRAW

        self.assertIsNone(self.game.get_winner())

    def test_no_winner_for_ongoing(self):
        """Test that ongoing game returns no winner."""
        self.assertEqual(self.game.game_status, GameStatus.ONGOING)
        self.assertIsNone(self.game.get_winner())

    def test_is_game_over_for_all_statuses(self):
        """Test is_game_over for all game statuses."""
        # Ongoing
        self.game._game_status = GameStatus.ONGOING
        self.assertFalse(self.game.is_game_over())

        # Player one wins
        self.game._game_status = GameStatus.PLAYER_ONE_WINS
        self.assertTrue(self.game.is_game_over())

        # Player two wins
        self.game._game_status = GameStatus.PLAYER_TWO_WINS
        self.assertTrue(self.game.is_game_over())

        # Draw
        self.game._game_status = GameStatus.DRAW
        self.assertTrue(self.game.is_game_over())



class TestUndoFunctionality(unittest.TestCase):
    """Test undo functionality and state restoration."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_undo_simple_move(self):
        """Test undoing a simple move."""
        # Make a move
        from_pos = Position(8, 0)
        to_pos = Position(7, 0)
        piece = self.game.board.get_piece(from_pos)

        self.game.make_move(from_pos, to_pos)

        # Undo the move
        result = self.game.undo_move()

        self.assertTrue(result)
        # Piece should be back at original position
        self.assertEqual(self.game.board.get_piece(from_pos), piece)
        self.assertIsNone(self.game.board.get_piece(to_pos))
        self.assertEqual(piece.position, from_pos)

    def test_undo_restores_current_player(self):
        """Test that undo restores the current player."""
        # Initially red player
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

        # Make a move (switches to blue)
        self.game.make_move(Position(8, 0), Position(7, 0))
        self.assertEqual(self.game.get_current_player().color, PlayerColor.BLUE)

        # Undo (should restore to red)
        self.game.undo_move()
        self.assertEqual(self.game.get_current_player().color, PlayerColor.RED)

    def test_undo_removes_move_from_history(self):
        """Test that undo removes the move from history."""
        initial_count = len(self.game.move_history)

        self.game.make_move(Position(8, 0), Position(7, 0))
        self.assertEqual(len(self.game.move_history), initial_count + 1)

        self.game.undo_move()
        self.assertEqual(len(self.game.move_history), initial_count)

    def test_undo_with_capture(self):
        """Test undoing a move that captured a piece."""
        # Set up capture scenario
        blue_rat = self.game.board.get_piece(Position(0, 6))
        blue_player = self.game.players[1]
        initial_blue_pieces = len(blue_player.get_active_pieces())

        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(Position(6, 1), blue_rat)
        blue_rat.position = Position(6, 1)

        # Red dog captures blue rat
        self.game.make_move(Position(7, 1), Position(6, 1))

        # Blue player should have one less piece
        self.assertEqual(len(blue_player.get_active_pieces()), initial_blue_pieces - 1)

        # Undo the capture
        self.game.undo_move()

        # Blue rat should be restored to player's collection
        self.assertEqual(len(blue_player.get_active_pieces()), initial_blue_pieces)
        self.assertIn(blue_rat, blue_player.get_active_pieces())

    def test_undo_restores_captured_piece_position(self):
        """Test that undo restores captured piece to correct position."""
        # Set up capture scenario
        blue_rat = self.game.board.get_piece(Position(0, 6))
        capture_pos = Position(6, 1)

        self.game._board.set_piece(Position(0, 6), None)
        self.game._board.set_piece(capture_pos, blue_rat)
        blue_rat.position = capture_pos

        # Capture
        self.game.make_move(Position(7, 1), Position(6, 1))

        # Undo
        self.game.undo_move()

        # Blue rat should be back at capture position
        self.assertEqual(self.game.board.get_piece(capture_pos), blue_rat)
        self.assertEqual(blue_rat.position, capture_pos)

    def test_cannot_undo_when_no_moves(self):
        """Test that undo returns False when no moves to undo."""
        result = self.game.undo_move()

        self.assertFalse(result)

    def test_cannot_undo_after_game_over(self):
        """Test that undo raises exception after game is over."""
        from model.exceptions import GameOverException

        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        # Set game to over
        self.game._game_status = GameStatus.PLAYER_ONE_WINS

        # Try to undo
        with self.assertRaises(GameOverException):
            self.game.undo_move()

    def test_multiple_undos(self):
        """Test undoing multiple moves in sequence."""
        # Make three moves
        moves = [
            (Position(8, 0), Position(7, 0)),  # Red rat
            (Position(0, 6), Position(1, 6)),  # Blue rat
            (Position(8, 2), Position(7, 2)),  # Red leopard
        ]

        for from_pos, to_pos in moves:
            self.game.make_move(from_pos, to_pos)

        self.assertEqual(len(self.game.move_history), 3)

        # Undo all three moves
        self.assertTrue(self.game.undo_move())
        self.assertEqual(len(self.game.move_history), 2)

        self.assertTrue(self.game.undo_move())
        self.assertEqual(len(self.game.move_history), 1)

        self.assertTrue(self.game.undo_move())
        self.assertEqual(len(self.game.move_history), 0)

        # No more moves to undo
        self.assertFalse(self.game.undo_move())

    def test_max_undo_limit(self):
        """Test that only MAX_UNDO_MOVES states are kept."""
        # Make more than MAX_UNDO_MOVES moves
        moves = [
            (Position(8, 0), Position(7, 0)),  # 1
            (Position(0, 6), Position(1, 6)),  # 2
            (Position(7, 0), Position(6, 0)),  # 3
            (Position(1, 6), Position(2, 6)),  # 4
            (Position(6, 0), Position(5, 0)),  # 5
        ]

        for from_pos, to_pos in moves:
            self.game.make_move(from_pos, to_pos)

        # Should only have MAX_UNDO_MOVES (3) states saved
        self.assertEqual(len(self.game._game_states), Game.MAX_UNDO_MOVES)

        # Should only be able to undo MAX_UNDO_MOVES (3) times
        undo_count = 0
        initial_history_count = len(self.game.move_history)
        while self.game.can_undo():
            self.game.undo_move()
            undo_count += 1

        self.assertEqual(undo_count, Game.MAX_UNDO_MOVES)
        # After undoing 3 moves, history should have 3 fewer moves
        self.assertEqual(len(self.game.move_history), initial_history_count - Game.MAX_UNDO_MOVES)

    def test_undo_and_make_new_move(self):
        """Test making a new move after undo."""
        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        # Undo it
        self.game.undo_move()

        # Make a different move
        result = self.game.make_move(Position(8, 2), Position(7, 2))

        self.assertTrue(result.success)
        self.assertEqual(len(self.game.move_history), 1)

    def test_can_undo_returns_correct_value(self):
        """Test that can_undo returns correct value."""
        # Initially no moves
        self.assertFalse(self.game.can_undo())

        # After a move
        self.game.make_move(Position(8, 0), Position(7, 0))
        self.assertTrue(self.game.can_undo())

        # After undo
        self.game.undo_move()
        self.assertFalse(self.game.can_undo())

    def test_undo_preserves_board_state_completely(self):
        """Test that undo restores complete board state."""
        # Record initial board state
        initial_pieces = {}
        for row in range(Board.BOARD_HEIGHT):
            for col in range(Board.BOARD_WIDTH):
                pos = Position(row, col)
                piece = self.game.board.get_piece(pos)
                if piece is not None:
                    initial_pieces[pos] = piece

        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))

        # Undo
        self.game.undo_move()

        # Check all pieces are back in original positions
        for pos, piece in initial_pieces.items():
            self.assertEqual(self.game.board.get_piece(pos), piece)
            self.assertEqual(piece.position, pos)

    def test_undo_state_count_management(self):
        """Test that game state count is properly managed."""
        # Initially no states
        self.assertEqual(len(self.game._game_states), 0)

        # Make a move
        self.game.make_move(Position(8, 0), Position(7, 0))
        self.assertEqual(len(self.game._game_states), 1)

        # Undo
        self.game.undo_move()
        self.assertEqual(len(self.game._game_states), 0)
