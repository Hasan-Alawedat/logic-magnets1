from collections import deque


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

class Piece:
    def __init__(self, symbol, row, col):
        self.symbol = symbol
        self.row = row
        self.col = col

    def move(self, grid, new_row, new_col):
        if grid.within_bounds(new_row, new_col) and grid.empty(new_row, new_col):
            grid.remove_piece(self.row, self.col)
            self.row, self.col = new_row, new_col
            grid.place_piece(self, self.row, self.col)
            return True
        return False

class RedPiece(Piece):
    def __init__(self, row, col):
        super().__init__('R', row, col)

    def attract(self, grid, pieces):
        for p in pieces:
            if p != self and isinstance(p, (GrayPiece, PurplePiece)):
                if p.row == self.row:  
                    if p.col < self.col:  
                        self._attract_piece(grid, p, 0, 1)
                    elif p.col > self.col:  
                        self._attract_piece(grid, p, 0, -1)
                elif p.col == self.col:  
                    if p.row < self.row:  
                        self._attract_piece(grid, p, 1, 0)
                    elif p.row > self.row:  
                        self._attract_piece(grid, p, -1, 0)

    def _attract_piece(self, grid, piece, row_dir, col_dir):
        new_row = piece.row + row_dir
        new_col = piece.col + col_dir
        if grid.within_bounds(new_row, new_col) and grid.empty(new_row, new_col):
            grid.remove_piece(piece.row, piece.col)
            piece.row, piece.col = new_row, new_col
            grid.place_piece(piece, new_row, new_col)

class PurplePiece(Piece):
    def __init__(self, row, col):
        super().__init__('P', row, col)

    def repel(self, grid, pieces):
        for p in pieces:
            if p != self and isinstance(p, (GrayPiece, RedPiece)):
                if p.row == self.row:  
                    if p.col < self.col:   
                        self._repel_piece(grid, p, 0, -1)
                    elif p.col > self.col:  
                        self._repel_piece(grid, p, 0, 1)
                elif p.col == self.col:  
                    if p.row < self.row:  
                        self._repel_piece(grid, p, -1, 0)
                    elif p.row > self.row:  
                        self._repel_piece(grid, p, 1, 0)

    def _repel_piece(self, grid, piece, row_dir, col_dir):
        new_row = piece.row + row_dir
        new_col = piece.col + col_dir
        if grid.within_bounds(new_row, new_col) and grid.empty(new_row, new_col):
            grid.remove_piece(piece.row, piece.col)
            piece.row, piece.col = new_row, new_col
            grid.place_piece(piece, new_row, new_col)

class GrayPiece(Piece):
    def __init__(self, row, col):
        super().__init__('G', row, col)



from collections import deque

