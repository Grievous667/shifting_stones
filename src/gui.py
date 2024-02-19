import pygame
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

class infoGUI():
    def __init__(self, pygame_surf, pos) -> None:
        self.buttons = []
        self.pygame_surf = pygame_surf
        self.pos = pos
        self.padding = 5
        self.tile_size = 75

        self.moves = 3
        self.points = 0
        self.total_moves = 0
        self.avg_moves = 0.0

    def draw(self, point_sum):
        pygame.draw.rect(self.pygame_surf, 'black',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50])
        pygame.draw.rect(self.pygame_surf, 'orange',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50], 1)
        
        self.moves_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Moves Remaining: ' + str(self.moves), True, 'white')
        self.pygame_surf.blit(self.moves_txt, [self.pos[0] + self.padding, self.pos[1] - 50])

        self.points_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Points: ' + str(self.points), True, 'white')
        self.pygame_surf.blit(self.points_txt, [self.pos[0] + self.padding, self.pos[1]])

        self.avg_moves_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Average: ' + str(round(self.avg_moves, 2)), True, 'white')
        self.pygame_surf.blit(self.avg_moves_txt, [self.pos[0] + self.padding, self.pos[1]+50])

        self.point_sum_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Point Sum: ' + str(point_sum), True, 'white')
        self.pygame_surf.blit(self.point_sum_txt, [self.pos[0] + self.padding, self.pos[1]+100])


