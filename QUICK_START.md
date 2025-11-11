# Jungle Game - Quick Start Guide

## For Players

### Installation
```bash
# No installation needed - uses Python standard library only
python main.py
```

### Basic Commands
```
move a0 b0    # Move piece from a0 to b0
undo          # Undo last move (up to 3)
save game.jungle    # Save game
load game.jungle    # Load game
record game.record  # Save move history
quit          # Exit game
help          # Show all commands
```

### Move Formats
```
a0 b0         # Chess notation
0,0 1,0       # Coordinate notation
(0,0) (1,0)   # Parentheses notation
move from a0 to b0  # Verbose
```

## For Developers

### Project Structure
```
model/        # Game logic (no dependencies on view/controller)
view/         # Display and rendering
controller/   # Input handling and coordination
utils/        # Logging and utilities
tests/        # Test suite (491 tests)
```

### Running Tests
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_game.py -v

# With coverage
python -m pytest tests/ --cov=model --cov=controller --cov=view
```

### Debugging
```bash
# Enable debug logging
python main.py --debug

# View logs
tail -f logs/jungle_game_*.log

# Search logs
grep "ERROR" logs/*.log
```

### Adding Logging
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Message")
logger.debug("Debug info")
logger.error("Error", exc_info=True)
```

### Key Classes

**Game (model/game.py)**
```python
game = Game("Player 1", "Player 2")
result = game.make_move(from_pos, to_pos)
game.undo_move()
winner = game.get_winner()
```

**Board (model/board.py)**
```python
piece = board.get_piece(position)
board.set_piece(position, piece)
is_water = board.is_water(position)
```

**Piece (model/piece.py)**
```python
can_move = piece.can_move_to(board, target)
can_capture = piece.can_capture(target_piece, board)
valid_moves = piece.get_valid_moves(board)
```

### Adding a New Piece
1. Create class in `model/piece.py` inheriting from `Piece`
2. Implement `can_move_to()`, `can_capture()`, `get_valid_moves()`
3. Add symbol to `BoardRenderer.PIECE_SYMBOLS`
4. Update `Game._initialize_pieces()`
5. Write tests in `tests/test_piece.py`

### Adding a New Command
1. Add handler method in `GameController`
2. Add routing in `process_command()`
3. Update help message
4. Write tests

### Code Style
- Follow PEP 8
- Use type hints for all functions
- Add docstrings to all classes/methods
- Maximum line length: 100 characters
- Use `get_logger(__name__)` for logging

### Documentation
- **DEVELOPER_GUIDE.md** - Complete developer guide (7,500+ words)
- **API_REFERENCE.md** - API documentation (5,000+ words)
- **DOCUMENTATION_SUMMARY.md** - Task 14 completion summary

### Common Tasks

**Run game:**
```bash
python main.py
```

**Run with debug logging:**
```bash
python main.py --debug
```

**Load saved game:**
```bash
python main.py --load mygame.jungle
```

**Replay game:**
```bash
python main.py --replay mygame.record
```

**Run tests:**
```bash
python -m pytest tests/ -v
```

**Check code:**
```bash
# Type checking (if mypy installed)
mypy model/ controller/ view/

# Linting (if pylint installed)
pylint model/ controller/ view/
```

### Architecture Pattern

```
User Input → Controller → Model → Controller → View → Display
                ↓           ↓
            Commands    Game Logic
                ↓           ↓
            Parsing     Rules
                        State
```

### MVC Separation
- **Model**: Pure game logic, no I/O, independently testable
- **View**: Display only, no game logic
- **Controller**: Coordinates model and view, handles I/O

### Testing Pattern
```python
import unittest
from model.game import Game
from model.position import Position

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        self.game = Game("P1", "P2")
    
    def test_something(self):
        result = self.game.make_move(
            Position(8, 0),
            Position(7, 0)
        )
        self.assertTrue(result.success)
```

### Logging Levels
- **DEBUG**: Detailed diagnostic info
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

### File Formats

**.jungle (JSON):**
```json
{
  "version": "1.0",
  "players": [...],
  "board_state": {...},
  "move_history": [...]
}
```

**.record (Text):**
```
JUNGLE_GAME_RECORD_V1.0
Players: Player 1 (Red), Player 2 (Blue)
Move 1: Player 1 - Rat from (8,0) to (7,0)
...
```

### Getting Help

1. Check `DEVELOPER_GUIDE.md` for detailed information
2. Check `API_REFERENCE.md` for API documentation
3. Enable debug logging: `python main.py --debug`
4. Check log files in `logs/` directory
5. Run tests to verify behavior
6. Check docstrings in source code

### Useful Commands

```bash
# Find all TODOs
grep -r "TODO" model/ controller/ view/

# Count lines of code
find . -name "*.py" -not -path "./tests/*" | xargs wc -l

# Generate documentation (if pydoc installed)
python -m pydoc -w model controller view utils

# Profile performance
python -m cProfile -o profile.stats main.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

### Resources

- **Python Docs**: https://docs.python.org/3/
- **Type Hints**: https://docs.python.org/3/library/typing.html
- **Pytest**: https://docs.pytest.org/
- **PEP 8**: https://pep8.org/

---

**Quick Start Version:** 1.0  
**Last Updated:** November 11, 2025  
**For More Details:** See DEVELOPER_GUIDE.md and API_REFERENCE.md
