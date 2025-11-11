# Jungle Game Board Layout

## Board Dimensions
- 9 rows (0-8) x 7 columns (0-6)
- Blue player at top (rows 0-2)
- Red player at bottom (rows 6-8)

## Initial Piece Positions

```
Row 0: [E] [ ] [W] [D] [L] [ ] [R]    Blue pieces
Row 1: [ ] [C] [T] [ ] [T] [D] [ ]    T = Trap, D = Den
Row 2: [T] [ ] [ ] [ ] [ ] [ ] [L]
Row 3: [ ] [~] [~] [ ] [~] [~] [ ]    ~ = Water
Row 4: [ ] [~] [~] [ ] [~] [~] [ ]    ~ = Water
Row 5: [ ] [~] [~] [ ] [~] [~] [ ]    ~ = Water
Row 6: [L] [ ] [ ] [ ] [ ] [ ] [T]    Red pieces
Row 7: [ ] [D] [T] [ ] [T] [C] [ ]    T = Trap, D = Den
Row 8: [R] [ ] [L] [D] [W] [ ] [E]
```

## Legend
- **E** = Elephant (rank 8)
- **L** = Lion (rank 7) or Leopard (rank 5)
- **T** = Tiger (rank 6)
- **W** = Wolf (rank 4)
- **D** = Dog (rank 3)
- **C** = Cat (rank 2)
- **R** = Rat (rank 1)
- **~** = Water (only Rat can enter)
- **T** (in terrain) = Trap
- **D** (in terrain) = Den

## Detailed Starting Positions

### Blue Player (Top)
- Row 0: Elephant(0,0), Wolf(0,2), Leopard(0,4), Rat(0,6)
- Row 1: Cat(1,1), Dog(1,5)
- Row 2: Tiger(2,0), Lion(2,6)

### Red Player (Bottom)
- Row 6: Lion(6,0), Tiger(6,6)
- Row 7: Dog(7,1), Cat(7,5)
- Row 8: Rat(8,0), Leopard(8,2), Wolf(8,4), Elephant(8,6)

## Terrain Features

### Water (Rows 3-5, Columns 1-2 and 4-5)
- (3,1), (3,2), (3,4), (3,5)
- (4,1), (4,2), (4,4), (4,5)
- (5,1), (5,2), (5,4), (5,5)

### Blue Den and Traps (Top)
- Den: (0,3)
- Traps: (0,2), (0,4), (1,2), (1,4)

### Red Den and Traps (Bottom)
- Den: (8,3)
- Traps: (7,2), (7,4), (8,2), (8,4)

## Valid Move Paths (Avoiding Water)

### Column 0 (Left edge - No water)
- Clear path from row 0 to row 8
- Good for: Elephant, Lion, Tiger, etc.

### Column 3 (Center - No water)
- Clear path from row 0 to row 8
- Contains both dens
- Good for: Any piece

### Column 6 (Right edge - No water)
- Clear path from row 0 to row 8
- Good for: Elephant, Lion, Tiger, etc.

### Columns 1-2 and 4-5 (Water zones)
- Rows 3-5 are water
- Only Rats can pass through
- Other pieces must go around or jump (Lion/Tiger)

## Sample Valid Move Sequences

### Simple Moves (No obstacles)
1. Red Rat: (8,0) → (8,1) [right]
2. Blue Rat: (0,6) → (0,5) [left]
3. Red Elephant: (8,6) → (8,5) [left]
4. Blue Elephant: (0,0) → (1,0) [down]

### Moving Around Water
1. Red Lion at (6,0): Can move up to (5,0), (4,0), (3,0), (2,0), (1,0), (0,0)
2. Blue Tiger at (2,0): Can move down to (3,0), (4,0), (5,0), (6,0), (7,0), (8,0)

### Lion/Tiger River Jumps
- Red Lion at (6,0) → (5,0) → (4,0) → can jump to (4,4) [horizontal jump over water]
- Blue Lion at (2,6) → (3,6) → (4,6) → can jump to (4,2) [horizontal jump over water]

### Rat Water Movement
- Red Rat: (8,0) → (8,1) → (7,1) is BLOCKED by Red Dog at (7,1)
- Red Rat: (8,0) → (7,0) is BLOCKED by Red Lion at (6,0) path
- Better: Move rat sideways first to clear column

## Key Insights for Test Design

1. **Column 0 is clear**: Best for moving pieces up/down without water issues
2. **Column 3 is clear**: Center column, good for den approaches
3. **Column 6 is clear**: Right edge, good for moving pieces
4. **Pieces block each other**: Dog at (7,1) blocks rat from moving up column 1
5. **Water blocks non-rats**: Rows 3-5 in columns 1,2,4,5 are impassable except for rats
6. **Traps are adjacent to dens**: Easy to test trap mechanics near dens
