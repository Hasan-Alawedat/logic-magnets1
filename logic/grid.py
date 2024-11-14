# grid.py

class TargetCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_occupied = False  

    def occupy(self):
        self.is_occupied = True

    def release(self):
        self.is_occupied = False

class Grid:
    def __init__(self, size, target_positions):
        self.size = size
        self.grid = [['*' for _ in range(size)] for _ in range(size)]  
        self.targets = [TargetCell(row, col) for row, col in target_positions]  
        for target in self.targets:
            self.grid[target.row][target.col] = 'o'  

    def within_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def empty(self, row, col):
        return self.grid[row][col] == '*' or self.grid[row][col] == 'o'

    def place_piece(self, piece, row, col):
        self.grid[row][col] = piece.symbol
        for target in self.targets:
            if target.row == row and target.col == col:
                target.occupy()

    def remove_piece(self, row, col):
        if self.is_target_cell(row, col):
            self.grid[row][col] = 'o'  
        else:
            self.grid[row][col] = '*'

    def is_target_cell(self, row, col):
        return any(target.row == row and target.col == col for target in self.targets)

    def display(self):
        for row in self.grid:
            print(" ".join(row))
        print()
