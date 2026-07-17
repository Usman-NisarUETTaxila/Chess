import pygame
from Constants import *
from board import Board
from Dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.current_turn = 'white'  # White always goes first
        self.game_over = False
        self.winner = None           # 'white', 'black', or 'draw'
        # Cached check state — updated once per move, read every frame
        self.white_in_check = False
        self.black_in_check = False

    def next_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def get_board(self):
        return self.board

    def has_any_legal_moves(self, color):
        """Returns True if the given color has at least one legal move remaining."""
        for r in range(rows):
            for c in range(columns):
                if self.board.squares[r][c].has_piece():
                    piece = self.board.squares[r][c].piece
                    if piece.color == color:
                        self.board.calc_moves(piece, r, c, check_filter=True)
                        if piece.moves:
                            return True
        return False

    def update_check_state(self):
        """Recompute and cache which kings are in check. Call once per move."""
        self.white_in_check = self.board.is_king_in_check('white')
        self.black_in_check = self.board.is_king_in_check('black')

    def check_game_over(self):
        """
        Call after every move. Detects checkmate and stalemate for the
        player whose turn it just became (self.current_turn).
        Sets self.game_over and self.winner accordingly.
        """
        # Update cached check flags first (single computation per move)
        self.update_check_state()

        color = self.current_turn
        in_check  = self.white_in_check if color == 'white' else self.black_in_check
        has_moves = self.has_any_legal_moves(color)

        if not has_moves:
            self.game_over = True
            if in_check:
                # Checkmate — the side that just moved wins
                self.winner = 'black' if color == 'white' else 'white'
            else:
                # Stalemate — draw
                self.winner = 'draw'

    def show_bg(self, surface):
        for row in range(rows):
            for col in range(columns):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # light green
                else:
                    color = (119, 154, 88)   # dark green

                # Highlight king square red using the cached check flags (no recalculation)
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.name == 'king':
                        if (piece.color == 'white' and self.white_in_check) or \
                           (piece.color == 'black' and self.black_in_check):
                            color = (255, 51, 51)

                rect = (col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(rows):
            for col in range(columns):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col * square_size + square_size // 2, row * square_size + square_size // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_possible_moves(self, surface, moves):
        color = (173, 216, 230)
        for move in moves:
            row = move[0]
            col = move[1]
            rect = (col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(surface, color, rect)

    def show_game_over(self, surface):
        """Render a semi-transparent overlay announcing the result."""
        # Dark overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        font_big   = pygame.font.SysFont('Arial', 54, bold=True)
        font_small = pygame.font.SysFont('Arial', 28)

        if self.winner == 'draw':
            title_text = 'Stalemate!'
            sub_text   = "It's a Draw"
            title_color = (230, 200, 60)
        else:
            title_text  = 'Checkmate!'
            sub_text    = f'{self.winner.capitalize()} Wins!'
            title_color = (255, 255, 255)

        title_surf = font_big.render(title_text, True, title_color)
        sub_surf   = font_small.render(sub_text, True, (200, 200, 200))
        hint_surf  = font_small.render('Press R to restart', True, (150, 150, 150))

        cx = width // 2
        cy = height // 2
        surface.blit(title_surf, title_surf.get_rect(center=(cx, cy - 50)))
        surface.blit(sub_surf,   sub_surf.get_rect(center=(cx, cy + 10)))
        surface.blit(hint_surf,  hint_surf.get_rect(center=(cx, cy + 55)))