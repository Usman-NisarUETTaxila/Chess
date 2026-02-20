import os

class Pieces:
    def __init__(self,name,color,value,texture=None,texture_rect=None):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False
        if color == 'white':
            self.value_sign = 1
        else:
            self.value_sign = -1
        self.value = value * self.value_sign
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self):
        self.texture = os.path.join(
            f"images/{self.color}_{self.name}.png"
        )
    def add_moves(self,move):
        self.moves.append(move)

class Pawn(Pieces):
    def __init__(self,color):
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1
        super().__init__('pawn',color,1.0)

class Knight(Pieces):
    def __init__(self,color):
        super().__init__('knight', color, 3.0)

class Bishop(Pieces):
    def __init__(self,color):
        super().__init__('bishop', color, 3.001)

class Rook(Pieces):
    def __init__(self,color):
        super().__init__('rook', color, 5.0)

class Queen(Pieces):
    def __init__(self,color):
        super().__init__('queen', color, 9.0)

class King(Pieces):
    def __init__(self,color):
        super().__init__('king', color, 10000.0)

