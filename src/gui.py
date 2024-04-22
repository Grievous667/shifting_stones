import pygame
import math
from random import randint 
from src.helper import load_images


class Button():
    def __init__(self, pygame_surf, pos, func, img, hover_img=None, size=30, tc='white', bc=None, bgc=None) -> None:
        self.pygame_surf = pygame_surf
        self.pos = pos
        self.func = func
        self.img = img
        self.hover_img = hover_img
        self.size = size
        self.tc = tc
        self.bc = bc
        self.bgc = bgc
        self.rect = pygame.draw.rect(self.pygame_surf, 'red', [self.pos[0], self.pos[1], self.size, self.size], 1)
    
    def draw(self):
        if self.bgc != None: pygame.draw.rect(self.pygame_surf, self.bgc, [self.pos[0], self.pos[1], self.size, self.size])
        if self.bc != None: pygame.draw.rect(self.pygame_surf, self.bc, [self.pos[0], self.pos[1], self.size, self.size], 1)
        self.pygame_surf.blit(self.img, [self.pos[0] + self.size/2- self.img.get_width()/2, self.pos[1]])

    def hover(self):
        if self.hover_img != None: self.pygame_surf.blit(self.hover_img, [self.pos[0] + self.size/2- self.hover_img.get_width()/2, self.pos[1]])

