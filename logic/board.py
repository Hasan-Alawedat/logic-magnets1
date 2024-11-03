import pygame
from circles import Red, Purple, Gray


YELLOW = (255, 150, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 160)
WHITE = (255, 255, 255)
SCREEN_SIZE = 700
GRID_SIZE = 6
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FONT_SIZE = 20  


pygame.init()
font = pygame.font.Font(None, FONT_SIZE)

class Board:
    def __init__(self, size, levels):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.levels = levels
        self.current_level = 0
        self.target_positions = []
        self.pieces = []
        self.move_count = 0  
        self.initialize(self.current_level)
        
    def initialize(self, level_number):
        self.current_level = level_number
        self.clearboard()
        level_data = self.levels[level_number]
        self.selected_position = (0, 0)  
        self.target_positions = level_data["targets"]
        self.move_count = level_data.get("move", 10)  


        self.selected_piece = None
        self.selected_index = -1
        self.piece_selected = False


        for x, y in self.target_positions:
            self.grid[x][y] = "target"

        for piece_data in level_data["pieces"]:
            piece = self.create(piece_data["type"], *piece_data["position"])
            self.pieces.append(piece)
            self.grid[piece.x][piece.y] = piece
            self.getpossible(piece)

        print(f" {level_number} {self.move_count}")
        print(f" {self.selected_position}")

        if self.pieces:
            self.selected_position = (self.pieces[0].x, self.pieces[0].y)

    def clearboard(self):
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.pieces = []

    def create(self, piece_type, x, y):
        if piece_type == "red":
            return Red(x, y)
        elif piece_type == "purple":
            return Purple(x, y)
        elif piece_type == "gray":
            return Gray(x, y)

    def move(self, piece, dx, dy): 
        new_x, new_y = piece.x + dx, piece.y + dy
        if (0 <= new_x < self.size and 0 <= new_y < self.size and
            (self.grid[new_x][new_y] is None or (new_x, new_y) in self.target_positions)):
            
            self.grid[piece.x][piece.y] = None
            piece.move(dx, dy)
            self.grid[piece.x][piece.y] = piece
            self.move_count -= 1  
            
            if isinstance(piece, Purple):
                self.applyrepel(piece)

            elif isinstance(piece, Red):
                self.applyattract(piece)

    def applyrepel(self, repel_piece):
     for other_piece in self.pieces:
        if other_piece is not repel_piece:
            if other_piece.x == repel_piece.x or other_piece.y == repel_piece.y:
                dx, dy = 0, 0
                if other_piece.x == repel_piece.x:
                    dy = 1 if other_piece.y > repel_piece.y else -1
                elif other_piece.y == repel_piece.y:
                    dx = 1 if other_piece.x > repel_piece.x else -1

                new_x, new_y = other_piece.x + dx, other_piece.y + dy
                if (0 <= new_x < self.size and 0 <= new_y < self.size and
                    (self.grid[new_x][new_y] is None or 
                     (new_x, new_y) in self.target_positions and
                     all(self.grid[new_x][new_y] is None for piece in self.pieces if (piece.x, piece.y) == (new_x, new_y)))):  

                    self.grid[other_piece.x][other_piece.y] = None
                    other_piece.move(dx, dy)
                    self.grid[other_piece.x][other_piece.y] = other_piece



    def applyattract(self, magnet_piece):
     for other_piece in self.pieces:
        if other_piece is not magnet_piece:
            if other_piece.x == magnet_piece.x or other_piece.y == magnet_piece.y:
                dx, dy = 0, 0
                if other_piece.x == magnet_piece.x:
                    dy = -1 if other_piece.y > magnet_piece.y else 1
                elif other_piece.y == magnet_piece.y:
                    dx = -1 if other_piece.x > magnet_piece.x else 1

                new_x, new_y = other_piece.x + dx, other_piece.y + dy
                if (0 <= new_x < self.size and 0 <= new_y < self.size and
                    (self.grid[new_x][new_y] is None or 
                     (new_x, new_y) in self.target_positions and
                     all(self.grid[new_x][new_y] is None for piece in self.pieces if (piece.x, piece.y) == (new_x, new_y)))):  

                    self.grid[other_piece.x][other_piece.y] = None
                    other_piece.move(dx, dy)
                    self.grid[other_piece.x][other_piece.y] = other_piece


    def getpossible(self, piece):
       if not isinstance(piece, (Red, Purple,Gray)):
          return []

       possible_moves = []

       for x in range(self.size):
         for y in range(self.size):
            if (x, y) == (piece.x, piece.y):
                continue
            
            target_piece = self.grid[x][y]
            if target_piece is None:  
                possible_moves.append((x, y))

       print(f"({piece.x}, {piece.y}): {possible_moves}")
       return possible_moves






    def drawboard(self, screen):
        self.update()

        screen.fill(YELLOW)
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                
                if (x, y) in self.target_positions:
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
        
        for piece in self.pieces:
            color = GRAY if isinstance(piece, Gray) else (RED if isinstance(piece, Red) else PURPLE)
            pygame.draw.circle(screen, color, (piece.y * CELL_SIZE + CELL_SIZE // 2, piece.x * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        moves_text = font.render(f'Moves Left: {self.move_count}', True, BLACK)
        screen.blit(moves_text, (10, 10))
    
        level_text = font.render(f'Level: {self.current_level + 1}', True, BLACK)  
        screen.blit(level_text, (610, 10))  


    def next(self):
        if self.current_level < len(self.levels) - 1:
            self.initialize(self.current_level + 1)


    def checkwin(self):
        for target_x, target_y in self.target_positions:
            piece = self.grid[target_x][target_y]
            if not isinstance(piece, (Gray, Red, Purple)):
                return False
        return True


    def update(self):

        if self.checkwin():
            self.next()

        elif self.move_count <= 0:
            self.initialize(self.current_level)
