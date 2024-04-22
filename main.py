# MRS: Shifting Stones GUI 
import os ; os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "T"
import pygame
import sys

from src.grid import TileGrid
from src.gui import infoGUI, CardGUI
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
        try:    self.bg = pygame.transform.scale(pygame.image.load('res/Game_Background.png'),  [1600, 880])  # Background surface
        except: self.bg = pygame.Surface((self.sx, self.sy))          # Background surface
        

        self.grid = TileGrid(self.s) # The grid object manages the tiles. It handles tile initialization, graphics, and has a grab function that returns a tile by inputted coordinate. 
        
        # self.target_gui = TargetGUI(self.s, [250,150]) # Code that manages the target tile 
        
        self.card_gui = CardGUI(self.s)
        self.info_gui = infoGUI(self.s, self.card_gui, [0,0], self.sx, self.sy)    # Code that manages displaying game information to the user
        self.predictor = Predictor()

        self.selection = None # Currently selected tile.
        self.card_selection = self.card_gui.cards[len(self.card_gui.cards)-1]
        self.point_sum = self.predictor.solve_target(self.grid.gridstate, self.card_selection.target_card)
        self.hovered_card = None
        self.has_moved = False

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
        if pygame.mouse.get_pressed()[0] or self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN] or self.keys[pygame.K_SPACE] or self.keys[pygame.K_F11] or self.keys[pygame.K_ESCAPE] or self.keys[pygame.K_RETURN]: self.can_click = False
        else: self.can_click = True

    def record_move(self, remove_this_card=None):
        if remove_this_card != None:      
            self.card_gui.cards.remove(remove_this_card)
            self.info_gui.total_moves += 1
        
        self.has_moved = True
        if len(self.card_gui.cards) == 0: 
            self.has_moved = self.card_gui.next_turn(self.has_moved) 

        self.card_selection = self.card_gui.cards[len(self.card_gui.cards)-1]
        self.hovered_card = None

        self.info_gui.cards = len(self.card_gui.cards)
        self.point_sum = self.predictor.solve_target(self.grid.gridstate, self.card_selection.target_card)

    def game_logic(self):
        # Draw the background and tiles.
        self.s.blit(self.bg, [0,0])
        self.grid.draw_tiles()

        self.info_gui.draw(self.point_sum)
        self.card_gui.draw(self.grid.gridstate, self.hovered_card)

        # Check for button collisions/clicks
        for button in self.info_gui.buttons:
            if button.rect.collidepoint(self.mouse_pos):
                button.hover()
                if pygame.mouse.get_pressed()[0] and self.can_click == True:
                    self.has_moved = button.func(self.has_moved)
                    self.info_gui.cards = len(self.card_gui.cards)
                    self.can_click = False
        
        #
        # USER INPUT 
        #
        
        if   self.keys[pygame.K_ESCAPE] and self.can_click == True: self.s = pygame.display.set_mode((self.sx, self.sy))       ; self.can_click = False   # Exit fullscreen
        elif self.keys[pygame.K_F11]    and self.can_click == True: self.s = pygame.display.set_mode((0,0), pygame.FULLSCREEN) ; self.can_click = False   # Set to fullscreen

        if self.card_gui.cards == [None,None,None,None]:
            self.has_moved = self.card_gui.next_turn(self.has_moved)
            self.card_selection = self.card_gui.cards[0]
        
        for card in self.card_gui.cards: 
            if card != None:
                if card.brect.collidepoint(self.mouse_pos):
                    self.hovered_card = card
                card.target_coords[0] = card.coords[0]
                card.target_coords[1] = card.coords[1]

        if self.hovered_card != None:
            if self.hovered_card.brect.collidepoint(self.mouse_pos):
                self.hovered_card.target_coords[0] = (self.hovered_card.coords[0] + self.hovered_card.speed*4 )
                self.hovered_card.target_coords[1] = (self.hovered_card.coords[1] - self.hovered_card.speed*2 )
                if pygame.mouse.get_pressed()[0] and self.can_click == True:
                        self.card_selection = self.hovered_card
                        self.point_sum = self.predictor.solve_target(self.grid.gridstate, self.card_selection.target_card)
                        self.can_click = False
            else: self.hovered_card = None
        
        

        # This handles tile selection. When the mouse is clicked, check every tile for a collision and select if that's the case. Unselect any tiles that aren't colliding.
        if pygame.mouse.get_pressed()[0] and self.can_click == True:
            for tile in self.grid.tile_rects:
                if self.grid.tile_rects[tile].collidepoint(self.mouse_pos):
                    self.selection = eval(tile)
                    break
                else: self.selection = None                
            self.can_click = False
        

        # This handles tile movement/flipping. Tiles are grabbed/drawn by position on the 3x3 grid. 
        if self.selection != None:
            self.grid.highlight(self.selection)
        if self.card_selection != None: 
            self.card_selection.highlight()
            if self.selection != None and self.can_click == True:

                # Switch selected tile left if valid
                if self.keys[pygame.K_LEFT]: 
                    if self.selection[0] != 0:
                        self.grid.switch(self.selection, [self.selection[0]-1, self.selection[1]]) ; self.selection[0] -= 1 
                        self.record_move(self.card_selection)
                    self.can_click = False

                # Switch selected tile right if valid
                elif self.keys[pygame.K_RIGHT]: 
                    if self.selection[0] != 2:
                        self.grid.switch(self.selection, [self.selection[0]+1, self.selection[1]]) ; self.selection[0] += 1 
                        self.record_move(self.card_selection)
                    self.can_click = False

                # Switch selected tile ip if valid
                elif self.keys[pygame.K_UP]: 
                    if self.selection[1] != 0:
                        self.grid.switch(self.selection, [self.selection[0], self.selection[1]-1]) ; self.selection[1] -= 1 
                        self.record_move(self.card_selection)
                    self.can_click = False 

                # Switch selected tile down if valid
                elif self.keys[pygame.K_DOWN]: 
                    if self.selection[1] != 2:
                        self.grid.switch(self.selection, [self.selection[0], self.selection[1]+1]) ; self.selection[1] += 1 
                        self.record_move(self.card_selection)
                    self.can_click = False

                # Flip the selected tile
                elif self.keys[pygame.K_SPACE]: 
                    self.grid.flip(self.selection)
                    self.record_move(self.card_selection)
                    self.can_click = False
        if self.can_click == True:
            if self.keys[pygame.K_RETURN]: 
                points = self.card_gui.cash(self.grid.gridstate, self.card_selection)
                if points > 0:
                    self.info_gui.points += points 
                    self.record_move()
                self.can_click = False



if __name__ == '__main__':
    print(__file__)      
    PygameEnvironment(1200, 750, 'Shifting Stones', 0)