class CardGUI():

    # Lib key:
        # 0: Sun 
        # 1: Moon
        # 2: Fish
        # 3: Bird
        # 4: Horse
        # 5: Boat
        # 6: Seed
        # 7: Tree
        # 8: Null
        # 9: Required Space
    
    deck =  [
            [[[9, 9, 9], [9, 9, 9], [9, 9, 1]]] ,
            [[[9, 9, 3], [9, 9, 9], [5, 9, 9]]] ,
            [[[0, 9, 9], [9, 9, 9], [9, 9, 9]]] ,
            [[[9, 6, 9], [4, 9, 4], [9, 1, 9]]] ,
            [[[7, 9, 9], [9, 9, 9], [9, 9, 2]]] ,
            [[[9, 9, 9], [9, 3, 9], [9, 9, 9]]] ,
            [[[9, 6, 9], [9, 9, 9], [6, 9, 6]]] ,
            [[[9, 0, 9], [9, 9, 9], [3, 9, 3]]] ,
            [[[9, 9, 6], [9, 9, 9], [6, 9, 9]]] ,
            [[[4, 9, 7], [9, 9, 9], [6, 9, 5]]] ,
            [[[9, 7, 9], [2, 9, 2], [9, 5, 9]]] ,
            [[[9, 9, 9], [9, 2, 9], [9, 9, 9]]] ,
            [[[4, 9, 9], [9, 9, 9], [9, 9, 4]]] ,
            [[[1, 9, 9], [9, 2, 9], [9, 9, 2]]] ,
            [[[8, 8, 8], [7, 9, 6], [8, 8, 8]], [[7, 9, 6], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 9, 6]]] ,
            [[[8, 7, 8], [8, 7, 8], [8, 7, 8]], [[7, 8, 8], [7, 8, 8], [7, 8, 8]], [[8, 8, 7], [8, 8, 7], [8, 8, 7]]] ,
            [[[8, 2, 8], [8, 7, 8], [8, 4, 8]], [[2, 8, 8], [7, 8, 8], [4, 8, 8]], [[8, 8, 2], [8, 8, 7], [8, 8, 4]]] ,
            [[[8, 8, 8], [5, 9, 5], [8, 8, 8]], [[5, 9, 5], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [5, 9, 5]]] ,
            [[[8, 8, 8], [9, 9, 0], [8, 8, 8]], [[9, 9, 0], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [9, 9, 0]]] ,
            [[[8, 9, 8], [8, 9, 8], [8, 1, 8]], [[9, 8, 8], [9, 8, 8], [1, 8, 8]], [[8, 8, 9], [8, 8, 9], [8, 8, 1]]] ,
            [[[8, 8, 8], [1, 9, 9], [8, 8, 8]], [[1, 9, 9], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [1, 9, 9]]] ,
            [[[8, 8, 8], [7, 2, 5], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 2, 5]], [[7, 2, 5], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 7, 7], [8, 8, 8]], [[7, 7, 7], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 7, 7]]] ,
            [[[8, 8, 8], [4, 9, 4], [8, 8, 8]], [[4, 9, 4], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [4, 9, 4]]] ,
            [[[8, 8, 8], [6, 9, 7], [8, 8, 8]], [[6, 9, 7], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 9, 7]]] ,
            [[[8, 8, 8], [9, 4, 3], [8, 8, 8]], [[9, 4, 3], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [9, 4, 3]]] ,
            [[[8, 8, 8], [6, 6, 6], [8, 8, 8]], [[6, 6, 6], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 6, 6]]] ,
            [[[8, 5, 8], [8, 5, 8], [8, 5, 8]], [[5, 8, 8], [5, 8, 8], [5, 8, 8]], [[8, 8, 5], [8, 8, 5], [8, 8, 5]]] ,
            [[[8, 8, 8], [3, 9, 3], [8, 8, 8]], [[3, 9, 3], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [3, 9, 3]]] ,
            [[[8, 6, 8], [8, 9, 8], [8, 3, 8]], [[6, 8, 8], [9, 8, 8], [3, 8, 8]], [[8, 8, 6], [8, 8, 9], [8, 8, 3]]] ,
            [[[8, 2, 8], [8, 9, 8], [8, 2, 8]], [[2, 8, 8], [9, 8, 8], [2, 8, 8]], [[8, 8, 2], [8, 8, 9], [8, 8, 2]]] ,
            [[[8, 0, 8], [8, 9, 8], [8, 9, 8]], [[0, 8, 8], [9, 8, 8], [9, 8, 8]], [[8, 8, 0], [8, 8, 9], [8, 8, 9]]] ,
            [[[8, 8, 8], [4, 3, 6], [8, 8, 8]], [[4, 3, 6], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [4, 3, 6]]] ,
            [[[8, 2, 8], [8, 9, 8], [8, 7, 8]], [[2, 8, 8], [9, 8, 8], [7, 8, 8]], [[8, 8, 2], [8, 8, 9], [8, 8, 7]]] ,
            [[[9, 7, 8], [3, 9, 8], [8, 8, 8]], [[8, 9, 7], [8, 3, 9], [8, 8, 8]], [[8, 8, 8], [8, 9, 7], [8, 3, 9]], [[8, 8, 8], [9, 7, 8], [3, 9, 8]]] ,
            [[[9, 6, 8], [5, 9, 8], [8, 8, 8]], [[8, 9, 6], [8, 5, 9], [8, 8, 8]], [[8, 8, 8], [9, 6, 8], [5, 9, 8]], [[8, 8, 8], [8, 9, 6], [8, 5, 9]]] ,
            [[[4, 9, 8], [9, 2, 8], [8, 8, 8]], [[8, 4, 9], [8, 9, 2], [8, 8, 8]], [[8, 8, 8], [4, 9, 8], [9, 2, 8]], [[8, 8, 8], [8, 4, 9], [8, 9, 2]]] ,
            [[[7, 9, 8], [0, 7, 8], [8, 8, 8]], [[8, 7, 9], [8, 0, 7], [8, 8, 8]], [[8, 8, 8], [7, 9, 8], [0, 7, 8]], [[8, 8, 8], [8, 7, 9], [8, 0, 7]]] ,
            [[[7, 9, 8], [9, 4, 8], [8, 8, 8]], [[8, 7, 9], [8, 9, 4], [8, 8, 8]], [[8, 8, 8], [7, 9, 8], [9, 4, 8]], [[8, 8, 8], [8, 7, 9], [8, 9, 4]]] ,
            [[[9, 5, 8], [5, 1, 8], [8, 8, 8]], [[8, 9, 5], [8, 5, 1], [8, 8, 8]], [[8, 8, 8], [8, 9, 5], [8, 5, 1]], [[8, 8, 8], [9, 5, 8], [5, 1, 8]]] ,
            [[[8, 8, 8], [5, 4, 8], [8, 8, 8]], [[8, 8, 8], [8, 5, 4], [8, 8, 8]], [[5, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 5, 4], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [5, 4, 8]], [[8, 8, 8], [8, 8, 8], [8, 5, 4]]] ,
            [[[8, 5, 8], [8, 2, 8], [8, 8, 8]], [[5, 8, 8], [2, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 2]], [[8, 8, 8], [8, 5, 8], [8, 2, 8]], [[8, 8, 8], [5, 8, 8], [2, 8, 8]], [[8, 8, 5], [8, 8, 2], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 3, 8], [8, 8, 8]], [[7, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 7], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 7, 8], [8, 3, 8]], [[8, 8, 8], [7, 8, 8], [3, 8, 8]], [[8, 8, 8], [8, 8, 7], [8, 8, 3]]] ,
            [[[8, 5, 8], [8, 3, 8], [8, 8, 8]], [[5, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 5], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 5, 8], [8, 3, 8]], [[8, 8, 8], [5, 8, 8], [3, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 3]]] ,
            [[[8, 8, 8], [6, 2, 8], [8, 8, 8]], [[6, 2, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 2, 8]], [[8, 8, 8], [8, 8, 8], [8, 6, 2]], [[8, 8, 8], [8, 6, 2], [8, 8, 8]], [[8, 6, 2], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 3, 8], [8, 3, 8], [8, 8, 8]], [[3, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 3], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 3, 8], [8, 3, 8]], [[8, 8, 8], [8, 8, 3], [8, 8, 3]], [[8, 8, 8], [3, 8, 8], [3, 8, 8]]] ,
            [[[8, 1, 8], [8, 6, 8], [8, 8, 8]], [[1, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 1], [8, 8, 6], [8, 8, 8]], [[8, 8, 8], [8, 1, 8], [8, 6, 8]], [[8, 8, 8], [1, 8, 8], [6, 8, 8]], [[8, 8, 8], [8, 8, 1], [8, 8, 6]]] ,
            [[[8, 7, 8], [8, 4, 8], [8, 8, 8]], [[7, 8, 8], [4, 8, 8], [8, 8, 8]], [[8, 8, 7], [8, 8, 4], [8, 8, 8]], [[8, 8, 8], [8, 7, 8], [8, 4, 8]], [[8, 8, 8], [8, 8, 7], [8, 8, 4]], [[8, 8, 8], [7, 8, 8], [4, 8, 8]]] ,
            [[[8, 7, 8], [8, 6, 8], [8, 8, 8]], [[7, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 7], [8, 8, 6], [8, 8, 8]], [[8, 8, 8], [8, 7, 8], [8, 6, 8]], [[8, 8, 8], [8, 8, 7], [8, 8, 6]], [[8, 8, 8], [7, 8, 8], [6, 8, 8]]] ,
            [[[8, 4, 8], [8, 5, 8], [8, 8, 8]], [[4, 8, 8], [5, 8, 8], [8, 8, 8]], [[8, 8, 4], [8, 8, 5], [8, 8, 8]], [[8, 8, 8], [8, 4, 8], [8, 5, 8]], [[8, 8, 8], [8, 8, 4], [8, 8, 5]], [[8, 8, 8], [4, 8, 8], [5, 8, 8]]] ,
            [[[8, 8, 8], [7, 6, 8], [8, 8, 8]], [[7, 6, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 6, 8]], [[8, 8, 8], [8, 8, 8], [8, 7, 6]], [[8, 7, 6], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 7, 6], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 7, 8], [8, 8, 8]], [[2, 7, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [2, 7, 8]], [[8, 8, 8], [8, 8, 8], [8, 2, 7]], [[8, 2, 7], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 2, 7], [8, 8, 8]]] ,
            [[[8, 5, 8], [8, 5, 8], [8, 8, 8]], [[8, 8, 8], [8, 5, 8], [8, 5, 8]], [[5, 8, 8], [5, 8, 8], [8, 8, 8]], [[8, 8, 5], [8, 8, 5], [8, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 5]], [[8, 8, 8], [5, 8, 8], [5, 8, 8]]] ,
            [[[8, 8, 8], [5, 1, 8], [8, 8, 8]], [[8, 8, 8], [8, 5, 1], [8, 8, 8]], [[5, 1, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [5, 1, 8]], [[8, 5, 1], [8, 8, 8], [8, 8, 8]] ,[[8, 8, 8], [8, 8, 8], [8, 5, 1]]] ,
            [[[8, 8, 8], [0, 4, 8], [8, 8, 8]], [[0, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [0, 4, 8]], [[8, 8, 8], [8, 8, 8], [8, 0, 4]], [[8, 8, 8], [8, 0, 4], [8, 8, 8]], [[8, 0, 4], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [6, 5, 8], [8, 8, 8]], [[6, 5, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 5, 8]], [[8, 8, 8], [8, 8, 8], [8, 6, 5]], [[8, 6, 5], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 6, 5], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 5, 8], [8, 8, 8]], [[2, 5, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [2, 5, 8]], [[8, 8, 8], [8, 8, 8], [8, 2, 5]], [[8, 2, 5], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 2, 5], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 2, 8], [8, 8, 8]], [[2, 2, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [2, 2, 8]], [[8, 8, 8], [8, 2, 2], [8, 8, 8]], [[8, 2, 2], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 2, 2]]] ,
            [[[8, 3, 8], [8, 6, 8], [8, 8, 8]], [[8, 8, 3], [8, 8, 6], [8, 8, 8]], [[3, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 3, 8], [8, 6, 8]], [[8, 8, 8], [3, 8, 8], [6, 8, 8]], [[8, 8, 8], [8, 8, 3], [8, 8, 6]]] ,
            [[[8, 6, 8], [8, 7, 8], [8, 8, 8]], [[6, 8, 8], [7, 8, 8], [8, 8, 8]], [[8, 8, 6], [8, 8, 7], [8, 8, 8]], [[8, 8, 8], [8, 6, 8], [8, 7, 8]], [[8, 8, 8], [8, 8, 6], [8, 8, 7]], [[8, 8, 8], [6, 8, 8], [7, 8, 8]]] ,
            [[[8, 6, 8], [8, 6, 8], [8, 8, 8]], [[6, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 6], [8, 8, 6], [8, 8, 8]], [[8, 8, 8], [8, 6, 8], [8, 6, 8]], [[8, 8, 8], [8, 8, 6], [8, 8, 6]], [[8, 8, 8], [6, 8, 8], [6, 8, 8]]] ,
            [[[8, 5, 8], [8, 4, 8], [8, 8, 8]], [[8, 8, 5], [8, 8, 4], [8, 8, 8]], [[5, 8, 8], [4, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 5, 8], [8, 4, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 4]], [[8, 8, 8], [5, 8, 8], [4, 8, 8]]] ,
            [[[8, 2, 8], [8, 4, 8], [8, 8, 8]], [[2, 8, 8], [4, 8, 8], [8, 8, 8]], [[8, 8, 2], [8, 8, 4], [8, 8, 8]], [[8, 8, 8], [8, 2, 8], [8, 4, 8]], [[8, 8, 8], [8, 8, 2], [8, 8, 4]], [[8, 8, 8], [2, 8, 8], [4, 8, 8]]] ,
            [[[8, 8, 8], [4, 4, 8], [8, 8, 8]], [[4, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [4, 4, 8]], [[8, 8, 8], [8, 4, 4], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 4, 4]], [[8, 4, 4], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 0, 8], [8, 8, 8]], [[7, 8, 8], [0, 8, 8], [8, 8, 8]], [[8, 8, 7], [8, 8, 0], [8, 8, 8]], [[8, 8, 8], [8, 7, 8], [8, 0, 8]], [[8, 8, 8], [7, 8, 8], [0, 8, 8]], [[8, 8, 8], [8, 8, 7], [8, 8, 0]]] ,
            [[[8, 8, 8], [3, 4, 8], [8, 8, 8]], [[3, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [3, 4, 8]], [[8, 8, 8], [8, 3, 4], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 3, 4]], [[8, 3, 4], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 4, 8], [8, 8, 8]], [[7, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 4, 8]], [[8, 8, 8], [8, 7, 4], [8, 8, 8]], [[8, 7, 4], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 7, 4]]] ,
            [[[8, 8, 8], [7, 7, 8], [8, 8, 8]], [[7, 7, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 7, 8]], [[8, 8, 8], [8, 7, 7], [8, 8, 8]], [[8, 7, 7], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 7, 7]]] ,
            [[[8, 8, 8], [6, 7, 8], [8, 8, 8]], [[6, 7, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 7, 8]], [[8, 8, 8], [8, 6, 7], [8, 8, 8]], [[8, 6, 7], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 6, 7]]] ,
            [[[8, 5, 8], [8, 6, 8], [8, 8, 8]], [[5, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 5], [8, 8, 6], [8, 8, 8]], [[8, 8, 8], [8, 5, 8], [8, 6, 8]], [[8, 8, 8], [5, 8, 8], [6, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 6]]] ,
            [[[8, 8, 8], [4, 5, 8], [8, 8, 8]], [[4, 5, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [4, 5, 8]], [[8, 8, 8], [8, 4, 5], [8, 8, 8]], [[8, 4, 5], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [8, 4, 5]]] ,
                           ]
    
    def __init__(self, pygame_surf, coords=[50, 100]) -> None:
        self.turn_num  = 1
        self.last_skip = 0
        self.pygame_surf = pygame_surf
        self.card_img = load_images()[13]
        self.coords = coords
        self.xspacing = self.card_img.get_width()+20
        self.yspacing = self.card_img.get_height()+20
        self.cards = []

        for i in range(4): self.cards.append(Card(self.pygame_surf, self, CardGUI.deck[randint(0, len(CardGUI.deck)-1)], 1, self.coords))

    def cash(self, gridstate, selected_card):
        r_val = 0
        if selected_card.match(gridstate) == True:
            r_val = selected_card.point_val
            self.cards.remove(selected_card)
            self.turn_num += 1
            return r_val

        
        for card in self.cards:
            if card.match(gridstate) == True:
                r_val = card.point_val
                self.cards.remove(card)
                self.turn_num += 1
                break
        return r_val
                

    def next_turn(self, has_moved):
        cards_in_hand = len(self.cards)
        if cards_in_hand < 4:
            for i in range(4 - cards_in_hand):
                self.cards.append(Card(self.pygame_surf, self, CardGUI.deck[randint(0, len(CardGUI.deck)-1)], 1, self.coords))
            self.turn_num += 1
            return False

        elif (self.turn_num - self.last_skip) >= 1: 
            self.cards.append(Card(self.pygame_surf, self, CardGUI.deck[randint(0, len(CardGUI.deck)-1)], 1, self.coords))
            self.cards.append(Card(self.pygame_surf, self, CardGUI.deck[randint(0, len(CardGUI.deck)-1)], 1, self.coords))
            self.last_skip = self.turn_num + 1
            self.turn_num += 1
            return False
        elif has_moved == True:
            self.turn_num += 1
            return False

    def draw(self, gridstate, hovered_card):
        for card in self.cards:
            if card != None and card != hovered_card: 
                card.draw(len(self.cards))
                if card.match(gridstate): card.highlight_playable()

        if hovered_card != None:
            hovered_card.draw(len(self.cards))
            if hovered_card.match(gridstate): hovered_card.highlight_playable()




