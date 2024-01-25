import pygame
import random

class Slot():
    tile_size = 200
    
    def __init__(self, surf, x, y) -> None:
        self.x = x
        self.y = y
        self.surf = surf

        self.width = Slot.tile_size
        self.height = Slot.tile_size

        self.color = 'red'
        self.select_color = 'red'

        self.rect = pygame.draw.rect(self.surf, self.color, [self.x, self.y, self.width, self.height], 1)

        type = random.randint(0, 3)
        flip = random.randint(0,1)
        
        if type == 0:
            self.card = Faces_SunMoon()
        elif type == 1:
            self.card = Faces_FishBird()
        elif type == 2:
            self.card = Faces_SeedTree()
        elif type == 3:
            self.card = Faces_UnicornBoat()

        if flip == 0: self.card.flipped = False
        else: self.card.flipped = True

    def draw(self):
        self.rect = pygame.draw.rect(self.surf, self.color, [self.x, self.y, self.width, self.height], 1)
        if self.card != None:
            if self.card.flipped == False:
                pygame.draw.rect(self.surf, self.card.side_1, [self.x + 3, self.y + 3, self.width - 6, self.height - 6])
                if self.card.img_1 != None: self.surf.blit(self.card.img_1, [self.x, self.y])
            elif self.card.flipped == True:
                pygame.draw.rect(self.surf, self.card.side_2, [self.x + 3, self.y + 3, self.width - 6, self.height - 6])
                if self.card.img_2 != None: self.surf.blit(self.card.img_2, [self.x, self.y])

            if self.card.selected == True:
                pygame.draw.rect(self.surf, self.select_color, [self.x-5, self.y-5, self.width+10, self.height+10], 5, 5)

    def swap_right(self, grid):
        for row in range(3):
            for c in range(3):
                if grid[row][c] == self and grid[row][c] != grid[row][2]:
                    x = self.card
                    grid[row][c].card = grid[row][c+1].card
                    grid[row][c + 1].card = x
                    return grid
        return grid

    def swap_left(self, grid):
        for row in range(3):
            for c in range(3):
                if grid[row][c] == self and grid[row][c] != grid[row][0]:
                    x = self.card
                    grid[row][c].card = grid[row][c-1].card
                    grid[row][c - 1].card = x
                    return grid
        return grid

    def swap_up(self, grid):
        for row in range(3):
            for c in range(3):
                if grid[row][c] == self and grid[row][c] != grid[0][c]:
                    x = self.card
                    grid[row][c].card = grid[row-1][c].card
                    grid[row - 1][c].card = x
                    return grid
        return grid
    
    def swap_down(self, grid):
        for row in range(3):
            for c in range(3):
                if grid[row][c] == self and grid[row][c] != grid[2][c]:
                    x = self.card
                    grid[row][c].card = grid[row+1][c].card
                    grid[row + 1][c].card = x
                    return grid
        return grid
    
    def flip(self):
        if self.card.flipped == False:
            self.card.flipped = True
        else: self.card.flipped = False
        self.card.can_flip = False

    def logic(self, mouse_pos, keys, grid):
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if pygame.mouse.get_pressed()[0] == True:
                self.card.selected = True
        else:
            if pygame.mouse.get_pressed()[0] == True:
                self.card.selected = False
        
        if self.card.selected == True:
            if keys[pygame.K_SPACE]:
                if self.card.can_flip == True:
                    self.flip()
            else: self.card.can_flip = True

            if keys[pygame.K_LEFT]:
                if self.card.can_switch == True:
                    self.card.can_switch = False
                    grid = self.swap_left(grid)
                    
            elif keys[pygame.K_RIGHT]:
                if self.card.can_switch == True:
                    self.card.can_switch = False
                    grid = self.swap_right(grid)
                    
            elif keys[pygame.K_UP]:
                if self.card.can_switch == True:
                    self.card.can_switch = False
                    grid = self.swap_up(grid)
                    
            elif keys[pygame.K_DOWN]:
                if self.card.can_switch == True:
                    self.card.can_switch = False
                    grid = self.swap_down(grid)
                    
            else: self.card.can_switch = True
        return grid



class Card():
    def __init__(self) -> None:
        self.flipped = False
        self.selected = False
        self.can_flip = True
        self.can_switch = True

class Faces_SunMoon(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'yellow'
        self.side_2 = 'grey'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load('res/Sun_Tile.png'), [Slot.tile_size, Slot.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load('res/Moon_Tile.png'), [Slot.tile_size, Slot.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None

class Faces_FishBird(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'orange'
        self.side_2 = 'red'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load('res/Fish_Tile.png'), [Slot.tile_size, Slot.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load('res/Bird_Tile.png'), [Slot.tile_size, Slot.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None

class Faces_UnicornBoat(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'purple'
        self.side_2 = 'cyan'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load('res/Unicorn_Tile.png'), [Slot.tile_size, Slot.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load('res/Boat_Tile.png'), [Slot.tile_size, Slot.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None

class Faces_SeedTree(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'white'
        self.side_2 = 'green'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load('res/Seed_Tile.png'), [Slot.tile_size, Slot.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load('res/Tree_Tile.png'), [Slot.tile_size, Slot.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None


class PygameEnvironment():
    def __init__(self, sx, sy, caption, mode=0) -> None:
        self.caption = caption
        self.sx = sx
        self.sy = sy

        self.running = True
        self.can_click = True

        pygame.init()
        pygame.display.set_caption(self.caption)
        self.s = pygame.display.set_mode((self.sx, self.sy))
        self.bg = pygame.Surface((self.sx, self.sy))

        self.grid = []
        gx = Slot.tile_size
        gy = Slot.tile_size / 2
        
        for i in range(3): 
            self.grid.append([])
            for _ in range(3):
                self.grid[i].append(Slot(self.s, gx, gy))
                gx += Slot.tile_size + 10
            gx = Slot.tile_size
            gy += Slot.tile_size + 10

        while self.running == True:
            self.mainloop()

    def exit(self):
        self.running = False

    def mainloop(self):
        self.catch_events()
        self.get_input()
        self.restrict_clicks()
        self.game_logic()

        pygame.display.update()

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.exit()
                exit()
                return

    def get_input(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def restrict_clicks(self):
        if pygame.mouse.get_pressed()[0]:
            self.can_click = False
        else:
            self.can_click = True

    def game_logic(self):
        self.s.blit(self.bg, [0,0])
        for r in self.grid:
            for g_item in r:
                g_item.draw()
                self.grid = g_item.logic(self.mouse_pos, self.keys, self.grid)
            
            
PygameEnvironment(1000, 750, 'Shifting Stones', 0)
