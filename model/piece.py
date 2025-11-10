"""
Piece classes for Jungle Game.
Defines the abstract Piece base class and concrete piece implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

from model.position import Position
from model.enums import PlayerColor

if TYPE_CHECKING:
    from model.board import Board
    from model.player import Player


class Piece(ABC):
    """
    Abstract base class for all game pieces.
    
    Attributes:
        rank: The piece's rank (1-8, where 8 is strongest)
        owner: The player who owns this piece
        position: Current position on the board
    """
    
    def __init__(self, rank: int, owner: 'Player', position: Position):
        """
        Initialize a piece.
        
        Args:
            rank: The piece's rank (1-8)
            owner: The player who owns this piece
            position: Initial position on the board
        """
        self._rank = rank
        self._owner = owner
        self._position = position
    
    @property
    def rank(self) -> int:
        """Get the piece's rank."""
        return self._rank
    
    @property
    def owner(self) -> 'Player':
        """Get the piece's owner."""
        return self._owner
    
    @property
    def position(self) -> Position:
        """Get the piece's current position."""
        return self._position
    
    @position.setter
    def position(self, new_position: Position) -> None:
        """Set the piece's position."""
        self._position = new_position
    
    @abstractmethod
    def can_move_to(self, board: 'Board', target: Position) -> bool:
        """
        Check if this piece can move to the target position.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the move is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def can_capture(self, target_piece: 'Piece', board: 'Board') -> bool:
        """
        Check if this piece can capture the target piece.
        
        Args:
            target_piece: The piece to potentially capture
            board: The game board
            
        Returns:
            True if capture is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """
        Get all valid moves for this piece.
        
        Args:
            board: The game board
            
        Returns:
            List of valid positions this piece can move to
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the piece."""
        return f"{self.__class__.__name__}(rank={self.rank}, owner={self.owner.color.value}, pos={self.position})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return self.__str__()



class StandardLandPiece(Piece):
    """
    Base class for standard land animal pieces.
    Standard pieces move one square horizontally or vertically,
    cannot enter water, and capture based on rank.
    """
    
    def can_move_to(self, board: 'Board', target: Position) -> bool:
        """
        Check if this piece can move to the target position.
        Standard pieces can move one square horizontally or vertically,
        but cannot move onto water or their own den.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Must be adjacent (one square horizontally or vertically)
        if not self.position.is_adjacent(target):
            return False
        
        # Cannot move to invalid positions
        if not board.is_valid_position(target):
            return False
        
        # Cannot move onto water
        if board.is_water(target):
            return False
        
        # Cannot move to own den
        if board.is_den(target, self.owner):
            return False
        
        # Check if target square is occupied by own piece
        target_piece = board.get_piece(target)
        if target_piece is not None and target_piece.owner == self.owner:
            return False
        
        return True
    
    def can_capture(self, target_piece: 'Piece', board: 'Board') -> bool:
        """
        Check if this piece can capture the target piece.
        Standard pieces can capture pieces of equal or lower rank.
        Pieces in enemy traps can be captured regardless of rank.
        
        Args:
            target_piece: The piece to potentially capture
            board: The game board
            
        Returns:
            True if capture is allowed, False otherwise
        """
        # Cannot capture own pieces
        if target_piece.owner == self.owner:
            return False
        
        # If target is in a trap that belongs to the attacker, can always capture
        # (enemy piece in my trap)
        if board.is_trap(target_piece.position, self.owner):
            return True
        
        # Standard rank-based capture: can capture equal or lower rank
        return self.rank >= target_piece.rank
    
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """
        Get all valid moves for this piece.
        
        Args:
            board: The game board
            
        Returns:
            List of valid positions this piece can move to
        """
        from model.enums import Direction
        valid_moves = []
        
        for direction in Direction:
            new_pos = self.position.move(direction)
            if board.is_valid_position(new_pos) and self.can_move_to(board, new_pos):
                valid_moves.append(new_pos)
        
        return valid_moves


class Cat(StandardLandPiece):
    """
    Cat piece - Rank 2.
    Standard land animal with normal movement and capture rules.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Cat piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=2, owner=owner, position=position)


