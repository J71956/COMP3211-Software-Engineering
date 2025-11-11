# Jungle Game - API Reference

## Table of Contents

1. [Model Package](#model-package)
2. [View Package](#view-package)
3. [Controller Package](#controller-package)
4. [Utils Package](#utils-package)

---

## Model Package

### game.py

#### `class Game`

Central game state manager and rule enforcer.

**Constructor:**
```python
Game(player1_name: str = "Player 1", player2_name: str = "Player 2")
```

**Properties:**
- `board: Board` - The game board
- `players: List[Player]` - List of players (read-only copy)
- `current_player_index: int` - Index of current player (0 or 1)
- `move_history: List[Move]` - History of all moves (read-only copy)
- `game_status: GameStatus` - Current game status

**Methods:**

`make_move(from_pos: Position, to_pos: Position) -> MoveResult`
- Execute a move from one position to another
- Validates move, handles captures, updates game state
- Returns: MoveResult with success status and message
- Raises: Various exceptions for invalid moves

`undo_move() -> bool`
- Undo the last move and restore previous state
- Returns: True if successful, False if no moves to undo
- Raises: GameOverException if game is over

`is_game_over() -> bool`
- Check if the game has ended
- Returns: True if game is over, False otherwise

`get_winner() -> Optional[Player]`
- Get the winning player
- Returns: Player object or None if no winner

`get_current_player() -> Player`
- Get the player whose turn it is
- Returns: Current Player object

`can_undo() -> bool`
- Check if undo is available
- Returns: True if moves can be undone

---

### board.py

#### `class Board`

7x9 game board with terrain and piece management.

**Class Attributes:**
- `BOARD_HEIGHT = 9` - Number of rows
- `BOARD_WIDTH = 7` - Number of columns

**Methods:**

`get_piece(pos: Position) -> Optional[Piece]`
- Get the piece at a position
- Returns: Piece object or None if empty

`set_piece(pos: Position, piece: Optional[Piece]) -> None`
- Place or remove a piece at a position

`is_valid_position(pos: Position) -> bool`
- Check if position is within board bounds
- Returns: True if valid, False otherwise

`get_terrain(pos: Position) -> TerrainType`
- Get terrain type at position
- Returns: TerrainType enum value

`is_den(pos: Position, player: Optional[Player] = None) -> bool`
- Check if position is a den
- If player specified, checks if it's that player's den

`is_trap(pos: Position, player: Optional[Player] = None) -> bool`
- Check if position is a trap
- If player specified, checks if it's that player's trap

`is_water(pos: Position) -> bool`
- Check if position is water
- Returns: True if water, False otherwise

---

### piece.py

#### `class Piece` (Abstract Base Class)

Base class for all game pieces.

**Constructor:**
```python
Piece(rank: int, owner: Player, position: Position)
```

**Properties:**
- `rank: int` - Piece rank (1-8)
- `owner: Player` - Owning player
- `position: Position` - Current position

**Abstract Methods:**

`can_move_to(board: Board, target: Position) -> bool`
- Check if piece can move to target position
- Must be implemented by subclasses

`can_capture(target_piece: Piece, board: Board) -> bool`
- Check if piece can capture target piece
- Must be implemented by subclasses

`get_valid_moves(board: Board) -> List[Position]`
- Get all valid moves for this piece
- Must be implemented by subclasses

#### Concrete Piece Classes

All inherit from `Piece` and implement the abstract methods:

- `Rat(owner, position)` - Rank 1, can move in water
- `Cat(owner, position)` - Rank 2, standard land piece
- `Dog(owner, position)` - Rank 3, standard land piece
- `Wolf(owner, position)` - Rank 4, standard land piece
- `Leopard(owner, position)` - Rank 5, standard land piece
- `Tiger(owner, position)` - Rank 6, can jump rivers
- `Lion(owner, position)` - Rank 7, can jump rivers
- `Elephant(owner, position)` - Rank 8, cannot capture rats

---

### player.py

#### `class Player`

Represents a player in the game.

**Constructor:**
```python
Player(name: str, color: PlayerColor)
```

**Properties:**
- `name: str` - Player's name
- `color: PlayerColor` - Player's color (RED or BLUE)
- `pieces: Set[Piece]` - Set of owned pieces (read-only copy)

**Methods:**

`add_piece(piece: Piece) -> None`
- Add a piece to player's collection

`remove_piece(piece: Piece) -> None`
- Remove a piece from player's collection

`get_active_pieces() -> List[Piece]`
- Get list of all active pieces
- Returns: List of Piece objects

`has_pieces() -> bool`
- Check if player has any pieces remaining
- Returns: True if pieces exist, False otherwise

`get_den_position() -> Position`
- Get position of player's den
- Returns: Position object

`get_trap_positions() -> List[Position]`
- Get positions of player's traps
- Returns: List of Position objects

---

### position.py

#### `class Position`

Immutable position on the game board.

**Constructor:**
```python
Position(row: int, col: int)
```

**Properties:**
- `row: int` - Row index (0-8)
- `col: int` - Column index (0-6)

**Methods:**

`is_adjacent(other: Position) -> bool`
- Check if another position is adjacent
- Returns: True if adjacent horizontally or vertically

`get_direction(other: Position) -> Optional[Direction]`
- Get direction to another adjacent position
- Returns: Direction enum or None

`move(direction: Direction) -> Position`
- Create new position by moving in a direction
- Returns: New Position object

---

### move.py

#### `class Move` (dataclass)

Immutable move record with timestamp.

**Attributes:**
- `piece: Piece` - The piece that moved
- `from_pos: Position` - Starting position
- `to_pos: Position` - Destination position
- `captured_piece: Optional[Piece]` - Captured piece if any
- `timestamp: datetime` - When move was made

**Methods:**

`to_dict() -> Dict[str, Any]`
- Serialize move to dictionary
- Returns: Dictionary representation

`from_dict(data: Dict[str, Any], game: Game) -> Move` (static)
- Deserialize move from dictionary
- Returns: Move object

`to_record_string() -> str`
- Convert to human-readable string
- Returns: Formatted string for .record files

`parse_record_string(record_str: str) -> Dict[str, Any]` (static)
- Parse move from record string
- Returns: Dictionary with move data

#### `class MoveResult` (dataclass)

Result of a move operation.

**Attributes:**
- `success: bool` - Whether move succeeded
- `message: str` - Descriptive message
- `captured_piece: Optional[Piece]` - Captured piece if any

---

### enums.py

#### Enumerations

`TerrainType(Enum)`
- `LAND` - Normal land square
- `WATER` - Water square (river)
- `DEN` - Den square
- `TRAP` - Trap square

`PlayerColor(Enum)`
- `RED` - Red player
- `BLUE` - Blue player

`GameStatus(Enum)`
- `ONGOING` - Game in progress
- `PLAYER_ONE_WINS` - Player 1 won
- `PLAYER_TWO_WINS` - Player 2 won
- `DRAW` - Game ended in draw

`Direction(Enum)`
- `NORTH` - Up (-1, 0)
- `SOUTH` - Down (1, 0)
- `EAST` - Right (0, 1)
- `WEST` - Left (0, -1)

**Properties:**
- `row_delta: int` - Row change for direction
- `col_delta: int` - Column change for direction

---

### exceptions.py

#### Exception Hierarchy

All exceptions inherit from `JungleGameException`:

- `JungleGameException` - Base exception
- `InvalidMoveException` - Move violates rules
- `InvalidPositionException` - Position out of bounds
- `GameOverException` - Action after game ended
- `FileOperationException` - File operation failed
- `InvalidInputException` - Invalid user input
- `PieceNotFoundException` - No piece at position
- `WrongPlayerException` - Wrong player's piece
- `InvalidCaptureException` - Invalid capture attempt
- `ValidationException` - Data validation failed

---

## View Package

### game_view.py

#### `class GameView`

Main view coordinator for displaying game state.

**Constructor:**
```python
GameView()
```

**Attributes:**
- `board_renderer: BoardRenderer` - Board renderer instance

**Methods:**

`display_game_state(game: Game) -> str`
- Display complete game state
- Returns: Formatted string

`display_welcome_message() -> str`
- Display welcome message
- Returns: Formatted string

`display_game_over(game: Game) -> str`
- Display game over message
- Returns: Formatted string

`display_move_result(result: MoveResult) -> str`
- Display move result
- Returns: Formatted string

`display_error(message: str) -> str`
- Display error message
- Returns: Formatted string

`display_info(message: str) -> str`
- Display informational message
- Returns: Formatted string

`display_undo_result(success: bool) -> str`
- Display undo result
- Returns: Formatted string

---

### board_renderer.py

#### `class BoardRenderer`

Renders the board as ASCII art.

**Class Attributes:**
- `PIECE_SYMBOLS: Dict[str, str]` - Piece type to symbol mapping

**Methods:**

`render_board(board: Board) -> str`
- Render complete board
- Returns: ASCII art string

`render_piece(piece: Optional[Piece]) -> str`
- Render single piece as symbol
- Returns: Single character

`render_terrain_markers() -> str`
- Render legend for terrain and pieces
- Returns: Formatted legend string

---

### message_display.py

#### `class MessageDisplay`

Handles user communication through formatted messages.

**Methods:**

`show_error(message: str) -> str`
- Format error message

`show_info(message: str) -> str`
- Format informational message

`show_warning(message: str) -> str`
- Format warning message

`show_success(message: str) -> str`
- Format success message

`show_failure(message: str) -> str`
- Format failure message

`prompt_for_input(prompt: str) -> str`
- Format input prompt

`confirm_action(action: str) -> str`
- Format confirmation prompt

`show_validation_error(field: str, reason: str) -> str`
- Format validation error

`show_file_error(filename: str, operation: str, reason: str) -> str`
- Format file operation error

`show_file_success(filename: str, operation: str) -> str`
- Format file operation success

---

## Controller Package

### game_controller.py

#### `class GameController`

Main game controller and command processor.

**Constructor:**
```python
GameController(game: Optional[Game] = None)
```

**Attributes:**
- `game: Optional[Game]` - Current game instance
- `view: GameView` - Game view
- `command_parser: CommandParser` - Command parser
- `file_manager: FileManager` - File manager
- `running: bool` - Game loop status

**Methods:**

`run_game_loop() -> None`
- Run the main game loop
- Handles display, input, and command processing

`process_command(command: str) -> bool`
- Process a user command
- Returns: True if successful, False otherwise

---

### command_parser.py

#### `class CommandParser`

Parses and validates user input commands.

**Class Attributes:**
- `BOARD_ROWS = 9` - Number of rows
- `BOARD_COLS = 7` - Number of columns

**Static Methods:**

`parse_move_command(input_str: str) -> Tuple[Position, Position]`
- Parse move command into positions
- Supports multiple formats (chess notation, coordinates)
- Returns: Tuple of (from_position, to_position)
- Raises: InvalidInputException, InvalidPositionException

`parse_position(row: int, col: int) -> Position`
- Create and validate Position
- Returns: Position object
- Raises: InvalidPositionException

`is_valid_position(row: int, col: int) -> bool`
- Check if position is valid
- Returns: True if valid, False otherwise

`validate_command_format(command: str) -> bool`
- Validate command format
- Returns: True if valid, False otherwise

`format_position(position: Position) -> str`
- Format position as string
- Returns: Formatted string (e.g., "a0")

---

### file_manager.py

#### `class FileManager`

Handles file operations for save/load and records.

**Class Attributes:**
- `JUNGLE_VERSION = "1.0"` - Save file version
- `RECORD_VERSION = "1.0"` - Record file version

**Static Methods:**

`save_game(game: Game, filename: str) -> bool`
- Save game to .jungle file
- Returns: True if successful
- Raises: FileOperationException

`load_game(filename: str) -> Optional[Game]`
- Load game from .jungle file
- Returns: Game object or None
- Raises: FileOperationException

`save_record(game: Game, filename: str) -> bool`
- Save game record to .record file
- Returns: True if successful
- Raises: FileOperationException

`load_record(filename: str) -> Optional[List[Dict[str, Any]]]`
- Load moves from .record file
- Returns: List of move dictionaries or None
- Raises: FileOperationException

`replay_record(filename: str, player1_name: str = None, player2_name: str = None) -> Optional[Game]`
- Replay game from .record file
- Returns: Game object with moves replayed or None
- Raises: FileOperationException

---

### name_manager.py

#### `class NameManager`

Manages player name input and generation.

**Class Attributes:**
- `ADJECTIVES: List[str]` - Adjectives for random names
- `ANIMALS: List[str]` - Animals for random names

**Static Methods:**

`validate_name(name: str) -> bool`
- Validate player name
- Returns: True if valid, False otherwise

`generate_random_name() -> str`
- Generate random player name
- Returns: Random name string

`get_player_name(prompt: str, default_name: Optional[str] = None) -> str`
- Get player name from input or generate random
- Returns: Valid player name

`get_player_names() -> Tuple[str, str]`
- Get names for both players
- Returns: Tuple of (player1_name, player2_name)

---

## Utils Package

### logger.py

#### `class GameLogger`

Centralized logging configuration.

**Class Attributes:**
- `DEFAULT_FORMAT: str` - Default log format
- `DETAILED_FORMAT: str` - Detailed log format with file/line
- `LOG_DIR: Path` - Log directory path

**Class Methods:**

`initialize(level: int = logging.INFO, log_to_file: bool = True, log_to_console: bool = True, detailed: bool = False) -> None`
- Initialize logging system
- Sets up handlers and formatters

`get_logger(name: str) -> logging.Logger`
- Get logger instance for module
- Returns: Logger object

`set_level(level: int) -> None`
- Change logging level for all handlers

`get_log_file() -> Optional[Path]`
- Get current log file path
- Returns: Path object or None

`cleanup_old_logs(keep_days: int = 7) -> int`
- Clean up old log files
- Returns: Number of files deleted

**Module Function:**

`get_logger(name: str) -> logging.Logger`
- Convenience function to get logger
- Returns: Logger object

**Usage Example:**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Information message")
logger.debug("Debug message")
logger.error("Error message", exc_info=True)
```

---

## Command-Line Interface

### main.py

**Command-Line Arguments:**

```
python main.py [options]

Options:
  --load FILE, -l FILE      Load saved game from .jungle file
  --replay FILE, -r FILE    Replay game from .record file
  --player1 NAME            Name for player 1 (Red)
  --player2 NAME            Name for player 2 (Blue)
  --debug                   Enable debug logging
  --log-file                Enable file logging (default)
  --no-log-file             Disable file logging
  --version, -v             Show version
  --help, -h                Show help message
```

**Examples:**
```bash
# Start new game
python main.py

# Load saved game
python main.py --load mygame.jungle

# Replay game record
python main.py --replay mygame.record

# Enable debug logging
python main.py --debug

# Set player names
python main.py --player1 "Alice" --player2 "Bob"
```

---

## File Formats

### .jungle File Format (JSON)

```json
{
  "version": "1.0",
  "players": [
    {"name": "Player 1", "color": "red"},
    {"name": "Player 2", "color": "blue"}
  ],
  "current_player": 0,
  "board_state": {
    "0,0": {"piece": "Elephant", "owner": "blue", "rank": 8},
    "8,6": {"piece": "Elephant", "owner": "red", "rank": 8}
  },
  "move_history": [
    {
      "piece_type": "Rat",
      "piece_rank": 1,
      "owner_color": "red",
      "from_row": 8,
      "from_col": 0,
      "to_row": 7,
      "to_col": 0,
      "captured_piece_type": null,
      "captured_piece_rank": null,
      "timestamp": "2024-01-01T10:00:00"
    }
  ],
  "game_status": "ongoing"
}
```

### .record File Format (Text)

```
JUNGLE_GAME_RECORD_V1.0
Players: Player 1 (Red), Player 2 (Blue)
Start Time: 2024-01-01 10:00:00
Move 1: Player 1 - Rat from (8,0) to (7,0)
Move 2: Player 2 - Cat from (1,1) to (2,1)
Move 3: Player 1 - Dog from (7,1) to (6,1) (captured Cat)
Game Result: Player 1 Wins
End Time: 2024-01-01 10:15:30
```

---

## Type Hints Reference

The codebase uses comprehensive type hints. Common patterns:

```python
from typing import Optional, List, Dict, Tuple, Set, Any, TYPE_CHECKING

# Optional values
def get_piece(pos: Position) -> Optional[Piece]:
    pass

# Collections
def get_valid_moves(board: Board) -> List[Position]:
    pass

# Multiple return values
def parse_command(cmd: str) -> Tuple[Position, Position]:
    pass

# Forward references (avoid circular imports)
if TYPE_CHECKING:
    from model.board import Board
```

---

## Error Handling Patterns

### Raising Exceptions

```python
if not self.is_valid_position(pos):
    raise InvalidPositionException(
        f"Position {pos} is out of bounds"
    )
```

### Catching Exceptions

```python
try:
    result = game.make_move(from_pos, to_pos)
except InvalidMoveException as e:
    logger.error(f"Invalid move: {e}")
    print(f"Error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

---

## Logging Patterns

### Module-Level Logger

```python
from utils.logger import get_logger

logger = get_logger(__name__)
```

### Logging Levels

```python
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical error")
```

### Logging with Context

```python
logger.info(f"Player {player.name} made move: {from_pos} -> {to_pos}")
logger.debug(f"Board state: {len(pieces)} pieces remaining")
```

---

This API reference provides a comprehensive overview of all public interfaces in the Jungle Game codebase. For implementation details and examples, refer to the [Developer Guide](DEVELOPER_GUIDE.md).
