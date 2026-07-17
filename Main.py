import pygame
import sys

from Constants import *
from game import *

class Main:
    # Main Variables of the chess game and initialization of display
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def reset(self):
        """Restart the game from scratch."""
        self.game = Game()
        pygame.display.set_caption("Chess")

    # Main loop function of the game and all the events
    def mainloop(self):

        game    = self.game
        screen  = self.screen
        board   = self.game.board
        dragger = self.game.dragger
        piece_moves = []

        while True:
            # --- Always re-bind after a possible reset ---
            game    = self.game
            board   = self.game.board
            dragger = self.game.dragger

            # --- Draw ---
            game.show_bg(screen)
            game.show_possible_moves(screen, piece_moves)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            # Show game-over overlay on top of everything
            if game.game_over:
                game.show_game_over(screen)
                pygame.display.update()

                # Only listen for R (restart) or Quit when game is over
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset()
                        piece_moves = []
                continue  # skip normal input processing

            # --- Update window title with whose turn it is ---
            pygame.display.set_caption(f"Chess  —  {game.current_turn.capitalize()}'s Turn")

            for event in pygame.event.get():

                # ── Mouse button down: pick up a piece ──────────────────────
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // square_size
                    clicked_col = dragger.mouseX // square_size

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # Only allow dragging pieces that belong to the current player
                        if piece.color == game.current_turn:
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # calc_moves with check_filter=True so only legal moves shown
                            board.calc_moves(piece, clicked_row, clicked_col, check_filter=True)
                            piece_moves = piece.moves

                # ── Mouse motion: follow the dragged piece ──────────────────
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                # ── Mouse button up: drop the piece ────────────────────────
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        initial_row = dragger.initial_row
                        initial_col = dragger.initial_col

                        dragger.undrag_piece(event.pos, board)

                        # If the source square is now empty the move was accepted
                        if not board.squares[initial_row][initial_col].has_piece():
                            game.next_turn()
                            # Check for checkmate / stalemate for the new current player
                            game.check_game_over()

                    piece_moves.clear()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        piece_moves = []

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()