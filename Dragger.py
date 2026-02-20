import pygame
from Constants import *
from square import Square

class Dragger:

    def __init__(self):
        self.dragging = False
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos):
        self.mouseX , self.mouseY = pos

    def update_blit(self, surface):
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mouseX,self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)

    def save_initial(self, pos):
        self.initial_row = pos[1] // square_size
        self.initial_col = pos[0] // square_size

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self, pos, board):

        # Moves Calculation 
        piece_moves = self.piece.moves
    
        # Calculate current possition 
        row = pos[1] // square_size
        col = pos[0] // square_size

        placed = False
        # Place Piece
        for move in piece_moves:
            move_row = move[0]
            move_col = move[1]


            if board.squares[row][col].is_empty() and (move_row == row and move_col == col):
                if self.piece.name == 'king' and self.piece.value_sign == 1:
                    board.white_king_row = row
                    board.white_king_col = col
                elif self.piece.name == 'king' and self.piece.value_sign == -1:
                    board.black_king_row = row
                    board.black_king_col = col

                board.squares[row][col].piece = self.piece
                placed = True
                break
            elif board.squares[row][col].has_enemy_piece(self.piece.color) and (move_row == row and move_col == col):
                if self.piece.name == 'king' and self.piece.value_sign == 1:
                    board.white_king_row = row
                    board.white_king_col = col
                elif self.piece.name == 'king' and self.piece.value_sign == -1:
                    board.black_king_row = row
                    board.black_king_col = col

                board.squares[row][col].piece = self.piece
                placed = True
                break


        # Delete Previous piece
        if placed == True:
            board.squares[self.initial_row][self.initial_col] = Square(self.initial_row, self.initial_col)

        # Undrag
        self.piece = None
        self.dragging = False