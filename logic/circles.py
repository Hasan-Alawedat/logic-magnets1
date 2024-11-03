class Piece:
    def __init__(self, x, y, target_positions=None):
        self.x = x
        self.y = y
        self.target_positions = target_positions or []  

    def move(self, dx, dy):
        self.x += dx
        self.y += dy



class Red(Piece):
    def __init__(self, x, y, target_positions=None):
        super().__init__(x, y, target_positions)


class Purple(Piece):
    def __init__(self, x, y, target_positions=None):
        super().__init__(x, y, target_positions)


class Gray(Piece):
    def __init__(self, x, y, target_positions=None):
        super().__init__(x, y, target_positions)