class Card():
    images = load_images(50)
    def __init__(self, pygame_surf, card_gui, target_card, point_val, coords, cso=-200) -> None:
        self.pygame_surf = pygame_surf
        self.padding = 2
        self.speed = 10
        self.card_gui = card_gui

        self.card_spawn_offset = cso
        self.coords = [coords[0] + self.card_spawn_offset, coords[1] + self.card_spawn_offset]
        self.current_coords = self.coords.copy()
        self.target_coords = self.coords.copy()

        self.img_size = 50
        self.error_margin = 10
        self.card_img = Card.images[13]
        self.xspacing = self.card_img.get_width()+20
        self.yspacing = self.card_img.get_height()
        self.target_card = target_card
        self.display_card = self.target_card[0]
        self.brect = pygame.rect.Rect(self.coords[0], self.coords[1], self.card_img.get_width(), self.card_img.get_height())
        self.point_val = point_val
        self.point_render = pygame.font.SysFont('Comic Sans MS', 40).render(str(point_val), True, "WHITE")
        

    def draw(self, num_cards):
        i = self.card_gui.cards.index(self)

        if len(self.card_gui.cards) <= 6:
            if   i <= 1: 
                self.target_coords = [self.coords[0]+(i%2*self.xspacing) - self.card_spawn_offset, self.coords[1] - self.card_spawn_offset]
            elif i <= 3: 
                self.target_coords = [self.coords[0]+(i%2*self.xspacing) - self.card_spawn_offset, self.coords[1]+(1*self.yspacing) - self.card_spawn_offset]
                if num_cards > 4: self.target_coords[1] = math.floor(self.target_coords[1]/1.7)
            elif i <= 5: 
                self.target_coords = [self.coords[0]+(i%2*self.xspacing) - self.card_spawn_offset, self.coords[1]+(2*self.yspacing) - self.card_spawn_offset]
                if num_cards > 4: self.target_coords[1] = math.floor(self.target_coords[1]/1.7)
            elif i <= 7: 
                self.target_coords = [self.coords[0]+(i%2*self.xspacing) - self.card_spawn_offset, self.coords[1]+(3*self.yspacing) - self.card_spawn_offset]
                if num_cards > 4: self.target_coords[1] = math.floor(self.target_coords[1]/1.7)
        
        elif len(self.card_gui.cards) > 6: 
            if   i <= 3: 
                self.target_coords = [self.coords[0]+((i%4*self.xspacing)/3) - self.card_spawn_offset, self.coords[1] - self.card_spawn_offset]
            elif i <= 7: 
                self.target_coords = [self.coords[0]+((i%4*self.xspacing)/3) - self.card_spawn_offset, self.coords[1]+(.3*self.yspacing) - self.card_spawn_offset]
            elif i <= 11: 
                self.target_coords = [self.coords[0]+((i%4*self.xspacing)/3) - self.card_spawn_offset, self.coords[1]+(.6*self.yspacing) - self.card_spawn_offset]
            elif i <= 15: 
                self.target_coords = [self.coords[0]+((i%4*self.xspacing)/3) - self.card_spawn_offset, self.coords[1]+(.9*self.yspacing) - self.card_spawn_offset]
            elif i > 15: 
                self.target_coords = [self.coords[0]+((i%4*self.xspacing)/3) - self.card_spawn_offset, self.coords[1]+(1.2*self.yspacing) - self.card_spawn_offset]


        
        speed = self.speed/2 + ((2*self.speed) * (abs(self.current_coords[0] - self.target_coords[0])/200))
        if abs(self.target_coords[0] - self.current_coords[0]) > self.error_margin: 
            if   self.current_coords[0] > self.target_coords[0]: self.current_coords[0] -= speed
            elif self.current_coords[0] < self.target_coords[0]: self.current_coords[0] += speed

        speed = self.speed/2 + ((2*self.speed) * (abs(self.current_coords[1] - self.target_coords[1])/200))
        if abs(self.target_coords[1] - self.current_coords[1]) > self.error_margin: 
            if   self.current_coords[1] > self.target_coords[1]: self.current_coords[1] -= speed
            elif self.current_coords[1] < self.target_coords[1]: self.current_coords[1] += speed
        
        self.pygame_surf.blit(self.card_img, self.current_coords)
        self.pygame_surf.blit(self.point_render, [self.current_coords[0]+self.card_img.get_width()/2-self.point_render.get_width()/2, self.current_coords[1]+10])
        self.brect = pygame.rect.Rect(self.current_coords[0], self.current_coords[1], self.card_img.get_width(), self.card_img.get_height())

        yoffset = 0
        for row in self.display_card:
            xoffset = 0
            for item in row:
                pos = [self.current_coords[0]+self.card_img.get_width()/2-(((self.img_size + self.padding)/2)*3) + xoffset, self.current_coords[1]+yoffset+100]
                if item == 0:   self.pygame_surf.blit(Card.images[0], pos)
                elif item == 1: self.pygame_surf.blit(Card.images[1], pos)
                elif item == 2: self.pygame_surf.blit(Card.images[2], pos)
                elif item == 3: self.pygame_surf.blit(Card.images[3], pos)
                elif item == 4: self.pygame_surf.blit(Card.images[4], pos)
                elif item == 5: self.pygame_surf.blit(Card.images[5], pos)
                elif item == 6: self.pygame_surf.blit(Card.images[6], pos)
                elif item == 7: self.pygame_surf.blit(Card.images[7], pos)
                elif item == 9: self.pygame_surf.blit(Card.images[9], pos)
                xoffset += self.img_size + self.padding
            yoffset += self.img_size + self.padding

    def match(self, gridstate):
        for accept_state in self.target_card:
            is_match = True
            for x in range(3):
                for y in range(3):
                    if accept_state[x][y] != 8 and accept_state[x][y] != 9:
                        if gridstate[x][y] != accept_state[x][y]: is_match = False
            if is_match == True: return True

    def highlight(self):
        pygame.draw.rect(self.pygame_surf, 'ORANGE', pygame.rect.Rect(self.current_coords[0], self.current_coords[1], self.card_img.get_width(), self.card_img.get_height()), 2)

    def highlight_playable(self):
        pygame.draw.rect(self.pygame_surf, 'GREEN', pygame.rect.Rect(self.current_coords[0], self.current_coords[1], self.card_img.get_width(), self.card_img.get_height()), 5)

        


