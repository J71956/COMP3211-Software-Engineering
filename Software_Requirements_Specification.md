# Software Requirements Specification
## Jungle Game (Dou Shou Qi) Implementation

**Document Version:** 1.0  
**Date:** November 23, 2025  
**Project:** COMP3211 Software Engineering - Jungle Game Implementation

---

## Preface

### Expected Readership

This Software Requirements Specification (SRS) document is intended for:

- **Software Developers**: Primary implementers of the Jungle Game system
- **Project Stakeholders**: Course instructors and academic evaluators
- **Quality Assurance Teams**: Testers responsible for validation and verification
- **System Architects**: Technical leads overseeing the system design
- **Students**: Team members involved in the software engineering project

### Version History

| Version | Date | Author | Changes | Rationale |
|---------|------|--------|---------|-----------|
| 1.0 | November 23, 2025 | Development Team | Initial SRS creation | Establish comprehensive requirements documentation for COMP3211 project implementation |

### Document Purpose

This document serves as the authoritative specification for the Jungle Game implementation, providing detailed functional and non-functional requirements, system architecture overview, and interface specifications. It establishes the foundation for design, implementation, and testing phases of the software development lifecycle.

---

## Introduction

### System Overview

The Jungle Game system is a digital implementation of the traditional Chinese board game "Dou Shou Qi" (Fighting Animals), designed as a command-line application for educational purposes in software engineering. The system provides a complete gaming experience with strategic gameplay, file management capabilities, and comprehensive game state management.

### Business Context

This software system is developed as part of the COMP3211 Software Engineering course project, demonstrating practical application of software engineering principles including:

- Object-oriented design and implementation
- Model-View-Controller (MVC) architectural pattern
- Comprehensive testing strategies
- Documentation and specification practices
- Version control and collaborative development

### System Functions

The Jungle Game system provides the following core functions:

1. **Game Management**: Initialize, play, and terminate game sessions
2. **Move Processing**: Validate and execute player moves according to game rules
3. **State Persistence**: Save and load game states for session continuity
4. **Game Recording**: Create and replay complete game histories
5. **Player Management**: Handle player identification and turn management
6. **Rule Enforcement**: Implement traditional Jungle Game mechanics and victory conditions

### System Integration

The Jungle Game operates as a standalone command-line application with the following external interactions:

- **File System**: Read/write operations for game saves and records
- **Operating System**: Command-line interface integration
- **Python Runtime**: Execution environment dependency

### Strategic Objectives

The system supports the following educational and technical objectives:

- Demonstrate proficiency in Python programming and object-oriented design
- Implement comprehensive software testing practices
- Apply software engineering methodologies in a practical context
- Create maintainable and extensible software architecture
- Develop skills in requirements analysis and system specification

---

## Glossary

### Game-Specific Terms

- **Animal Piece**: Game pieces representing different animals with unique ranks and abilities
- **Board**: 7x9 grid playing surface with special terrain areas
- **Capture**: Action of removing an opponent's piece by moving onto its position
- **Den**: Special board positions that serve as each player's home base
- **Dou Shou Qi**: Traditional Chinese name for the Jungle Game
- **Jungle Game**: The strategic board game being implemented
- **Move**: Transfer of a piece from one board position to another
- **Rank**: Numerical value (1-8) determining piece capture relationships
- **River**: Water terrain that affects piece movement
- **Trap**: Special positions adjacent to dens that weaken pieces
- **Turn**: One player's opportunity to make a move

### Technical Terms

- **Command Parser**: Component responsible for interpreting user input
- **Controller**: MVC component managing user interaction and system coordination
- **File Manager**: Component handling save/load and record operations
- **Game State**: Complete snapshot of game condition at a specific moment
- **Model**: MVC component containing game logic and data structures
- **MVC**: Model-View-Controller architectural pattern
- **Position**: Coordinate pair (row, column) identifying board locations
- **Serialization**: Process of converting game state to storable format
- **System**: The complete Jungle Game software application
- **Undo**: Functionality to reverse previous moves
- **View**: MVC component responsible for user interface and display

### File Format Terms

- **.jungle**: File extension for saved game states
- **.record**: File extension for game replay files
- **JSON**: JavaScript Object Notation format used for game saves
- **Persistence**: Long-term storage of game data

---

## User Requirements Definition

### Functional Requirements

#### Game Initialization and Management

**REQ-1: Game Session Management**
The system shall provide complete game session lifecycle management including initialization, gameplay, and termination capabilities.

