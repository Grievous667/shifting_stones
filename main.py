import pygame
import sys

from src.grid import TileGrid
from src.gui import TargetGUI, infoGUI
from src.predictor import Predictor


class PygameEnvironment():
    def __init__(self, sx, sy, caption, mode=0) -> None:
        self.caption = caption
        self.sx = sx # Screen width
        self.sy = sy # Screen height

        self.running = True
        self.can_click = True

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.caption)
        self.s = pygame.display.set_mode((self.sx, self.sy)) # Pygame display

        try: pygame.display.set_icon(pygame.image.load('res/Moon_Tile.png'))  # Window Icon
        except: pass
        try: self.bg =  pygame.image.load('res/Game_Background.png')  # Background surface
        except: self.bg = pygame.Surface((self.sx, self.sy))          # Background surface
        

        self.grid = TileGrid(self.s) # The grid object manages the tiles. It handles tile initialization, graphics, and has a grab function that returns a tile by inputted coordinate. 
        
        self.target_gui = TargetGUI(self.s, [50,150]) # Code that manages the target tile 
        self.info_gui = infoGUI(self.s, [50,470])    # Code that manages displaying game information to the user
        self.predictor = Predictor()
        self.point_sum = self.predictor.solve_target(self.grid.gridstate, self.target_gui.target_card)

        self.selection = None # Currently selected tile.

        while self.running == True:
            self.mainloop()

    def exit(self): # Exit code
        self.running = False
        pygame.display.quit
        pygame.quit()
        sys.exit()
        
    def mainloop(self): # This code is iterated through on each program cycle. Everything that needs to be consistently executed should be here.
        self.catch_events()
        self.get_input()
        self.game_logic()
        self.restrict_clicks()
        pygame.display.update()

    def catch_events(self): # Pygame template code. Close the window if the x is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.exit()
                
    def get_input(self): # Pygame input handlers 
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def restrict_clicks(self): # self.can_click restricts every handled mouse input/keystroke to call only once when pressed. The input must be released before another can be called.
        if pygame.mouse.get_pressed()[0] or self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN]or self.keys[pygame.K_SPACE]: self.can_click = False
        else: self.can_click = True

    def record_move(self):
        self.info_gui.moves -= 1
        self.info_gui.total_moves += 1
        while self.target_gui.match(self.grid.gridstate):
            self.target_gui.new_target()
            self.info_gui.moves = 3
            self.info_gui.points += 1
            self.info_gui.avg_moves = self.info_gui.total_moves/self.info_gui.points
        self.point_sum = self.predictor.solve_target(self.grid.gridstate, self.target_gui.target_card)
         

    def game_logic(self):
        # Draw the background and tiles.
        self.s.blit(self.bg, [0,0])
        self.target_gui.draw()
        self.info_gui.draw(self.point_sum)
        self.grid.draw_tiles()

        for button in self.target_gui.buttons:
            if button.rect.collidepoint(self.mouse_pos):
                button.hover()
                if pygame.mouse.get_pressed()[0] and self.can_click == True:
                    self.target_gui.new_target()
                    self.info_gui.moves = 3
                    self.can_click = False
                    while self.target_gui.match(self.grid.gridstate):
                        self.target_gui.new_target()
                        self.info_gui.points += 1
                        self.info_gui.avg_moves = self.info_gui.total_moves/self.info_gui.points

        # This handles tile selection. When the mouse is clicked, check every tile for a collision and select if that's the case. Unselect any tiles that aren't colliding.
        if pygame.mouse.get_pressed()[0] and self.can_click == True:
            for tile in self.grid.tile_rects:
                if self.grid.tile_rects[tile].collidepoint(self.mouse_pos):
                    self.selection = eval(tile)
                    break
                else:
                    self.selection = None                
            self.can_click = False
        
        # This handles tile movement/flipping. Tiles are grabbed/drawn by position on the 3x3 grid. 
        if self.selection != None:
            self.grid.highlight(self.selection)
            if self.can_click == True:
                if self.keys[pygame.K_LEFT]: 
                    if self.selection[0] != 0:
                        self.grid.switch(self.selection, [self.selection[0]-1, self.selection[1]]) ; self.selection[0] -= 1
                        self.record_move()
                    self.can_click = False
                elif self.keys[pygame.K_RIGHT]: 
                    if self.selection[0] != 2:
                        self.grid.switch(self.selection, [self.selection[0]+1, self.selection[1]]) ; self.selection[0] += 1
                        self.record_move()
                    self.can_click = False
                elif self.keys[pygame.K_UP]: 
                    if self.selection[1] != 0:
                        self.grid.switch(self.selection, [self.selection[0], self.selection[1]-1]) ; self.selection[1] -= 1
                        self.record_move()
                    self.can_click = False
                elif self.keys[pygame.K_DOWN]: 
                    if self.selection[1] != 2:
                        self.grid.switch(self.selection, [self.selection[0], self.selection[1]+1]) ; self.selection[1] += 1
                        self.record_move()
                    self.can_click = False

                elif self.keys[pygame.K_SPACE]: 
                    self.grid.flip(self.selection)
                    self.record_move()
                    self.can_click = False


if __name__ == '__main__':
    print(__file__)      
    PygameEnvironment(1000, 750, 'Shifting Stones', 0)