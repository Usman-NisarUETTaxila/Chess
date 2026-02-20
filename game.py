import pygame
from Constants import *
from board import Board
from Dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        
    def get_board(self):
        return self.board

    def show_bg(self,surface, white_in_check, black_in_check):
        for row in range(rows):
            for col in range(columns):
                if (row+col) % 2 == 0:
                    color = (234,235,200) # light green
                else:
                    color = (119,154,88)  # dark green

                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if (white_in_check == True and piece.name == 'king' and piece.value_sign == 1) or (black_in_check == True and piece.name == 'king' and piece.value_sign == -1):
                        color = (255,51,51)

                rect = (col * square_size,row * square_size,square_size,square_size)
                pygame.draw.rect(surface , color , rect)

    def show_pieces(self, surface):
        for row in range(rows):
            for col in range(columns):
                # Checking Piece
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col * square_size + square_size // 2, row * square_size + square_size // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)

    def show_possible_moves(self, surface, moves):
        color = (173, 216, 230)
        for move in moves:
            row = move[0]
            col = move[1]

            rect = (col * square_size,row * square_size,square_size,square_size)
            pygame.draw.rect(surface , color , rect)
    