- Initialize new games with proper board setup and piece placement
- Manage active game sessions with turn-based gameplay
- Terminate games gracefully with proper cleanup
- Support multiple game sessions through application restart

**REQ-2: Player Management**
The system shall support flexible player identification and management throughout game sessions.

- Accept custom player names through user input
- Generate random player names when custom names are not provided
- Display player identification consistently throughout the interface
- Maintain player-specific game statistics and piece ownership

#### Core Gameplay Features

**REQ-3: Move Processing and Validation**
The system shall implement comprehensive move validation and execution according to traditional Jungle Game rules.

- Validate piece movement patterns (one square horizontally/vertically)
- Enforce terrain-specific movement restrictions
- Process piece captures according to rank-based rules
- Maintain game state consistency after each move

**REQ-4: Game State Display**
The system shall provide comprehensive visual representation of current game status.

- Display complete board state with piece positions and ownership
- Show current player turn and available actions
- Indicate special board areas (dens, traps, rivers)
- Present piece information including type and rank

**REQ-5: Undo Functionality**
The system shall support limited move reversal to enhance user experience.

- Allow reversal of up to 3 previous moves per game
- Maintain game state history for undo operations
- Restore complete board state and turn information
- Prevent undo operations when history is unavailable

#### File Management and Persistence

**REQ-6: Game State Persistence**
The system shall provide reliable save and load functionality for game continuity.

- Save complete game state to .jungle files
- Load saved games with full state restoration
- Validate file integrity during load operations
- Handle file operation errors gracefully

**REQ-7: Game Recording and Replay**
The system shall support comprehensive game recording and replay capabilities.

- Record complete move history during gameplay
- Save game records to .record files with metadata
- Replay recorded games with step-by-step progression
- Support record file validation and error handling

### Non-Functional Requirements

#### Performance Requirements

**REQ-8: Response Time**
The system shall provide responsive user interaction with minimal delays.

- Process user commands within 100 milliseconds
- Display game state updates immediately after moves
- Complete file operations within 2 seconds for typical game sizes
- Maintain consistent performance throughout extended game sessions

**REQ-9: Memory Usage**
The system shall operate efficiently within reasonable memory constraints.

- Limit memory usage to under 50MB during normal operation
- Manage game state history efficiently for undo functionality
- Release resources properly during game termination
- Support games with up to 1000 moves without performance degradation

#### Reliability Requirements

**REQ-10: Data Integrity**
The system shall maintain data consistency and prevent corruption.

- Ensure game state remains valid after all operations
- Validate file formats during save and load operations
- Prevent invalid game states through comprehensive validation
- Recover gracefully from unexpected errors

**REQ-11: Error Handling**
The system shall provide robust error handling and user feedback.

- Display clear error messages for invalid user input
- Handle file system errors without application termination
- Validate all user commands before execution
- Provide helpful guidance for error resolution

#### Usability Requirements

**REQ-12: User Interface**
The system shall provide an intuitive command-line interface.

- Use clear and consistent command syntax
- Provide helpful prompts and instructions
- Display game information in readable format
- Support standard command-line interaction patterns

**REQ-13: Documentation**
The system shall include comprehensive user and developer documentation.

- Provide user manual with gameplay instructions
- Include developer documentation for code maintenance
- Document all command syntax and options
- Explain file formats and system architecture

#### Compatibility Requirements

**REQ-14: Platform Compatibility**
The system shall operate reliably across different computing environments.

- Support Python 3.8+ runtime environments
- Function on Windows, macOS, and Linux operating systems
- Use standard library components for maximum compatibility
- Avoid platform-specific dependencies where possible

### Quality Standards

#### Code Quality Standards

- **PEP 8**: Python code style guide compliance
- **Type Hints**: Comprehensive type annotation throughout codebase
- **Documentation**: Docstring documentation for all public methods
- **Testing**: Minimum 90% code coverage for model components

#### Process Standards

- **Version Control**: Git-based development with meaningful commit messages
- **Code Review**: Peer review for all significant code changes
- **Testing**: Automated unit and integration testing
- **Documentation**: Maintained technical and user documentation

---

## System Architecture

### Architectural Overview

The Jungle Game system implements the Model-View-Controller (MVC) architectural pattern to ensure clear separation of concerns, maintainability, and testability. This architecture provides a robust foundation for the game implementation while supporting future enhancements and modifications.

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Jungle Game System                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │             │    │             │    │             │     │
│  │    View     │    │ Controller  │    │    Model    │     │
│  │  Package    │◄──►│  Package    │◄──►│  Package    │     │
│  │             │    │             │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │          │
│         │                   │                   │          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Display   │    │   Command   │    │    Game     │     │
│  │ Components  │    │ Processing  │    │   Logic     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                    Utility Components                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    File     │    │   Logger    │    │ Exception   │     │
│  │  Manager    │    │             │    │  Handling   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                   External Interfaces                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ File System │    │ Command Line│    │   Python    │     │
│  │ Interface   │    │ Interface   │    │  Runtime    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Distribution

