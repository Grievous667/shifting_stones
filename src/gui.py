import pygame
from random import randint 
from src.faces import *

class Button():
    def __init__(self, pygame_surf, pos, func, img, hover_img=None, size=30, tc='white', bc='orange', bgc='black') -> None:
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
        self.avg_moves = 0

    def draw(self):
        pygame.draw.rect(self.pygame_surf, 'black',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50])
        pygame.draw.rect(self.pygame_surf, 'orange',[self.pos[0] - self.padding, self.pos[1] - self.padding - 50, self.tile_size*3+self.padding*4, self.tile_size*3+self.padding*4 + 50], 1)
        
        self.moves_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Moves Remaining: ' + str(self.moves), True, 'white')
        self.pygame_surf.blit(self.moves_txt, [self.pos[0] + self.padding, self.pos[1] - 50])

        self.points_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Points: ' + str(self.points), True, 'white')
        self.pygame_surf.blit(self.points_txt, [self.pos[0] + self.padding, self.pos[1]])

        self.avg_moves_txt = pygame.font.SysFont('Comic Sans MS', 20).render('Average: ' + str(round(self.avg_moves, 2)), True, 'white')
        self.pygame_surf.blit(self.avg_moves_txt, [self.pos[0] + self.padding, self.pos[1]+50])
        

        
        

