import pygame, random

from .faces import *

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
            self.card = SunMoon()
        elif type == 1:
            self.card = FishBird()
        elif type == 2:
            self.card = SeedTree()
        elif type == 3:
            self.card = UnicornBoat()

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