#### Model Package Components

**Core Game Logic**
- `Game`: Central game state manager and rule coordinator
- `Board`: 7x9 grid representation with terrain management
- `Player`: Player information and piece ownership tracking
- `GameState`: Immutable state snapshots for undo functionality

**Piece Hierarchy**
- `Piece`: Abstract base class defining common piece behavior
- `Rat`, `Cat`, `Dog`, `Wolf`, `Leopard`, `Tiger`, `Lion`, `Elephant`: Concrete piece implementations
- Specialized movement and capture logic for each piece type

**Supporting Classes**
- `Position`: Immutable coordinate representation
- `Move`: Move record with metadata
- `MoveResult`: Operation result communication

#### View Package Components

**Display Management**
- `GameView`: Main view coordinator and state presentation
- `BoardRenderer`: ASCII board visualization with piece representation
- `MessageDisplay`: User communication and error reporting

#### Controller Package Components

**User Interaction**
- `GameController`: Main game loop and command coordination
- `CommandParser`: Input parsing and validation
- `FileManager`: Save/load and record operations

#### Utility Components

**Cross-Cutting Concerns**
- `Logger`: Application logging and debugging support
- Exception hierarchy for error handling
- Configuration management for game parameters

### Architectural Principles

#### Separation of Concerns

Each package has distinct responsibilities:
- **Model**: Game rules, state management, and business logic
- **View**: User interface and information presentation
- **Controller**: User input handling and system coordination

#### Dependency Management

- Model components have no dependencies on View or Controller
- View components depend only on Model for data access
- Controller coordinates between Model and View without tight coupling

#### Extensibility

The architecture supports future enhancements:
- New piece types through inheritance
- Alternative user interfaces through View abstraction
- Additional game modes through Controller extension

### Reusable Components

#### Position and Coordinate System

The `Position` class provides reusable coordinate representation used throughout the system for board locations, movement calculations, and spatial relationships.

#### File Management Infrastructure

The `FileManager` component provides reusable serialization and persistence capabilities that can be extended for additional file formats or storage mechanisms.

#### Exception Handling Framework

A comprehensive exception hierarchy provides consistent error handling patterns across all system components.

---

## System Requirements Specification

### Functional Requirements Specification

#### Game Initialization Requirements

**FR-1: Board Setup**
- **Description**: The system shall initialize a 7x9 game board with proper terrain configuration
- **Input**: New game command
- **Processing**: Create board grid, configure terrain areas (dens, traps, rivers)
- **Output**: Initialized board with all terrain features properly positioned
- **Error Conditions**: Memory allocation failure, configuration errors

**FR-2: Piece Placement**
- **Description**: The system shall place all 16 pieces in their initial positions according to traditional setup
- **Input**: Board initialization request
- **Processing**: Create piece instances, assign to players, position on board
- **Output**: Board with all pieces in starting positions
- **Error Conditions**: Invalid position assignments, piece creation failures

#### Move Processing Requirements

**FR-3: Move Validation**
- **Description**: The system shall validate all move requests against game rules
- **Input**: Source position, destination position, current game state
- **Processing**: Check piece ownership, movement patterns, terrain restrictions, capture rules
- **Output**: Move validation result with success/failure indication
- **Error Conditions**: Invalid positions, rule violations, game state inconsistencies

**FR-4: Move Execution**
- **Description**: The system shall execute valid moves and update game state
- **Input**: Validated move request
- **Processing**: Update piece positions, handle captures, switch turns, record move
- **Output**: Updated game state with move applied
- **Error Conditions**: State update failures, history recording errors

#### Game State Management Requirements

**FR-5: State Persistence**
- **Description**: The system shall save complete game state to .jungle files
- **Input**: Current game state, target filename
- **Processing**: Serialize game data to JSON format, write to file system
- **Output**: Saved game file with complete state information
- **Error Conditions**: File system errors, serialization failures, permission issues

**FR-6: State Restoration**
- **Description**: The system shall load saved games and restore complete state
- **Input**: .jungle filename
- **Processing**: Read file, deserialize data, validate state, restore game
- **Output**: Restored game state ready for continued play
- **Error Conditions**: File not found, corruption, format incompatibility