class TargetGUI():
    def __init__(self, pygame_surf, pos) -> None:
        self.buttons = []

        # Lib key:
        # 0: Required Spacing 
        # 1: Sun
        # 2: Moon
        # 3: Fish
        # 4: Bird
        # 5: Horse
        # 6: Boat
        # 7: Seed
        # 8: Tree
        # 9: Null
        self.translation_dict = {
            SunMoon: [1,2],
            FishBird: [3,4],
            HorseBoat: [5,6],
            SeedTree: [7,8],
        }
        self.target_lib = [[[[9, 9, 9],[6, 5, 9],[9, 9, 9]], [[9, 9, 9],[9, 6, 5],[9, 9, 9]], [[6, 5, 9],[9, 9, 9],[9, 9, 9]], [[9, 6, 5],[9, 9, 9],[9, 9, 9]], [[9, 9, 9],[9, 9, 9],[6, 5, 9]], [[9, 9, 9],[9, 9, 9],[9, 6, 6]]],
                           [[[5, 0, 9],[0, 3, 9],[9, 9, 9]], [[9, 5, 0],[9, 0, 3],[9, 9, 9]], [[9, 9, 9],[5, 0, 9],[0, 3, 9]], [[9, 9, 9],[9, 0, 5],[9, 0, 3]]],
                           [[[9, 6, 9], [9, 3, 9], [9, 9, 9]], [[6, 9, 9], [3, 9, 9], [9, 9, 9]], [[9, 9, 9], [9, 9, 6], [9, 9, 3]], [[9, 9, 9], [9, 6, 9], [9, 3, 9]], [[9, 9, 9], [6, 9, 9], [3, 9, 9]], [[9, 9, 6], [9, 9, 3], [9, 9, 9]]],
                           [[[0, 0, 0],[0, 0, 0],[0, 0, 2]]],
                           [[[0, 7, 0],[5, 0, 5],[0, 2, 0]]],
                           [[[8, 0, 0],[0, 0, 0],[0, 0, 3]]],
                           [[[0, 0, 0],[0, 4, 0],[0, 0, 0]]],
                           [[[0, 7, 0],[0, 0, 0],[7, 0, 7]]],
                           [[[0, 1, 0],[0, 0, 0],[4, 0, 4]]],
                           [[[9, 3, 9],[9, 8, 9],[9, 5, 9]], [[3, 9, 9],[8, 9, 9],[5, 9, 9]], [[9, 9, 3],[9, 9, 8],[9, 9, 5]]],
                           [[[9, 8, 9],[9, 4, 9],[9, 9, 9]], [[8, 9, 9],[4, 9, 9],[9, 9, 9]], [[9, 9, 8],[9, 9, 4],[9, 9, 9]], [[9, 9, 9],[9, 8, 9],[9, 4, 9]], [[9, 9, 9],[8, 9, 9],[4, 9, 9]], [[9, 9, 9],[9, 9, 8],[9, 9, 4]]],
                           [[[9, 6, 9],[9, 4, 9],[9, 9, 9]], [[6, 9, 9],[4, 9, 9],[9, 9, 9]], [[9, 9, 6],[9, 9, 4],[9, 9, 9]], [[9, 9, 9],[9, 6, 9],[9, 4, 9]], [[9, 9, 9],[6, 9, 9],[4, 9, 9]], [[9, 9, 9],[9, 9, 6],[9, 9, 4]]],
                           [[[9, 9, 9],[6, 0, 6],[9, 9, 9]], [[6, 0, 6],[9, 9, 9],[9, 9, 9]], [[9, 9, 9],[9, 9, 9],[6, 0, 6]]],
                           [[[0, 8, 9],[4, 0, 9],[9, 9, 9]], [[9, 0, 8],[9, 4, 0],[9, 9, 9]], [[9, 9, 9],[9, 0, 8],[9, 4, 0]], [[9, 9, 9],[0, 8, 9],[4, 0, 9]]],
                           [[[0, 7, 9],[6, 0, 9],[9, 9, 9]], [[9, 0, 7],[9, 6, 0],[9, 9, 9]], [[9, 9, 9],[0, 7, 9],[6, 0, 9]], [[9, 9, 9],[9, 0, 7],[9, 6, 0]]],
                           [[[8, 0, 9],[1, 8, 9],[9, 9, 9]], [[9, 8, 0],[9, 1, 8],[9, 9, 9]], [[9, 9, 9],[8, 0, 9],[1, 8, 9]], [[9, 9, 9],[9, 8, 0],[9, 1, 8]]],
                           [[[9, 9, 9],[7, 3, 9],[9, 9, 9]], [[7, 3, 9],[9, 9, 9],[9, 9, 9]], [[9, 9, 9],[9, 9, 9],[7, 3, 9]], [[9, 9, 9],[9, 9, 9],[9, 7, 3]], [[9, 9, 9],[9, 7, 3],[9, 9, 9]], [[9, 7, 3],[9, 9, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[5, 0, 5],[9, 9, 9]], [[5, 0, 5],[9, 9, 9],[9, 9, 9]], [[9, 9, 9],[9, 9, 9],[5, 0, 5]]],
                           [[[9, 4, 9],[9, 4, 9],[9, 9, 9]], [[4, 9, 9],[4, 9, 9],[9, 9, 9]], [[9, 9, 4],[9, 9, 4],[9, 9, 9]], [[9, 9, 9],[9, 4, 9],[9, 4, 9],], [[9, 9, 9],[9, 9, 4],[9, 9, 4]], [[9, 9, 9],[4, 9, 9],[4, 9, 9]]],
                           [[[9, 2, 9],[9, 7, 9],[9, 9, 9]], [[2, 9, 9],[7, 9, 9],[9, 9, 9]], [[9, 9, 2],[9, 9, 7],[9, 9, 9]], [[9, 9, 9],[9, 2, 9],[9, 7, 9]], [[9, 9, 9],[2, 9, 9],[7, 9, 9]], [[9, 9, 9],[9, 9, 2],[9, 9, 7]]],
                           [[[9, 9, 9],[8, 3, 6],[9, 9, 9]], [[9, 9, 9],[9, 9, 9],[8, 3, 6]], [[8, 3, 6],[9, 9, 9],[9, 9, 9]]],
                           [[[9, 8, 9],[9, 5, 9],[9, 9, 9]]],
                           [[[9, 8, 9],[9, 7, 9],[9, 9, 9]]],
                           [[[9, 5, 9],[9, 6, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[8, 0, 7],[9, 9, 9]]],
                           [[[9, 9, 9],[7, 0, 8],[9, 9, 9]]],

                           [[[8, 0, 9],[0, 5, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[8, 7, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[3, 8, 9],[9, 9, 9]]],
                           [[[9, 8, 9],[9, 8, 9],[9, 8, 9]]],
                           [[[9, 6, 9],[9, 6, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[6, 2, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[1, 5, 9],[9, 9, 9]]],

                           [[[9, 0, 9],[9, 0, 9],[9, 2, 9]]],
                           [[[9, 9, 9],[0, 0, 1],[9, 9, 9]]],
                           [[[0, 8, 0],[3, 0, 3],[0, 6, 0]]],
                           [[[9, 9, 9],[7, 6, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[3, 6, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[3, 3, 9],[9, 9, 9]]],
                           [[[9, 4, 9],[9, 7, 9],[9, 9, 9]]],
                           [[[9, 7, 9],[9, 8, 9],[9, 9, 9]]],
                           [[[9, 7, 9],[9, 7, 9],[9, 9, 9]]],
                           
                           [[[9, 6, 9],[9, 5, 9],[9, 9, 9]]],
                           [[[9, 3, 9],[9, 0, 9],[9, 8, 9]]],
                           [[[9, 3, 9],[9, 5, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[5, 5, 9],[9, 9, 9]]],
                           [[[9, 8, 9],[9, 1, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[4, 5, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[8, 5, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[0, 5, 4],[9, 9, 9]]],
                           [[[9, 9, 9],[8, 8, 9],[9, 9, 9]]],
                           [[[9, 3, 9],[9, 0, 9],[9, 3, 9]]],

                           [[[9, 9, 9],[7, 7, 7],[9, 9, 9]]],
                           [[[2, 0, 0],[0, 3, 0],[0, 0, 3]]],
                           [[[9, 9, 9],[7, 8, 9],[9, 9, 9]]],
                           [[[9, 7, 9],[9, 0, 9],[9, 4, 9]]],
                           [[[9, 9, 9],[8, 8, 8],[9, 9, 9]]],
                           [[[9, 6, 9],[9, 7, 9],[9, 9, 9]]],
                           [[[9, 9, 9],[4, 0, 4],[9, 9, 9]]],
                           [[[9, 9, 9],[5, 4, 7],[9, 9, 9]]],
                           [[[0, 6, 9],[6, 2, 9],[9, 9, 9]]],
                           [[[0, 0, 7],[0, 0, 0],[7, 0, 0]]],

                           [[[9, 6, 9],[9, 6, 9],[9, 6, 9]]],
                           [[[5, 0, 8],[0, 0, 0],[7, 0, 6]]],
                           [[[5, 0, 0],[0, 0, 0],[0, 0, 5]]],
                           [[[9, 1, 9],[9, 0, 9],[9, 0, 9]]],
                           [[[0, 0, 4],[0, 0, 0],[6, 0, 0]]],
                           [[[0, 0, 0],[0, 3, 0],[0, 0, 0]]],
                           [[[9, 9, 9],[2, 0, 0],[9, 9, 9]]],
                           [[[1, 0, 0],[0, 0, 0],[0, 0, 0]]],
                           [[[9, 9, 9],[5, 6, 9],[9, 9, 9]]],
                          
                           ]
        self.target_card = self.target_lib[randint(0, len(self.target_lib)-1)]
        
        self.pygame_surf = pygame_surf
        self.pos = pos
        self.tile_size = 75
        self.padding = 5

        self.load_images()
        self.target_text = pygame.font.SysFont('Comic Sans MS', 30).render('Target', True, 'white')

        self.new_card_b = Button(self.pygame_surf, [(self.pos[0] - self.padding) + (self.tile_size*3+self.padding*4) - 40, self.pos[1] - 45], self.new_target, self.reset_icon, self.reset_icon_hover, 30, 'white', None, None)
        self.buttons.append(self.new_card_b)

    def match(self, tilegrid):
        check_board = [[None, None, None],[None, None, None],[None, None, None]]
        for x in range(len(tilegrid)):
            for y in range(len(tilegrid[x])):
                if tilegrid[x][y][1] == True:
                    check_board[y][x] = (self.translation_dict[tilegrid[x][y][0]][1])
                else: check_board[y][x] = (self.translation_dict[tilegrid[x][y][0]][0])
        
        for accept_state in self.target_card:
            is_match = True
            for x in range(len(check_board)):
                for y in range(len(check_board[x])):
                    if accept_state[x][y] != 0 and accept_state[x][y] != 9:
                        if check_board[x][y] != accept_state[x][y]: is_match = False
            if is_match == True: return True

    def new_target(self):
        self.target_card = self.target_lib[randint(0, len(self.target_lib)-1)]

        
        
    def load_images(self):
        try:
            self.t1 = pygame.transform.scale(pygame.image.load('res/Sun_Tile.png'), [self.tile_size, self.tile_size])
            self.t2 = pygame.transform.scale(pygame.image.load('res/Moon_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t3 = pygame.transform.scale(pygame.image.load('res/Fish_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t4 = pygame.transform.scale(pygame.image.load('res/Bird_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t5 = pygame.transform.scale(pygame.image.load('res/Unicorn_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t6 = pygame.transform.scale(pygame.image.load('res/Boat_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t7 = pygame.transform.scale(pygame.image.load('res/Seed_Tile.png'), [self.tile_size, self.tile_size]) 
            self.t8 = pygame.transform.scale(pygame.image.load('res/Tree_Tile.png'), [self.tile_size, self.tile_size]) 

            self.reset_icon = pygame.transform.smoothscale(pygame.image.load('res/Reset_Icon.png'), [30,30]) 
            self.reset_icon_hover = pygame.transform.smoothscale(pygame.image.load('res/Reset_Icon_Hover.png'), [30,30]) 
        except: 
            self.t1 = pygame.Surface((self.tile_size, self.tile_size))
            self.t2 = pygame.Surface((self.tile_size, self.tile_size))
            self.t3 = pygame.Surface((self.tile_size, self.tile_size))
            self.t4 = pygame.Surface((self.tile_size, self.tile_size))
            self.t5 = pygame.Surface((self.tile_size, self.tile_size))
            self.t6 = pygame.Surface((self.tile_size, self.tile_size))
            self.t7 = pygame.Surface((self.tile_size, self.tile_size))
            self.t8 = pygame.Surface((self.tile_size, self.tile_size))

            self.t1.fill('yellow')
            self.t2.fill('grey')
            self.t3.fill('orange')
            self.t4.fill('red')
            self.t5.fill('purple')
            self.t6.fill('cyan')
            self.t7.fill('white')
            self.t8.fill('green')

            self.reset_icon = pygame.font.SysFont('Comic Sans MS', 20).render('R', True, 'white')
            self.reset_icon_hover = pygame.font.SysFont('Comic Sans MS', 20).render('R', True, 'cyan')
        
        self.t0 = pygame.Surface((self.tile_size, self.tile_size))
        self.t9 = pygame.Surface((self.tile_size, self.tile_size))
        self.t0.fill((50,50,50))
        self.t9.fill((0,0,0))
        
        
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
                if item == 0:   self.pygame_surf.blit(self.t0, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 1: self.pygame_surf.blit(self.t1, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 2: self.pygame_surf.blit(self.t2, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 3: self.pygame_surf.blit(self.t3, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 4: self.pygame_surf.blit(self.t4, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 5: self.pygame_surf.blit(self.t5, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 6: self.pygame_surf.blit(self.t6, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 7: self.pygame_surf.blit(self.t7, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 8: self.pygame_surf.blit(self.t8, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                elif item == 9: self.pygame_surf.blit(self.t9, [self.pos[0]+xoffset, self.pos[1]+yoffset])
                xoffset += self.tile_size + self.padding
            yoffset += self.tile_size + self.padding