import pygame
import sys

from src.grid import GameGrid


class PygameEnvironment():
    def __init__(self, sx, sy, caption, mode=0) -> None:
        self.caption = caption
        self.sx = sx # Screen width
        self.sy = sy # Screen height

        self.running = True
        self.can_click = True

        pygame.init()
        pygame.display.set_caption(self.caption)
        self.s = pygame.display.set_mode((self.sx, self.sy)) # Pygame display
        self.bg = pygame.Surface((self.sx, self.sy)) # Background surface

        self.grid = GameGrid(self.s) # The grid object manages the tiles. It handles tile initialization, graphics, and has a grab function that returns a tile by inputted coordinate. 
        self.selection = None # Currently selected tile.

        while self.running == True:
            self.mainloop()

    def exit(self):
        self.running = False

    def mainloop(self):
        self.catch_events()
        self.get_input()
        
        self.game_logic()
        self.restrict_clicks()

        pygame.display.update()

    def catch_events(self): # Pygame template code. Close the window if the x is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit
                pygame.quit()
                self.exit()
                sys.exit()
                return

    def get_input(self): # Pygame input handlers 
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def restrict_clicks(self): # self.can_click restricts every handled mouse input/keystroke to call only once when pressed. The input must be released before another can be called.
        if pygame.mouse.get_pressed()[0] or self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN]or self.keys[pygame.K_SPACE]:
            self.can_click = False
        else: self.can_click = True 

    def game_logic(self):
        # Draw the background and tiles.
        self.s.blit(self.bg, [0,0])
        self.grid.draw_tiles()

        # This handles tile selection. When the mouse is clicked, check every tile for a collision and select if that's the case. Unselect any tiles that aren't colliding.
        if pygame.mouse.get_pressed()[0] and self.can_click == True:
            self.selection = None
            for tile in self.grid.active_tiles:
                tile.selected = False
                if tile.rect.collidepoint(self.mouse_pos):
                    tile.selected = True
                    self.selection = tile                    
            self.can_click = False
        
        # This handles tile movement/flipping. Tiles are grabbed/drawn by position on the 3x3 grid. 
        if self.selection != None:
            if self.can_click == True:
                if self.keys[pygame.K_LEFT]: 
                    if self.selection.pos[0] != 0:
                        self.selection.swap(self.grid.grab_tile([self.selection.pos[0]-1, self.selection.pos[1]]))
                    self.can_click = False
                elif self.keys[pygame.K_RIGHT]: 
                    if self.selection.pos[0] != 2:
                        self.selection.swap(self.grid.grab_tile([self.selection.pos[0]+1, self.selection.pos[1]]))
                    self.can_click = False
                elif self.keys[pygame.K_UP]: 
                    if self.selection.pos[1] != 0:
                        self.selection.swap(self.grid.grab_tile([self.selection.pos[0], self.selection.pos[1]-1]))
                    self.can_click = False
                elif self.keys[pygame.K_DOWN]: 
                    if self.selection.pos[1] != 2:
                        self.selection.swap(self.grid.grab_tile([self.selection.pos[0], self.selection.pos[1]+1]))
                    self.can_click = False

                elif self.keys[pygame.K_SPACE]: 
                    self.selection.flip()
                    self.can_click = False
                
                if self.can_click == False:
                    self.grid.update_gridstate()
        
if __name__ == '__main__':
    print(__file__)      
    PygameEnvironment(1000, 750, 'Shifting Stones', 0)
