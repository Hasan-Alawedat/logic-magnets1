import pygame
from board import SCREEN_SIZE, GRID_SIZE, CELL_SIZE
from board import Board
from phases import levels
from circles import Red, Purple

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Logic Magnets")

    game = Board(size=GRID_SIZE, levels=levels)
    game.initialize(0)

    cursor_position = (0, 0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    movable_pieces = [piece for piece in game.pieces if isinstance(piece, (Red, Purple))]
                    if movable_pieces:
                        game.selected_index = (game.selected_index + 1) % len(movable_pieces)
                        game.selected_piece = movable_pieces[game.selected_index]

                elif event.key == pygame.K_RETURN:
                    if game.selected_piece and not game.piece_selected:
                        game.piece_selected = True
                        cursor_position = (game.selected_piece.x, game.selected_piece.y)
                    elif game.piece_selected:
                        game.move(game.selected_piece, cursor_position[0] - game.selected_piece.x, cursor_position[1] - game.selected_piece.y)
                        game.piece_selected = False
                        game.selected_piece = None
                        game.selected_index = -1

                elif game.piece_selected:
                    if event.key == pygame.K_UP:
                        cursor_position = (max(0, cursor_position[0] - 1), cursor_position[1])
                    elif event.key == pygame.K_DOWN:
                        cursor_position = (min(GRID_SIZE - 1, cursor_position[0] + 1), cursor_position[1])
                    elif event.key == pygame.K_LEFT:
                        cursor_position = (cursor_position[0], max(0, cursor_position[1] - 1))
                    elif event.key == pygame.K_RIGHT:
                        cursor_position = (cursor_position[0], min(GRID_SIZE - 1, cursor_position[1] + 1))

                elif event.key == pygame.K_n:
                    game.initialize((game.current_level + 1) % len(levels))
                
                elif event.key == pygame.K_k:
                    game.initialize((game.current_level - 1) % len(levels))

        game.drawboard(screen)

        if game.selected_piece:
            if game.piece_selected:
                rect = pygame.Rect(cursor_position[1] * CELL_SIZE, cursor_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, 0, 255), rect, 3)
            else:
                rect = pygame.Rect(game.selected_piece.y * CELL_SIZE, game.selected_piece.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
