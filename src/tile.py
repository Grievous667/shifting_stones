class Tile():
    tilelist = []
    tile_size = 200
    def __init__(self, subclass, pos=[0,0]) -> None:
        self.type = subclass()
        self.pos = pos
        self.flipped = False

        self.selected = False
        self.rect = None

    def swap(self, other_tile):
        pos_copy = self.pos
        self.pos = other_tile.pos
        other_tile.pos = pos_copy

    def flip(self):
        self.flipped = not self.flipped
        return self.flipped
        