class Dog(StandardLandPiece):
    """
    Dog piece - Rank 3.
    Standard land animal with normal movement and capture rules.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Dog piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=3, owner=owner, position=position)


class Wolf(StandardLandPiece):
    """
    Wolf piece - Rank 4.
    Standard land animal with normal movement and capture rules.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Wolf piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=4, owner=owner, position=position)


class Leopard(StandardLandPiece):
    """
    Leopard piece - Rank 5.
    Standard land animal with normal movement and capture rules.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Leopard piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=5, owner=owner, position=position)


class Elephant(StandardLandPiece):
    """
    Elephant piece - Rank 8 (highest).
    Standard land animal but cannot capture rats.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize an Elephant piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=8, owner=owner, position=position)
    
    def can_capture(self, target_piece: 'Piece', board: 'Board') -> bool:
        """
        Check if this piece can capture the target piece.
        Elephants cannot capture rats (special rule).
        
        Args:
            target_piece: The piece to potentially capture
            board: The game board
            
        Returns:
            True if capture is allowed, False otherwise
        """
        # Elephants cannot capture rats
        if target_piece.rank == 1:  # Rat has rank 1
            return False
        
        # Otherwise use standard capture rules
        return super().can_capture(target_piece, board)



class Rat(Piece):
    """
    Rat piece - Rank 1 (lowest).
    Special piece that can move in water and has unique capture rules.
    Can capture elephants but elephants cannot capture rats.
    Cannot capture rats across water/land boundaries.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Rat piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=1, owner=owner, position=position)
    
    def can_move_to(self, board: 'Board', target: Position) -> bool:
        """
        Check if this piece can move to the target position.
        Rats can move one square horizontally or vertically,
        including onto water squares (unique ability).
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Must be adjacent (one square horizontally or vertically)
        if not self.position.is_adjacent(target):
            return False
        
        # Cannot move to invalid positions
        if not board.is_valid_position(target):
            return False
        
        # Cannot move to own den
        if board.is_den(target, self.owner):
            return False
        
        # Check if target square is occupied by own piece
        target_piece = board.get_piece(target)
        if target_piece is not None and target_piece.owner == self.owner:
            return False
        
        # Rats CAN move onto water (unlike other pieces)
        return True
    
    def can_capture(self, target_piece: 'Piece', board: 'Board') -> bool:
        """
        Check if this piece can capture the target piece.
        Rats have special capture rules:
        - Can capture elephants (rank 8)
        - Can capture other rats only if both are in the same environment (both in water or both on land)
        - Cannot capture from water to land or vice versa
        - Standard rank-based capture for other pieces
        
        Args:
            target_piece: The piece to potentially capture
            board: The game board
            
        Returns:
            True if capture is allowed, False otherwise
        """
        # Cannot capture own pieces
        if target_piece.owner == self.owner:
            return False
        
        # If target is in attacker's trap, can always capture
        if board.is_trap(target_piece.position, self.owner):
            return True
        
        # Check if rat is in water
        rat_in_water = board.is_water(self.position)
        target_in_water = board.is_water(target_piece.position)
        
        # Special rule: Rat in water cannot capture pieces on land
        if rat_in_water and not target_in_water:
            return False
        
        # Special rule: Rat on land cannot capture pieces in water
        if not rat_in_water and target_in_water:
            return False
        
        # Rats can capture elephants (special rule)
        if target_piece.rank == 8:  # Elephant
            return True
        
        # Standard rank-based capture for other pieces
        return self.rank >= target_piece.rank
    
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """
        Get all valid moves for this piece.
        
        Args:
            board: The game board
            
        Returns:
            List of valid positions this piece can move to
        """
        from model.enums import Direction
        valid_moves = []
        
        for direction in Direction:
            new_pos = self.position.move(direction)
            if board.is_valid_position(new_pos) and self.can_move_to(board, new_pos):
                valid_moves.append(new_pos)
        
        return valid_moves



