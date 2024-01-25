import pygame, random
from .faces import *

class GameGrid():
    def __init__(self, pygame_surf) -> None:
        self.tile_size = Tile.tile_size
        self.tile_choices = [SunMoon, FishBird, FishBird, SeedTree, SeedTree, SeedTree, HorseBoat, HorseBoat, HorseBoat]
        self.active_tiles = []

        self.gridstate = [[None, None, None],[None, None, None],[None, None, None]]
        
        self.surf = pygame_surf

        for x in range(3):
            for y in range(3):
                tiletype = random.randint(0, len(self.tile_choices)-1)
                tileflip = random.randint(0,1)
                new_tile = Tile(self.tile_choices[tiletype], [x,y])
                new_tile.flipped = tileflip
                self.active_tiles.append(new_tile)
                self.tile_choices.remove(self.tile_choices[tiletype])
        self.update_gridstate()
        
    def update_gridstate(self):
        for tile in self.active_tiles:
            self.gridstate[tile.pos[0]][tile.pos[1]] = tile

    def draw_tiles(self):
        for tile in self.active_tiles:
            tile.rect = pygame.draw.rect(self.surf, 'red', [((tile.pos[0]+1)*Tile.tile_size) + (5*tile.pos[0]), ((tile.pos[1]+1)*Tile.tile_size) + (5*tile.pos[1])-100, Tile.tile_size, Tile.tile_size], 1)
            if tile.flipped == False:
                self.surf.blit(tile.type.upface, tile.rect)
            else: self.surf.blit(tile.type.downface, tile.rect)
            if tile.selected == True:
                pygame.draw.rect(self.surf, 'red', tile.rect, 5)

    def grab_tile(self, pos):
        for tile in self.active_tiles:
            if tile.pos == pos:
                return tile
