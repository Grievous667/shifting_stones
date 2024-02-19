import pygame, random
from src.helper import load_images

class TileGrid():
    def __init__(self, pygame_surf) -> None:
        self.tile_choices = [[0,1], [2,3], [2,3], [4,5], [4,5], [4,5], [6,7], [6,7], [6,7]]
        self.gridstate = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.tile_size = 200
        self.tile_padding = 5
        self.tile_xoffset = 150
        self.tile_yoffset = -100
        
        self.tile_rects = dict()
        
        
        self.pygame_surf = pygame_surf
        self.images = load_images(self.tile_size)
        

        for y in range(3):
            for x in range(3): 
                self.tile_rects['['+str(x)+','+str(y)+']'] = pygame.Rect((x+1)*self.tile_size + (self.tile_padding*x) + self.tile_xoffset, (y+1)*self.tile_size + (self.tile_padding*y)+self.tile_yoffset, self.tile_size, self.tile_size)
                tiletype = random.randint(0, len(self.tile_choices)-1)
                tileflip = random.randint(0,1)
                self.gridstate[x][y] = self.tile_choices[tiletype][tileflip]
                self.tile_choices.remove(self.tile_choices[tiletype])
        

    def switch(self, tile1, tile2):
        temp = self.gridstate[tile1[1]][tile1[0]]
        self.gridstate[tile1[1]][tile1[0]] = self.gridstate[tile2[1]][tile2[0]]
        self.gridstate[tile2[1]][tile2[0]] = temp

    def flip(self, tile):
        if self.gridstate[tile[1]][tile[0]] % 2 == 0: self.gridstate[tile[1]][tile[0]] += 1
        else: self.gridstate[tile[1]][tile[0]] -= 1
        

    def draw_tiles(self):
        for x in range(3):
            for y in range(3):
                brect = [(x+1)*self.tile_size + (self.tile_padding*x) + self.tile_xoffset, (y+1)*self.tile_size + (self.tile_padding*y)+self.tile_yoffset, self.tile_size, self.tile_size]
                # pygame.draw.rect(self.pygame_surf, 'red', brect, 1)
                if   self.gridstate[y][x] == 0: self.pygame_surf.blit(self.images[0], brect)
                elif self.gridstate[y][x] == 1: self.pygame_surf.blit(self.images[1], brect)
                elif self.gridstate[y][x] == 2: self.pygame_surf.blit(self.images[2], brect)
                elif self.gridstate[y][x] == 3: self.pygame_surf.blit(self.images[3], brect)
                elif self.gridstate[y][x] == 4: self.pygame_surf.blit(self.images[4], brect)
                elif self.gridstate[y][x] == 5: self.pygame_surf.blit(self.images[5], brect)
                elif self.gridstate[y][x] == 6: self.pygame_surf.blit(self.images[6], brect)
                elif self.gridstate[y][x] == 7: self.pygame_surf.blit(self.images[7], brect)

    def highlight(self, tile):
        brect = [(tile[0]+1)*self.tile_size + (self.tile_padding*tile[0]) + self.tile_xoffset, (tile[1]+1)*self.tile_size + (self.tile_padding*tile[1])+self.tile_yoffset, self.tile_size, self.tile_size]
        pygame.draw.rect(self.pygame_surf, 'RED', brect, 5)