class Lion(StandardLandPiece):
    """
    Lion piece - Rank 7.
    Can jump over rivers horizontally or vertically if no rat blocks the path.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Lion piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=7, owner=owner, position=position)
    
    def can_jump_river(self, board: 'Board', target: Position) -> bool:
        """
        Check if the lion can jump over a river to reach the target position.
        Lions can jump horizontally or vertically over rivers (3 water squares),
        but only if no rat is blocking the path in the water.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the jump is valid, False otherwise
        """
        # Check if positions are in the same row or column
        if self.position.row != target.row and self.position.col != target.col:
            return False
        
        # Determine the direction and distance
        if self.position.row == target.row:
            # Horizontal jump
            col_diff = target.col - self.position.col
            if abs(col_diff) != 4:  # River is 3 squares wide, so jump is 4 squares
                return False
            
            # Check for rats in the water squares between
            direction = 1 if col_diff > 0 else -1
            for i in range(1, 4):  # Check the 3 water squares
                check_pos = Position(self.position.row, self.position.col + i * direction)
                if not board.is_water(check_pos):
                    return False  # Not jumping over water
                piece_in_water = board.get_piece(check_pos)
                if piece_in_water is not None and piece_in_water.rank == 1:  # Rat blocking
                    return False
        else:
            # Vertical jump
            row_diff = target.row - self.position.row
            if abs(row_diff) != 4:  # River is 3 rows tall, so jump is 4 rows
                return False
            
            # Check for rats in the water squares between
            direction = 1 if row_diff > 0 else -1
            for i in range(1, 4):  # Check the 3 water squares
                check_pos = Position(self.position.row + i * direction, self.position.col)
                if not board.is_water(check_pos):
                    return False  # Not jumping over water
                piece_in_water = board.get_piece(check_pos)
                if piece_in_water is not None and piece_in_water.rank == 1:  # Rat blocking
                    return False
        
        return True
    
    def can_move_to(self, board: 'Board', target: Position) -> bool:
        """
        Check if this piece can move to the target position.
        Lions can move normally or jump over rivers.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Try standard movement first
        if super().can_move_to(board, target):
            return True
        
        # Try river jumping
        if not board.is_valid_position(target):
            return False
        
        # Cannot jump to own den
        if board.is_den(target, self.owner):
            return False
        
        # Check if target is occupied by own piece
        target_piece = board.get_piece(target)
        if target_piece is not None and target_piece.owner == self.owner:
            return False
        
        # Check if can jump river
        return self.can_jump_river(board, target)
    
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """
        Get all valid moves for this piece, including river jumps.
        
        Args:
            board: The game board
            
        Returns:
            List of valid positions this piece can move to
        """
        from model.enums import Direction
        valid_moves = []
        
        # Add standard adjacent moves
        for direction in Direction:
            new_pos = self.position.move(direction)
            if board.is_valid_position(new_pos) and super().can_move_to(board, new_pos):
                valid_moves.append(new_pos)
        
        # Add river jump moves
        # Horizontal jumps (4 squares left/right)
        for col_offset in [-4, 4]:
            jump_pos = Position(self.position.row, self.position.col + col_offset)
            if board.is_valid_position(jump_pos) and self.can_move_to(board, jump_pos):
                valid_moves.append(jump_pos)
        
        # Vertical jumps (4 squares up/down)
        for row_offset in [-4, 4]:
            jump_pos = Position(self.position.row + row_offset, self.position.col)
            if board.is_valid_position(jump_pos) and self.can_move_to(board, jump_pos):
                valid_moves.append(jump_pos)
        
        return valid_moves


