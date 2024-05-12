import pygame, os
from pathlib import Path

def get_asset_path(filename):
    """
        Allow assets to be accessed from within the application instead of a static location in the
        filesystem. This allows the app to be run from anywhere
    """
    
    BASE_ASSET_DIR = os.path.dirname(__file__)[:-4] # Execution directory, with /src stripped
    return Path(os.path.join(BASE_ASSET_DIR, f'./res/{filename}')) # A platform-indpendant path to the asset

def load_images(tile_size=200):
    try:
        t0 = pygame.transform.scale(pygame.image.load('res/Sun_Tile.png'),    [tile_size, tile_size])
        t1 = pygame.transform.scale(pygame.image.load('res/Moon_Tile.png'),    [tile_size, tile_size]) 
        t2 = pygame.transform.scale(pygame.image.load('res/Fish_Tile.png'),    [tile_size, tile_size]) 
        t3 = pygame.transform.scale(pygame.image.load('res/Bird_Tile.png'),    [tile_size, tile_size]) 
        t4 = pygame.transform.scale(pygame.image.load('res/Unicorn_Tile.png'), [tile_size, tile_size]) 
        t5 = pygame.transform.scale(pygame.image.load('res/Boat_Tile.png'),    [tile_size, tile_size]) 
        t6 = pygame.transform.scale(pygame.image.load('res/Seed_Tile.png'),    [tile_size, tile_size]) 
        t7 = pygame.transform.scale(pygame.image.load('res/Tree_Tile.png'),    [tile_size, tile_size]) 

        next_turn = pygame.transform.smoothscale(pygame.image.load('res/NextTurnArrow.png'), [30,30]) 
        next_turn_hover = pygame.transform.smoothscale(pygame.image.load('res/NextTurnArrowHover.png'), [30,30]) 

        shadow = pygame.transform.scale(pygame.image.load('res/SquareDropShadow.png'),    [tile_size*1.3, tile_size*1.3]) 
        cardimg = pygame.transform.scale(pygame.image.load('res/CardImg.png'), [216,308]) 

        show_hint = pygame.transform.smoothscale(pygame.image.load('res/HintButtonImg.png'), [30,30]) 
        show_hint_hover = pygame.transform.smoothscale(pygame.image.load('res/HintButtonImgHover.png'), [30,30]) 

        flip_icon = pygame.transform.smoothscale(pygame.image.load('res/FlipIcon.png'), [tile_size/3, tile_size/3]) 
        swap_icon = pygame.transform.smoothscale(pygame.image.load('res/SwapIcon.png'), [tile_size/2, tile_size/4]) 

    except: 
        pygame.font.init()
        t0 = pygame.Surface((tile_size, tile_size))
        t1 = pygame.Surface((tile_size, tile_size))
        t2 = pygame.Surface((tile_size, tile_size))
        t3 = pygame.Surface((tile_size, tile_size))
        t4 = pygame.Surface((tile_size, tile_size))
        t5 = pygame.Surface((tile_size, tile_size))
        t6 = pygame.Surface((tile_size, tile_size))
        t7 = pygame.Surface((tile_size, tile_size))

        t0.fill('yellow')
        t1.fill('grey')
        t2.fill('orange')
        t3.fill('red')
        t4.fill('purple')
        t5.fill('cyan')
        t6.fill('white')
        t7.fill('green')

        next_turn = pygame.font.SysFont('Comic Sans MS', 20).render('->', True, 'white')
        next_turn_hover = pygame.font.SysFont('Comic Sans MS', 20).render('->', True, 'orange')

        shadow = pygame.Surface((0, 0))
        cardimg = pygame.Surface((216, 308))
        cardimg.fill([160, 140, 80])

        show_hint =  pygame.font.SysFont('Comic Sans MS', 20).render('?', True, 'white')
        show_hint_hover = pygame.font.SysFont('Comic Sans MS', 20).render('?', True, 'orange')

        flip_icon = pygame.font.SysFont('Comic Sans MS', 30).render('F', True, 'pink')
        swap_icon = pygame.font.SysFont('Comic Sans MS', 40).render('<--->', True, 'pink')
    
    t8 = pygame.Surface((tile_size, tile_size))
    t8.fill((0,0,0))
    t9 = pygame.Surface((tile_size, tile_size))
    t9.fill((50,50,50))
    return [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, next_turn, next_turn_hover, shadow, cardimg, show_hint, show_hint_hover, flip_icon, swap_icon]