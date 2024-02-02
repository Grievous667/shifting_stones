import pygame, os
from pathlib import Path

from .tile import Tile

def get_asset_path(filename):
    """
        Allow assets to be accessed from within the application instead of a static location in the
        filesystem. This allows the app to be run from anywhere
    """
    
    BASE_ASSET_DIR = os.path.dirname(__file__)[:-4] # Execution directory, with /src stripped
    return Path(os.path.join(BASE_ASSET_DIR, f'./res/{filename}')) # A platform-indpendant path to the asset


class SunMoon():
    def __init__(self) -> None:
        try:
            self.upface = pygame.transform.scale(pygame.image.load('res/Sun_Tile.png'), [Tile.tile_size, Tile.tile_size])
            self.downface = pygame.transform.scale(pygame.image.load('res/Moon_Tile.png'), [Tile.tile_size, Tile.tile_size])
        except:
            self.upface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.downface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.upface.fill('yellow')
            self.downface.fill('grey')

class FishBird():
    def __init__(self) -> None:
        try:
            self.upface = pygame.transform.scale(pygame.image.load('res/Fish_Tile.png'), [Tile.tile_size, Tile.tile_size])
            self.downface = pygame.transform.scale(pygame.image.load('res/Bird_Tile.png'), [Tile.tile_size, Tile.tile_size])
        except:
            self.upface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.downface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.upface.fill('orange')
            self.downface.fill('red')

class HorseBoat():
    def __init__(self) -> None:
        try:
            self.upface = pygame.transform.scale(pygame.image.load('res/Unicorn_Tile.png'), [Tile.tile_size, Tile.tile_size])
            self.downface = pygame.transform.scale(pygame.image.load('res/Boat_Tile.png'), [Tile.tile_size, Tile.tile_size])
        except:
            self.upface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.downface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.upface.fill('purple')
            self.downface.fill('cyan')

class SeedTree():
    def __init__(self) -> None:
        try:
            self.upface = pygame.transform.scale(pygame.image.load('res/Seed_Tile.png'), [Tile.tile_size, Tile.tile_size])
            self.downface = pygame.transform.scale(pygame.image.load('res/Tree_Tile.png'), [Tile.tile_size, Tile.tile_size])
        except:
            self.upface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.downface = pygame.Surface((Tile.tile_size, Tile.tile_size))
            self.upface.fill('white')
            self.downface.fill('green')