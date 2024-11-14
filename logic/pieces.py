# pieces.py

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