class infoGUI():
    def __init__(self, pygame_surf, card_gui, pos, sx, sy) -> None:
        self.buttons = []
        self.pygame_surf = pygame_surf
        self.pos = pos
        self.left_margin = 200
        self.padding = 10
        self.font_size = 22
        self.element_spacing = 100
        self.tile_size = 75
        self.images = load_images(self.tile_size)
        self.sx = sx
        self.sy = sy

        self.card_gui = card_gui
        self.next_turn_b = Button(self.pygame_surf, [self.pos[0]+2, self.pos[1]+4], self.card_gui.next_turn, self.images[10], self.images[11], 35, 'white', None, None)
        self.buttons.append(self.next_turn_b)
        
        self.cards = 4
        self.points = 0
        self.total_moves = 0
        self.avg_moves = 0.0

    def draw(self, point_sum):

        if self.points != 0: self.avg_moves = (self.total_moves/self.points)
        
        pygame.draw.rect(self.pygame_surf, 'black',[self.pos[0]-self.padding, self.pos[1]-self.padding, self.sx+(self.padding*2), 50])
        pygame.draw.rect(self.pygame_surf, 'orange',[self.pos[0]-self.padding, self.pos[1]-self.padding, self.sx+(self.padding*2), 50], 1)

        self.next_turn_b.draw()
        
        self.moves_txt = pygame.font.SysFont(['Consolas', 'Lucida Console', 'sans'], self.font_size).render('Cards Remaining: ' + str(self.cards), True, 'white')
        self.pygame_surf.blit(self.moves_txt, [self.pos[0]  + self.left_margin, self.pos[1] + self.padding])

        self.points_txt = pygame.font.SysFont(['Consolas', 'Lucida Console', 'sans'], self.font_size).render('Points: ' + str(self.points), True, 'white')
        self.pygame_surf.blit(self.points_txt, [self.pos[0] + (1*self.element_spacing) + self.moves_txt.get_width() + self.left_margin, self.pos[1] + self.padding])

        self.avg_moves_txt = pygame.font.SysFont(['Consolas', 'Lucida Console', 'sans'], self.font_size).render('Average: ' + str(round(self.avg_moves, 2)), True, 'white')
        self.pygame_surf.blit(self.avg_moves_txt, [self.pos[0] + (2*self.element_spacing) + self.moves_txt.get_width() + self.points_txt.get_width()  + self.left_margin, self.pos[1] + self.padding])

        self.point_sum_txt = pygame.font.SysFont(['Consolas', 'Lucida Console', 'sans'], self.font_size).render('Point Sum: ' + str(point_sum), True, 'white')
        self.pygame_surf.blit(self.point_sum_txt, [self.pos[0] + (3*self.element_spacing) + self.moves_txt.get_width() + self.points_txt.get_width() + self.avg_moves_txt.get_width()  + self.left_margin, self.pos[1] + self.padding])

    
    

