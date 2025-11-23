# Test Coverage Report - Jungle Game Model

**Date:** November 23, 2025  
**Project:** COMP3211 Software Engineering - Jungle Game  
**Test Framework:** pytest 8.3.4  
**Coverage Tool:** pytest-cov 7.0.0

---

## Summary

This report presents the line coverage achieved by the test suite for the Jungle Game model layer. All tests have been successfully executed with **100% pass rate** (481 tests passed, 0 failed).

### Overall Coverage Statistics

- **Total Statements:** 676
- **Statements Covered:** 626
- **Statements Missed:** 50
- **Overall Coverage:** **93%**

---

## Detailed Coverage by Module

### 1. `model/__init__.py`
- **Statements:** 2
- **Missed:** 0
- **Coverage:** **100%**

### 2. `model/board.py`
- **Statements:** 55
- **Missed:** 0
- **Coverage:** **100%**
- **Description:** Board management, terrain detection, piece placement

### 3. `model/enums.py`
- **Statements:** 25
- **Missed:** 0
- **Coverage:** **100%**
- **Description:** Game enumerations (PlayerColor, GameStatus, Direction, TerrainType)

### 4. `model/exceptions.py`
- **Statements:** 20
- **Missed:** 0
- **Coverage:** **100%**
- **Description:** Custom exception classes for game validation

### 5. `model/game.py`
- **Statements:** 160
- **Missed:** 2
- **Coverage:** **99%**
- **Description:** Core game logic, move validation, victory conditions
- **Notes:** Only 2 statements uncovered, representing edge cases

### 6. `model/game_state.py`
- **Statements:** 43
- **Missed:** 1
- **Coverage:** **98%**
- **Description:** Game state capture and restoration for undo functionality

### 7. `model/move.py`
- **Statements:** 55
- **Missed:** 17
- **Coverage:** **69%**
- **Description:** Move representation and serialization
- **Notes:** Some serialization/parsing methods have lower coverage

### 8. `model/piece.py`
- **Statements:** 231
- **Missed:** 27
- **Coverage:** **88%**
- **Description:** Piece classes (Rat, Cat, Dog, Wolf, Leopard, Tiger, Lion, Elephant)
- **Notes:** Complex piece movement logic with special cases

### 9. `model/player.py`
- **Statements:** 43
- **Missed:** 1
- **Coverage:** **98%**
- **Description:** Player management and piece tracking

### 10. `model/position.py`
- **Statements:** 42
- **Missed:** 2
- **Coverage:** **95%**

## Test Suite Statistics

### Test Distribution

| Test Module | Test Count | Status |
|------------|-----------|--------|
| test_board.py | 23 | ✅ All Passed |
| test_board_renderer.py | 12 | ✅ All Passed |
| test_command_parser.py | 33 | ✅ All Passed |
| test_enums.py | 6 | ✅ All Passed |
| test_error_handling.py | 23 | ✅ All Passed |
| test_exceptions.py | 12 | ✅ All Passed |
| test_file_manager.py | 28 | ✅ All Passed |
| test_game.py | 77 | ✅ All Passed |
| test_game_controller.py | 34 | ✅ All Passed |
| test_game_state.py | 13 | ✅ All Passed |
| test_game_view.py | 19 | ✅ All Passed |
| test_integration.py | 6 | ✅ All Passed |
| test_main.py | 16 | ✅ All Passed |
| test_message_display.py | 28 | ✅ All Passed |
| test_move.py | 15 | ✅ All Passed |
| test_name_manager.py | 28 | ✅ All Passed |
| test_piece.py | 61 | ✅ All Passed |
| test_player.py | 21 | ✅ All Passed |
| test_position.py | 19 | ✅ All Passed |

---
### Test Categories Covered

- ✅ **Unit Tests**: Individual component testing
- ✅ **Integration Tests**: Component interaction testing
- ✅ **Error Handling Tests**: Exception and validation testing
- ✅ **Edge Case Tests**: Boundary condition testing
- ✅ **State Management Tests**: Undo/redo functionality