class Tiger(StandardLandPiece):
    """
    Tiger piece - Rank 6.
    Can jump over rivers horizontally or vertically if no rat blocks the path.
    """
    
    def __init__(self, owner: 'Player', position: Position):
        """
        Initialize a Tiger piece.
        
        Args:
            owner: The player who owns this piece
            position: Initial position on the board
        """
        super().__init__(rank=6, owner=owner, position=position)
    
    def can_jump_river(self, board: 'Board', target: Position) -> bool:
        """
        Check if the tiger can jump over a river to reach the target position.
        Tigers can jump horizontally or vertically over rivers (3 water squares),
        but only if no rat is blocking the path in the water.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the jump is valid, False otherwise
        """
        # Check if positions are in the same row or column
        if self.position.row != target.row and self.position.col != target.col:
            return False
        
        # Determine the direction and distance
        if self.position.row == target.row:
            # Horizontal jump
            col_diff = target.col - self.position.col
            if abs(col_diff) != 4:  # River is 3 squares wide, so jump is 4 squares
                return False
            
            # Check for rats in the water squares between
            direction = 1 if col_diff > 0 else -1
            for i in range(1, 4):  # Check the 3 water squares
                check_pos = Position(self.position.row, self.position.col + i * direction)
                if not board.is_water(check_pos):
                    return False  # Not jumping over water
                piece_in_water = board.get_piece(check_pos)
                if piece_in_water is not None and piece_in_water.rank == 1:  # Rat blocking
                    return False
        else:
            # Vertical jump
            row_diff = target.row - self.position.row
            if abs(row_diff) != 4:  # River is 3 rows tall, so jump is 4 rows
                return False
            
            # Check for rats in the water squares between
            direction = 1 if row_diff > 0 else -1
            for i in range(1, 4):  # Check the 3 water squares
                check_pos = Position(self.position.row + i * direction, self.position.col)
                if not board.is_water(check_pos):
                    return False  # Not jumping over water
                piece_in_water = board.get_piece(check_pos)
                if piece_in_water is not None and piece_in_water.rank == 1:  # Rat blocking
                    return False
        
        return True
    
    def can_move_to(self, board: 'Board', target: Position) -> bool:
        """
        Check if this piece can move to the target position.
        Tigers can move normally or jump over rivers.
        
        Args:
            board: The game board
            target: The target position
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Try standard movement first
        if super().can_move_to(board, target):
            return True
        
        # Try river jumping
        if not board.is_valid_position(target):
            return False
        
        # Cannot jump to own den
        if board.is_den(target, self.owner):
            return False
        
        # Check if target is occupied by own piece
        target_piece = board.get_piece(target)
        if target_piece is not None and target_piece.owner == self.owner:
            return False
        
        # Check if can jump river
        return self.can_jump_river(board, target)
    
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """
        Get all valid moves for this piece, including river jumps.
        
        Args:
            board: The game board
            
        Returns:
            List of valid positions this piece can move to
        """
        from model.enums import Direction
        valid_moves = []
        
        # Add standard adjacent moves
        for direction in Direction:
            new_pos = self.position.move(direction)
            if board.is_valid_position(new_pos) and super().can_move_to(board, new_pos):
                valid_moves.append(new_pos)
        
        # Add river jump moves
        # Horizontal jumps (4 squares left/right)
        for col_offset in [-4, 4]:
            jump_pos = Position(self.position.row, self.position.col + col_offset)
            if board.is_valid_position(jump_pos) and self.can_move_to(board, jump_pos):
                valid_moves.append(jump_pos)
        
        # Vertical jumps (4 squares up/down)
        for row_offset in [-4, 4]:
            jump_pos = Position(self.position.row + row_offset, self.position.col)
            if board.is_valid_position(jump_pos) and self.can_move_to(board, jump_pos):
                valid_moves.append(jump_pos)
        
        return valid_moves