class TargetGUI():
    def __init__(self, pygame_surf, pos) -> None:
        self.buttons = []

        self.new_target()

        self.pygame_surf = pygame_surf
        self.pos = pos
        self.tile_size = 75
        self.padding = 5

        self.images = load_images(self.tile_size)
        self.target_text = pygame.font.SysFont('Comic Sans MS', 30).render('Target', True, 'white')

        self.next_turn_b = Button(self.pygame_surf, [(self.pos[0] - self.padding) + (self.tile_size*3+self.padding*4) - 40, self.pos[1] - 45], self.new_target, self.images[10], self.images[11], 30, 'white', None, None)
        self.buttons.append(self.next_turn_b)

    def match(self, gridstate):
        for accept_state in self.target_card:
            is_match = True
            for x in range(3):
                for y in range(3):
                    if accept_state[x][y] != 8 and accept_state[x][y] != 9:
                        if gridstate[x][y] != accept_state[x][y]: is_match = False
            if is_match == True: return True

    def new_target(self):
        self.target_card = self.target_lib[randint(0, len(self.target_lib)-1)]
        
    
        
    def draw(self):
        pygame.draw.rect(self.pygame_surf, 'black',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50])
        pygame.draw.rect(self.pygame_surf, 'orange',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50], 1)
        self.pygame_surf.blit(self.target_text, [(self.pos[0] - self.padding) + (self.tile_size*3+self.padding*4)/2 - (self.target_text.get_width()/2), self.pos[1] - 50])
        
        
        yoffset = 0
        xoffset = 0
        for row in self.target_card[0]:
            xoffset = 0
            for item in row:
                if item == 0:   self.pygame_surf.blit(self.images[0], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 1: self.pygame_surf.blit(self.images[1], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 2: self.pygame_surf.blit(self.images[2], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 3: self.pygame_surf.blit(self.images[3], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 4: self.pygame_surf.blit(self.images[4], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 5: self.pygame_surf.blit(self.images[5], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 6: self.pygame_surf.blit(self.images[6], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 7: self.pygame_surf.blit(self.images[7], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 8: self.pygame_surf.blit(self.images[8], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 9: self.pygame_surf.blit(self.images[9], [self.pos[0]+xoffset, self.pos[1]+yoffset])
                xoffset += self.tile_size + self.padding
            yoffset += self.tile_size + self.padding