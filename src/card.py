class Card():
    tile_size = 200
    
    def __init__(self) -> None:
        self.flipped = False
        self.selected = False
        self.can_flip = True
        self.can_switch = True