#### Recording and Replay Requirements

**FR-7: Move Recording**
- **Description**: The system shall record all moves during gameplay
- **Input**: Executed moves with metadata
- **Processing**: Format move data, append to game record
- **Output**: Complete move history with timestamps and details
- **Error Conditions**: Recording failures, format errors

**FR-8: Game Replay**
- **Description**: The system shall replay recorded games step by step
- **Input**: .record filename
- **Processing**: Parse record file, recreate game sequence, display progression
- **Output**: Step-by-step game recreation with user control
- **Error Conditions**: File corruption, invalid move sequences

### Non-Functional Requirements Specification

#### Performance Requirements

**NFR-1: Response Time**
- **Requirement**: All user commands shall be processed within 100ms
- **Measurement**: Time from command input to system response
- **Rationale**: Ensure responsive user experience
- **Testing**: Automated performance testing with timing measurements

**NFR-2: Memory Efficiency**
- **Requirement**: System memory usage shall not exceed 50MB during normal operation
- **Measurement**: Peak memory consumption during extended gameplay
- **Rationale**: Efficient resource utilization
- **Testing**: Memory profiling during stress testing

#### Reliability Requirements

**NFR-3: Data Integrity**
- **Requirement**: Game state shall remain consistent across all operations
- **Measurement**: State validation checks pass 100% of the time
- **Rationale**: Prevent game corruption and ensure fair play
- **Testing**: Comprehensive state validation testing

**NFR-4: Error Recovery**
- **Requirement**: System shall recover gracefully from 95% of error conditions
- **Measurement**: Percentage of errors handled without application termination
- **Rationale**: Maintain system stability and user experience
- **Testing**: Error injection and recovery testing

#### Usability Requirements

**NFR-5: Command Clarity**
- **Requirement**: All commands shall use intuitive, consistent syntax
- **Measurement**: User testing with success rate >90% for first-time users
- **Rationale**: Minimize learning curve and user errors
- **Testing**: Usability testing with target user groups

**NFR-6: Error Messages**
- **Requirement**: Error messages shall be clear and actionable
- **Measurement**: User comprehension rate >95% in testing
- **Rationale**: Enable users to resolve issues independently
- **Testing**: Message clarity evaluation with user feedback

### Interface Requirements

#### User Interface Requirements

**UI-1: Command Line Interface**
- **Description**: Primary user interaction through command-line interface
- **Input Format**: Text commands with standardized syntax
- **Output Format**: Formatted text display with clear information hierarchy
- **Error Handling**: Inline error messages with correction guidance

**UI-2: Game Display**
- **Description**: Visual representation of game state and board
- **Format**: ASCII art board with piece symbols and terrain indicators
- **Information**: Current player, piece positions, game status
- **Updates**: Real-time display updates after each move

#### File System Interface Requirements

**FSI-1: Save File Format**
- **Format**: JSON structure with versioning information
- **Extension**: .jungle files for saved games
- **Content**: Complete game state, player information, move history
- **Validation**: Format verification during load operations

**FSI-2: Record File Format**
- **Format**: Human-readable text with structured move data
- **Extension**: .record files for game recordings
- **Content**: Move sequence, player actions, game metadata
- **Compatibility**: Forward and backward compatibility across versions

#### System Interface Requirements

**SI-1: Python Runtime Interface**
- **Version**: Python 3.8+ compatibility
- **Dependencies**: Standard library components only
- **Platform**: Cross-platform operation (Windows, macOS, Linux)
- **Installation**: No additional dependencies required

**SI-2: Operating System Interface**
- **File System**: Standard file operations for save/load functionality
- **Command Line**: Standard input/output for user interaction
- **Process Management**: Clean startup and shutdown procedures
- **Resource Management**: Proper resource allocation and cleanup

### Data Requirements

#### Data Models

**Game State Data**
- Board configuration (7x9 grid)
- Piece positions and ownership
- Player information and turn state
- Move history and timestamps
- Game status and victory conditions

**Persistence Data**
- Serialized game states for save files
- Move records for replay functionality
- Configuration data for game parameters
- Log data for debugging and analysis

#### Data Validation

**Input Validation**
- Position coordinates within board boundaries
- Move commands conform to syntax requirements
- File names meet system requirements
- Player names within acceptable length limits

**State Validation**
- Game state consistency checks
- Rule compliance verification
- Data integrity validation
- Format compatibility confirmation

#### Data Security

**File Protection**
- Save file integrity verification
- Backup creation before overwriting
- Error recovery for corrupted files
- Access permission validation

