# Requirements Document

## Introduction

The Jungle Game is a strategic board game implementation that simulates the traditional Chinese board game "Dou Shou Qi" (Fighting Animals). The game features an 7x9 board with special terrain areas, eight different animal pieces per player with unique movement and capture rules, and various game management features including save/load functionality and move history. The implementation must be developed in Python using object-oriented design principles with a clear separation between the game model and other components.

## Requirements

### Requirement 1

**User Story:** As a player, I want to start a new game so that I can begin playing the Jungle Game with proper initial setup.

#### Acceptance Criteria

1. WHEN a player initiates a new game THEN the system SHALL create a 7x9 board with proper terrain setup
2. WHEN a new game starts THEN the system SHALL place all 16 pieces (8 per player) in their initial positions according to the animal pictures on the board
3. WHEN a new game is created THEN the system SHALL set the first player as the active player
4. WHEN a new game starts THEN the system SHALL initialize empty move history and game state

### Requirement 2

**User Story:** As a player, I want to end an ongoing game so that I can terminate the current session when needed.

#### Acceptance Criteria

1. WHEN a player requests to end the game THEN the system SHALL terminate the current game session
2. WHEN the game is ended THEN the system SHALL clean up the current game state
3. WHEN the game ends THEN the system SHALL return to the main menu or exit the application

### Requirement 3

**User Story:** As a player, I want to name the players with input or randomly generated strings so that I can better differentiate the players during gameplay.

#### Acceptance Criteria

1. WHEN setting up a new game THEN the system SHALL allow players to input custom names
2. WHEN no custom names are provided THEN the system SHALL generate random player names
3. WHEN player names are set THEN the system SHALL use these names throughout the game display
4. WHEN displaying game status THEN the system SHALL clearly indicate which named player's turn it is

### Requirement 4

**User Story:** As a player, I want to play the game via the command line console so that I can interact with the game through text-based commands.

#### Acceptance Criteria

1. WHEN the game runs THEN the system SHALL provide a command-line interface
2. WHEN a player enters a move command THEN the system SHALL parse and validate the input
3. WHEN invalid input is provided THEN the system SHALL display appropriate error messages
4. WHEN valid commands are entered THEN the system SHALL execute the corresponding game actions

### Requirement 5

**User Story:** As a player, I want to see the status of the game, including all remaining pieces and their positions on the board, as well as the next player to make a move, so that I can make informed decisions.

#### Acceptance Criteria

1. WHEN displaying game status THEN the system SHALL show the current board state with all pieces
2. WHEN showing the board THEN the system SHALL clearly indicate piece types and ownership
3. WHEN displaying status THEN the system SHALL show which player's turn it is
4. WHEN showing game state THEN the system SHALL indicate special board areas (dens, traps, rivers)
5. WHEN displaying pieces THEN the system SHALL show the rank and type of each animal

### Requirement 6

**User Story:** As a player, I want to take back at most 3 moves in each game so that I can undo recent mistakes.

#### Acceptance Criteria

1. WHEN a player requests an undo THEN the system SHALL revert the last move if available
2. WHEN tracking undo history THEN the system SHALL maintain at most 3 previous game states
3. WHEN no moves are available to undo THEN the system SHALL inform the player
4. WHEN undoing a move THEN the system SHALL restore the previous board state and switch the active player

### Requirement 7

**User Story:** As a player, I want to record all information about a game, including the players and their moves, into a file with extension ".record" so that I can review the game later.

#### Acceptance Criteria

1. WHEN a game is played THEN the system SHALL record all moves in chronological order
2. WHEN recording moves THEN the system SHALL include player names, piece types, source and destination positions
3. WHEN saving a record THEN the system SHALL write the data to a file with ".record" extension
4. WHEN creating a record file THEN the system SHALL include game metadata (players, start time, game outcome)

### Requirement 8

**User Story:** As a player, I want to use the record from a file with extension ".record" to replay a game so that I can review past games step by step.

#### Acceptance Criteria

1. WHEN loading a record file THEN the system SHALL parse and validate the file format
2. WHEN replaying a game THEN the system SHALL recreate each move in the original sequence
3. WHEN replaying THEN the system SHALL allow stepping through moves at the player's pace
4. WHEN replay is complete THEN the system SHALL show the final game state

### Requirement 9

**User Story:** As a player, I want to save the current game to a file with extension ".jungle" so that I can continue playing later.

#### Acceptance Criteria

1. WHEN saving a game THEN the system SHALL serialize the complete current game state
2. WHEN creating a save file THEN the system SHALL use the ".jungle" file extension
3. WHEN saving THEN the system SHALL include board state, player information, and move history
4. WHEN save is successful THEN the system SHALL confirm the save operation to the player

### Requirement 10

**User Story:** As a player, I want to load a game from a file with extension ".jungle" and continue playing so that I can resume interrupted games.

#### Acceptance Criteria

1. WHEN loading a saved game THEN the system SHALL restore the complete game state from the file
2. WHEN loading is successful THEN the system SHALL resume gameplay from the saved position
3. WHEN loading fails THEN the system SHALL display appropriate error messages
4. WHEN a game is loaded THEN the system SHALL maintain all game rules and constraints

### Requirement 11

**User Story:** As a player, I want pieces to move according to the jungle game rules so that the game follows traditional gameplay mechanics.

#### Acceptance Criteria

1. WHEN a piece moves THEN the system SHALL validate the move is one square horizontally or vertically
2. WHEN a piece attempts to move THEN the system SHALL prevent movement to the player's own den
3. WHEN the rat moves THEN the system SHALL allow movement onto water squares
4. WHEN other animals move THEN the system SHALL prevent movement onto water squares
5. WHEN lion or tiger moves THEN the system SHALL allow jumping over rivers if no rat blocks the path
6. WHEN any piece moves THEN the system SHALL prevent diagonal movement

### Requirement 12

**User Story:** As a player, I want pieces to capture according to rank and special rules so that combat follows the traditional jungle game mechanics.

#### Acceptance Criteria

1. WHEN a piece captures THEN the system SHALL allow capture of equal or lower ranked pieces
2. WHEN a rat encounters an elephant THEN the system SHALL allow the rat to capture the elephant
3. WHEN an elephant encounters a rat THEN the system SHALL prevent the elephant from capturing the rat
4. WHEN a piece is in a trap THEN the system SHALL allow any enemy piece to capture it regardless of rank
5. WHEN a rat is in water THEN the system SHALL prevent it from capturing elephants or rats on land
6. WHEN both rats are in the same environment THEN the system SHALL allow normal capture rules

### Requirement 13

**User Story:** As a player, I want the game to end when victory conditions are met so that games conclude properly.

#### Acceptance Criteria

1. WHEN a piece reaches the opponent's den THEN the system SHALL declare the moving player as winner
2. WHEN all opponent pieces are captured THEN the system SHALL declare the capturing player as winner
3. WHEN victory is achieved THEN the system SHALL display the game result
4. WHEN the game ends THEN the system SHALL prevent further moves

### Requirement 14

**User Story:** As a developer, I want the game model separated into a distinct package so that the code follows MVC architecture and supports unit testing.

#### Acceptance Criteria

1. WHEN organizing code THEN the system SHALL place all game logic in a "model" package
2. WHEN implementing architecture THEN the system SHALL separate model, view, and controller components
3. WHEN designing classes THEN the system SHALL use object-oriented principles for better maintainability
4. WHEN structuring code THEN the system SHALL ensure the model is independently testable