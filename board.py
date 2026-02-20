from Constants import *
from square import Square
from Pieces import *

class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(columns)]
        self.white_king_row = 7
        self.white_king_col = 4
        self.black_king_row = 0
        self.black_king_col = 4
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # important method to calculate the valid moves of a piece
    def calc_moves(self, piece, row, col):
        def bishop_moves():
            # Diagonal move generation 
            for i in range(4):
                for j in range(1,8):
                    # First Diagonal
                    if(i==0):
                        move_row, move_col = row+j, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Second Diagonal
                    elif(i==1):
                        move_row, move_col = row+j, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Third Diagonal
                    elif(i==2):
                        move_row, move_col = row-j, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    
                    # Fourth Diagonal
                    elif(i==3):
                        move_row, move_col = row-j, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
            
            print(piece.moves)

        def queen_moves():
            # Horizontal and Vertical Move Generation + Diagonal Generation
            for i in range(4):
                for j in range(1,8):
                    # First Line
                    if(i==0):
                        move_row, move_col = row, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Second Line
                    elif(i==1):
                        move_row, move_col = row, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Third Line
                    elif(i==2):
                        move_row, move_col = row-j, col
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    
                    # Fourth Line
                    elif(i==3):
                        move_row, move_col = row+j, col
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break

            for i in range(4):
                for j in range(1,8):
                    # First Diagonal
                    if(i==0):
                        move_row, move_col = row+j, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Second Diagonal
                    elif(i==1):
                        move_row, move_col = row+j, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Third Diagonal
                    elif(i==2):
                        move_row, move_col = row-j, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    
                    # Fourth Diagonal
                    elif(i==3):
                        move_row, move_col = row-j, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break

            print(piece.moves)

        def rook_moves():
            # Horizontal and Vertical Move Generation
            for i in range(4):
                for j in range(1,8):
                    # First Line
                    if(i==0):
                        move_row, move_col = row, col+j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Second Line
                    elif(i==1):
                        move_row, move_col = row, col-j
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break
                    # Third Line
                    elif(i==2):
                        move_row, move_col = row-j, col
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break

                    # Fourth Line
                    elif(i==3):
                        move_row, move_col = row+j, col
                        if not self._add_move(piece.moves, move_row, move_col, piece):
                            break

            print(piece.moves)

        def king_moves():
            possible_moves = [
                (row+1, col),
                (row-1, col),
                (row, col+1),
                (row, col-1),
                (row+1, col+1),
                (row+1, col-1),
                (row-1, col+1),
                (row-1, col-1)
            ]

            for i,possible_move in enumerate(possible_moves):
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        possible_moves[i] = (-1,-1)
                else:
                    possible_moves[i] = (-1,-1)
            piece.moves = [move for move in possible_moves if move != (-1,-1)]
            print(piece.moves)

        def knight_moves():
            # knight has 8 possible moves when placed in center
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for i,possible_move in enumerate(possible_moves):
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        possible_moves[i] = (-1,-1)
                else:
                    possible_moves[i] = (-1,-1)
            
            piece.moves = [move for move in possible_moves if move != (-1,-1)]
            print(piece.moves)
        
        def pawn_moves():
            # For White
            if(piece.dir == -1):
                possible_moves = [
                    (row-1, col),
                    (row-2, col),
                    (row-1, col+1),
                    (row-1, col-1)
                ]

                front_row, front_col = possible_moves[0]
                if Square.in_range(front_row, front_col):
                    if self.squares[front_row][front_col].has_team_piece(piece.color) or self.squares[front_row][front_col].has_enemy_piece(piece.color):
                        possible_moves[0] = (-1,-1)
                else:
                    possible_moves[0] = (-1,-1)

                front_forward_row, front_forward_col = possible_moves[1]
                if row != 6 or self.squares[front_forward_row][front_forward_col].has_team_piece(piece.color) or self.squares[front_forward_row][front_forward_col].has_enemy_piece(piece.color):
                    possible_moves[1] = (-1,-1)
                
                
                
                right_enemy_row, right_enemy_col = possible_moves[2]

                if Square.in_range(right_enemy_row, right_enemy_col):
                    if not self.squares[right_enemy_row][right_enemy_col].has_enemy_piece(piece.color):
                        possible_moves[2] = (-1,-1)
                else:
                    possible_moves[2] = (-1,-1)
                
                left_enemy_row, left_enemy_col = possible_moves[3]

                if Square.in_range(left_enemy_row, left_enemy_col):
                    if not self.squares[left_enemy_row][left_enemy_col].has_enemy_piece(piece.color):
                        possible_moves[3] = (-1,-1)
                else:
                    possible_moves[3] = (-1,-1)
                
                piece.moves = [move for move in possible_moves if move != (-1,-1)]
                print(piece.moves)
            # For Black
            else:
                possible_moves = [
                    (row+1, col),
                    (row+2, col),
                    (row+1, col+1),
                    (row+1, col-1)
                ]

                front_row, front_col = possible_moves[0]
                if Square.in_range(front_row, front_col):
                    if self.squares[front_row][front_col].has_team_piece(piece.color) or self.squares[front_row][front_col].has_enemy_piece(piece.color):
                        possible_moves[0] = (-1,-1)
                else:
                    possible_moves[0] = (-1,-1)

                front_forward_row, front_forward_col = possible_moves[1]
                if row != 1 or self.squares[front_forward_row][front_forward_col].has_team_piece(piece.color) or self.squares[front_forward_row][front_forward_col].has_enemy_piece(piece.color):
                    possible_moves[1] = (-1,-1)
                
                
                right_enemy_row, right_enemy_col = possible_moves[2]

                if Square.in_range(right_enemy_row, right_enemy_col):
                    if not self.squares[right_enemy_row][right_enemy_col].has_enemy_piece(piece.color):
                        possible_moves[2] = (-1,-1)
                else:
                    possible_moves[2] = (-1,-1)
                
                left_enemy_row, left_enemy_col = possible_moves[3]

                if Square.in_range(left_enemy_row, left_enemy_col):
                    if not self.squares[left_enemy_row][left_enemy_col].has_enemy_piece(piece.color):
                        possible_moves[3] = (-1,-1)
                else:
                    possible_moves[3] = (-1,-1)

                piece.moves = [move for move in possible_moves if move != (-1,-1)]
                print(piece.moves)   

        if isinstance(piece, Pawn):
            return pawn_moves()

        elif isinstance(piece, Knight):
            return knight_moves()

        elif isinstance(piece, Bishop):
            return bishop_moves()

        elif isinstance(piece, Rook):
            return rook_moves()

        elif isinstance(piece, Queen):
            return queen_moves()

        elif isinstance(piece, King):
            return king_moves()

        else:
            return []

    def _create(self):
        for row in range(rows):
            for col in range(columns):
                self.squares[row][col] = Square(row,col)



    def _add_pieces(self,color):
        if color == 'white':
            row_pawn,row_other = (6,7)
        else:
            row_pawn, row_other = (1,0)
        # Creating Pawns
        for col in range(columns):
            self.squares[row_pawn][col] = Square(row_pawn,col,Pawn(color))

        # Creating Knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6,Knight(color))

        # Creating bishops
        self.squares[row_other][2] = Square(row_other,2,Bishop(color))
        self.squares[row_other][5] = Square(row_other,5,Bishop(color))

        # Creating Rooks
        self.squares[row_other][0] = Square(row_other,0,Rook(color))
        self.squares[row_other][7] = Square(row_other,7,Rook(color))

        # Creating Queens
        self.squares[row_other][3] = Square(row_other,3,Queen(color))

        # Creating Kings
        self.squares[row_other][4] = Square(row_other,4,King(color))
    
    def _add_move(self, possible_moves, move_row, move_col, piece):
        if Square.in_range(move_row, move_col):
            if self.squares[move_row][move_col].is_empty():
                possible_moves.append((move_row, move_col))
                return True
            elif self.squares[move_row][move_col].has_enemy_piece(piece.color):
                possible_moves.append((move_row, move_col))
                return False
            else:
                return False
b = Board()