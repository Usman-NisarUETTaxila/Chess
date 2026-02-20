import pygame
import sys

from Constants import *
from game import *

class Main:
    # Main Variables of the chess game and initialization of display
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Chess")
        self.game = Game()

    # Main loop function of the game and all the events
    def mainloop(self):

        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        white_in_check = [False]
        black_in_check = [False]
        piece_moves = []
        while True:
            game.show_bg(screen, white_in_check[0], black_in_check[0])
            game.show_possible_moves(screen, piece_moves)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():


                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // square_size
                    clicked_col = dragger.mouseX // square_size

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        board.calc_moves(piece, clicked_row, clicked_col)
                        piece_moves = piece.moves

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece(event.pos, board)

                    white_in_check[0] = False
                    black_in_check[0] = False
                    
                    # Move Calculation 
                    for row in range(rows):
                        for col in range(columns):
                            # Checking Piece
                            if board.squares[row][col].has_piece():
                                piece = board.squares[row][col].piece
                                board.calc_moves(piece, row, col)

                                for move in piece.moves:
                                    move_row, move_col = move[0], move[1]

                                    if move_row == board.white_king_row and move_col == board.white_king_col and piece.value_sign != 1:
                                        white_in_check[0] = True
                                        break
                                    elif move_row == board.black_king_row and move_col == board.black_king_col and piece.value_sign != -1:
                                        black_in_check[0] = True
                                        break

                    print(white_in_check)
                    print(black_in_check)
                    piece_moves.clear()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            

            pygame.display.update()

main = Main()
main.mainloop()