class Game:
    def __init__(self, size, target_positions, red_pos, purple_pos, gray_pos):
        self.grid = Grid(size, target_positions)
        self.pieces = []
        self.red_piece = RedPiece(*red_pos)
        self.purple_piece = PurplePiece(*purple_pos)
        self.gray_pieces = [GrayPiece(row, col) for row, col in gray_pos]
        self.pieces = [self.red_piece, self.purple_piece] + self.gray_pieces
        for piece in self.pieces:
            self.grid.place_piece(piece, piece.row, piece.col)

    def display(self):
        self.grid.display()

    def is_solved(self):
        for target in self.grid.targets:
            if not any(piece.row == target.row and piece.col == target.col for piece in self.pieces):
                return False
        return True

    def play_move(self, piece, new_row, new_col):
        if piece.move(self.grid, new_row, new_col):
            if isinstance(piece, RedPiece):
                piece.attract(self.grid, self.pieces)
            elif isinstance(piece, PurplePiece):
                piece.repel(self.grid, self.pieces)

            for target in self.grid.targets:
                if target.row == new_row and target.col == new_col:
                    target.occupy()
                elif target.row == piece.row and target.col == piece.col:
                    target.release()
            return True
        return False

    def get_possible(self, piece):
        possible_moves = []
        if isinstance(piece, GrayPiece):
            return possible_moves  
        for row in range(self.grid.size):
            for col in range(self.grid.size):
                if piece.move(self.grid, row, col):
                    possible_moves.append((row, col))
                    piece.move(self.grid, piece.row, piece.col)  
        return possible_moves

    
    def dfs(self, depth, visited, moves):
     if self.is_solved():
        print("Found solution!")
        self.print_solution(moves)
        return True
     if depth == 0:
        return False

     current_state = tuple((piece.symbol, piece.row, piece.col) for piece in self.pieces)
     if current_state in visited:
        return False  

     visited.add(current_state)  

     for piece in self.pieces:
        if isinstance(piece, GrayPiece):
            continue  

        possible_moves = self.get_possible(piece)
        for row, col in possible_moves:

            original_row, original_col = piece.row, piece.col
            self.play_move(piece, row, col)
            moves.append((piece, (row, col))) 

            print(f"Trying move: {piece.symbol} to ({row}, {col})")

            if self.dfs(depth - 1, visited, moves):
                return True

            moves.pop()  
            piece.move(self.grid, original_row, original_col)  

     visited.remove(current_state)  
     return False

    
    def bfs(self):
        queue = deque([(self.pieces, [])]) 
        visited = set()
        
        print("Initial board:")
        self.display()

        while queue:
            current_pieces, moves = queue.popleft()
            self.pieces = current_pieces  

            if self.is_solved():
                print("\nFound solution!")
                self.print_solution(moves)
                return True
            current_state = frozenset((p.symbol, p.row, p.col) for p in self.pieces)

            if current_state in visited:
                continue  
            visited.add(current_state)
            
            for piece in self.pieces:
                if isinstance(piece, GrayPiece):
                    continue  
                possible_moves = self.get_possible(piece)
                for row, col in possible_moves:

                    print(f"Trying move: {piece.symbol} to ({row}, {col})")

                    original_row, original_col = piece.row, piece.col
                    if self.play_move(piece, row, col):  
                        new_moves = moves + [(piece, (row, col))]  



                        if self.is_solved():
                            print("\nFound solution!")
                            self.print_solution(new_moves)
                            return True
                        new_state = frozenset((p.symbol, p.row, p.col) for p in self.pieces)
                        if new_state not in visited:
                            queue.append((self.pieces.copy(), new_moves))
                    
                        piece.move(self.grid, original_row, original_col)

        print("No solution found.")
        return False

    def print_solution(self, moves):
        print("Moves made:")
        for move in moves:
            piece, (row, col) = move
            print(f"Piece {piece.symbol} moved to ({row}, {col})")
        print("\nFinal board:")
        self.display()

    def solve_game(self):
        print("Initial board:")
        self.display()
        
        mode = input("Enter 'd' for DFS, 'b' for BFS: ").lower()
        if mode == 'd':
            visited = set()
            depth = 10 
            if self.dfs(depth, visited, []):
                return
        elif mode == 'b':
            self.bfs()
        else:
            print("Invalid option.")


game = Game(size=4, target_positions=[(1, 1), (2, 2)], red_pos=(0, 0), purple_pos=(3, 3), gray_pos=[(2, 0),(0,2)]
)
game.display()


mode = input("Enter 'd' for solution with DFS, 'b' for BFS, or 'h' for manual play: ").lower()
if mode in ['d', 'b']:
    game.solve_game()
elif mode == 'h':

    while not game.is_solved():
        piece_type = input("Choose piece (r for red, p for purple): ").lower()
        current_row, current_col = map(int, input("Enter current position (row column): ").split())
        new_row, new_col = map(int, input("Enter new position (row column): ").split())
        piece = game.red_piece if piece_type == 'r' else game.purple_piece
        if piece.row == current_row and piece.col == current_col:
            if game.play_move(piece, new_row, new_col):
                game.display()
            else:
                print("Invalid move.")
        else:
            print("Piece is not at specified location.")
        
        if game.is_solved():
            print("Congratulations, you solved the game!")
else:
    print("Invalid option. Please enter 'd', 'b', or 'h'.")