class TargetGUI():
    def __init__(self, pygame_surf, pos) -> None:
        self.buttons = []

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

        self.target_lib = [
            #  [[[0, 2, 3], [4, 4, 5], [6, 8, 8]]] ,
            [[[8, 8, 8], [5, 4, 8], [8, 8, 8]], [[8, 8, 8], [8, 5, 4], [8, 8, 8]], [[5, 4, 8], [8, 8, 8], [8, 8, 8]], [[8, 5, 4], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [5, 4, 8]], [[8, 8, 8], [8, 8, 8], [8, 5, 5]]] ,
            [[[4, 9, 8], [9, 2, 8], [8, 8, 8]], [[8, 4, 9], [8, 9, 2], [8, 8, 8]], [[8, 8, 8], [4, 9, 8], [9, 2, 8]], [[8, 8, 8], [8, 9, 4], [8, 9, 2]]] ,
            [[[8, 5, 8], [8, 2, 8], [8, 8, 8]], [[5, 8, 8], [2, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 2]], [[8, 8, 8], [8, 5, 8], [8, 2, 8]], [[8, 8, 8], [5, 8, 8], [2, 8, 8]], [[8, 8, 5], [8, 8, 2], [8, 8, 8]]] ,
            [[[9, 9, 9], [9, 9, 9], [9, 9, 1]]] ,
            [[[9, 6, 9], [4, 9, 4], [9, 1, 9]]] ,
            [[[7, 9, 9], [9, 9, 9], [9, 9, 2]]] ,
            [[[9, 9, 9], [9, 3, 9], [9, 9, 9]]] ,
            [[[9, 6, 9], [9, 9, 9], [6, 9, 6]]] ,
            [[[9, 0, 9], [9, 9, 9], [3, 9, 3]]] ,
            [[[8, 2, 8], [8, 7, 8], [8, 4, 8]], [[2, 8, 8], [7, 8, 8], [4, 8, 8]], [[8, 8, 2], [8, 8, 7], [8, 8, 4]]] ,
            [[[8, 7, 8], [8, 3, 8], [8, 8, 8]], [[7, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 7], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 7, 8], [8, 3, 8]], [[8, 8, 8], [7, 8, 8], [3, 8, 8]], [[8, 8, 8], [8, 8, 7], [8, 8, 3]]] ,
            [[[8, 5, 8], [8, 3, 8], [8, 8, 8]], [[5, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 5], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 5, 8], [8, 3, 8]], [[8, 8, 8], [5, 8, 8], [3, 8, 8]], [[8, 8, 8], [8, 8, 5], [8, 8, 3]]] ,
            [[[8, 8, 8], [5, 9, 5], [8, 8, 8]], [[5, 9, 5], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [5, 9, 5]]] ,
            [[[9, 7, 8], [3, 9, 8], [8, 8, 8]], [[8, 9, 7], [8, 3, 9], [8, 8, 8]], [[8, 8, 8], [8, 9, 7], [8, 3, 9]], [[8, 8, 8], [9, 7, 8], [3, 9, 8]]] ,
            [[[9, 6, 8], [5, 9, 8], [8, 8, 8]], [[8, 9, 6], [8, 5, 9], [8, 8, 8]], [[8, 8, 8], [9, 6, 8], [5, 9, 8]], [[8, 8, 8], [8, 9, 6], [8, 5, 9]]] ,
            [[[7, 9, 8], [0, 7, 8], [8, 8, 8]], [[8, 7, 9], [8, 0, 7], [8, 8, 8]], [[8, 8, 8], [7, 9, 8], [0, 7, 8]], [[8, 8, 8], [8, 7, 9], [8, 0, 7]]] ,
            [[[8, 8, 8], [6, 2, 8], [8, 8, 8]], [[6, 2, 8], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [6, 2, 8]], [[8, 8, 8], [8, 8, 8], [8, 6, 2]], [[8, 8, 8], [8, 6, 2], [8, 8, 8]], [[8, 6, 2], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [4, 9, 4], [8, 8, 8]], [[4, 9, 4], [8, 8, 8], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [4, 9, 4]]] ,
            [[[8, 3, 8], [8, 3, 8], [8, 8, 8]], [[3, 8, 8], [3, 8, 8], [8, 8, 8]], [[8, 8, 3], [8, 8, 3], [8, 8, 8]], [[8, 8, 8], [8, 3, 8], [8, 3, 8]], [[8, 8, 8], [8, 8, 3], [8, 8, 3]], [[8, 8, 8], [3, 8, 8], [3, 8, 8]]] ,
            [[[8, 1, 8], [8, 6, 8], [8, 8, 8]], [[1, 8, 8], [6, 8, 8], [8, 8, 8]], [[8, 8, 1], [8, 8, 6], [8, 8, 8]], [[8, 8, 8], [8, 1, 8], [8, 6, 8]], [[8, 8, 8], [1, 8, 8], [6, 8, 8]], [[8, 8, 8], [8, 8, 1], [8, 8, 6]]] ,
            [[[8, 8, 8], [7, 2, 5], [8, 8, 8]], [[8, 8, 8], [8, 8, 8], [7, 2, 5]], [[7, 2, 5], [8, 8, 8], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 4, 8], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 6, 8], [8, 8, 8]]] ,
            [[[8, 4, 8], [8, 5, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 9, 6], [8, 8, 8]]] ,
            [[[8, 8, 8], [6, 9, 7], [8, 8, 8]]] ,
            [[[7, 9, 8], [9, 4, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 6, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 7, 8], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 7, 8], [8, 7, 8]]] ,
            [[[8, 5, 8], [8, 5, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [5, 1, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [0, 4, 8], [8, 8, 8]]] ,
            [[[8, 9, 8], [8, 9, 8], [8, 1, 8]]] ,
            [[[8, 8, 8], [9, 9, 0], [8, 8, 8]]] ,
            [[[9, 7, 9], [2, 9, 2], [9, 5, 9]]] ,
            [[[8, 8, 8], [6, 5, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 5, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [2, 2, 8], [8, 8, 8]]] ,
            [[[8, 3, 8], [8, 6, 8], [8, 8, 8]]] ,
            [[[8, 6, 8], [8, 7, 8], [8, 8, 8]]] ,
            [[[8, 6, 8], [8, 6, 8], [8, 8, 8]]] ,
            [[[8, 5, 8], [8, 4, 8], [8, 8, 8]]] ,
            [[[8, 2, 8], [8, 9, 8], [8, 7, 8]]] ,
            [[[8, 2, 8], [8, 4, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [4, 4, 8], [8, 8, 8]]] ,
            [[[8, 7, 8], [8, 0, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [3, 4, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 4, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [9, 4, 3], [8, 8, 8]]] ,
            [[[8, 8, 8], [7, 7, 8], [8, 8, 8]]] ,
            [[[8, 2, 8], [8, 9, 8], [8, 2, 8]]] ,
            [[[8, 8, 8], [6, 6, 6], [8, 8, 8]]] ,
            [[[1, 9, 9], [9, 2, 9], [9, 9, 2]]] ,
            [[[8, 8, 8], [6, 7, 8], [8, 8, 8]]] ,
            [[[8, 6, 8], [8, 9, 8], [8, 3, 8]]] ,
            [[[8, 8, 8], [7, 7, 7], [8, 8, 8]]] ,
            [[[8, 5, 8], [8, 6, 8], [8, 8, 8]]] ,
            [[[8, 8, 8], [3, 9, 3], [8, 8, 8]]] ,
            [[[8, 8, 8], [4, 3, 6], [8, 8, 8]]] ,
            [[[9, 5, 8], [5, 1, 8], [8, 8, 8]]] ,
            [[[9, 9, 6], [9, 9, 9], [6, 9, 9]]] ,
            [[[8, 5, 8], [8, 5, 8], [8, 5, 8]]] ,
            [[[4, 9, 7], [9, 9, 9], [6, 9, 5]]] ,
            [[[4, 9, 9], [9, 9, 9], [9, 9, 4]]] ,
            [[[8, 0, 8], [8, 9, 8], [8, 9, 8]]] ,
            [[[9, 9, 3], [9, 9, 9], [5, 9, 9]]] ,
            [[[9, 9, 9], [9, 2, 9], [9, 9, 9]]] ,
            [[[8, 8, 8], [1, 9, 9], [8, 8, 8]]] ,
            [[[0, 9, 9], [9, 9, 9], [9, 9, 9]]] ,
            [[[8, 8, 8], [4, 5, 8], [8, 8, 8]]] ,
                           ]

        self.new_target()

        self.pygame_surf = pygame_surf
        self.pos = pos
        self.tile_size = 75
        self.padding = 5

        self.images = load_images(self.tile_size)
        self.target_text = pygame.font.SysFont('Comic Sans MS', 30).render('Target', True, 'white')

        self.new_card_b = Button(self.pygame_surf, [(self.pos[0] - self.padding) + (self.tile_size*3+self.padding*4) - 40, self.pos[1] - 45], self.new_target, self.images[10], self.images[11], 30, 'white', None, None)
        self.buttons.append(self.new_card_b)

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
        self.new_card_b.draw()
        
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