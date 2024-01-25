import pygame, os
from pathlib import Path

from .card import Card

def get_asset_path(filename):
    """
        Allow assets to be accessed from within the application instead of a static location in the
        filesystem. This allows the app to be run from anywhere
    """
    
    BASE_ASSET_DIR = os.path.dirname(__file__)[:-4] # Execution directory, with /src stripped
    return Path(os.path.join(BASE_ASSET_DIR, f'./res/{filename}')) # A platform-indpendant path to the asset

class SunMoon(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'yellow'
        self.side_2 = 'grey'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load(get_asset_path('Sun_Tile.png')), [self.tile_size, self.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load(get_asset_path('Moon_Tile.png')), [self.tile_size, self.tile_size])
        except:
            self.img_1 = None
            self.img_2 = None

class FishBird(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'orange'
        self.side_2 = 'red'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load(get_asset_path('Fish_Tile.png')), [self.tile_size, self.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load(get_asset_path('Bird_Tile.png')), [self.tile_size, self.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None

class UnicornBoat(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'purple'
        self.side_2 = 'cyan'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load(get_asset_path('Unicorn_Tile.png')), [self.tile_size, self.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load(get_asset_path('Boat_Tile.png')), [self.tile_size, self.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None

class SeedTree(Card):
    def __init__(self) -> None:
        Card.__init__(self)
        self.side_1 = 'white'
        self.side_2 = 'green'
        try:
            self.img_1 = pygame.transform.scale(pygame.image.load(get_asset_path('Seed_Tile.png')), [self.tile_size, self.tile_size])
            self.img_2 = pygame.transform.scale(pygame.image.load(get_asset_path('Tree_Tile.png')), [self.tile_size, self.tile_size])
        except: 
            self.img_1 = None
            self.img_2 = None