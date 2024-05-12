# MRS: Shifting Stones GUI 
# Code by Luke Becker and Ryan Smith
# 5/11/2024
# This program is a digital representation of the Shifting Stones board game, written with Pygame. It was designed to assist in mathematically understanding the game, 
#   and includes an algorithm to suggest optimal play to the user. 

import pygame # Pygame is the main library used for graphics and logic
import sys # System is imported strictly to assist in exit procedure

from src.grid import TileGrid # Helper class for the grid logic. Handles many of the graphical elements 
from src.gui import infoGUI, CardGUI # Helper classes for displaying meta information to the user
from src.predictor import Predictor # Helper class which contains prediction functions for determining optimal play
from win32api import GetSystemMetrics # This is imported to support fullscreen logic


class PygameEnvironment(): # Pygame window instance. All game is called from within this class's mainloop
    def __init__(self, sx, sy, caption, mode=0) -> None:
        self.caption = caption # Window title
        self.sx = sx # Screen width
        self.sy = sy # Screen height

        self.running = True # Boolean value: true if program should run, false if program should terminate
        self.can_click = True # Boolean value: true if the user can input legally, false if not. This is used prevent held keys triggering multiple times. 

        pygame.init() # Initialize pygame
        pygame.font.init() # Initialize pygame fonts 
        pygame.display.set_caption(self.caption) # Set the window caption
        self.s = pygame.display.set_mode((self.sx, self.sy)) # Main pygame display object

        
        try: pygame.display.set_icon(pygame.image.load('res/Moon_Tile.png'))  # Try to set window icon
        except: pass

        try:    self.bg = pygame.transform.scale(pygame.image.load('res/Game_Background.png'),  [1600, 880])  # Try to set background surface
        except: self.bg = pygame.Surface((self.sx, self.sy)) # Else draw a generic background
        

        self.grid = TileGrid(self.s) # The grid object manages the tiles. It handles tile initialization, graphics, and has a grab function that returns a tile by inputted coordinate. 
        self.card_gui = CardGUI(self.s) # The card gui manages the game cards. It handles draw logic, discard logic, point cashing, etc. 
        self.info_gui = infoGUI(self.s, self.card_gui, [0,0], self.sx, self.sy) # Code that manages displaying game information to the user
        self.predictor = Predictor() # This contains prediction functions. 

        self.tile_selection = None # Currently selected tile. Highlighted orange. 
        self.card_selection = self.card_gui.cards[0] # Target card being played. Highlighted orange.
        self.discard_selection = self.card_gui.cards[len(self.card_gui.cards)-1] # Target card to discard next. Highlighted red.

        self.get_move_solution() # Inital call sets point sum to the correct value and returns an optimal moveset 
        
        self.display_hint = False # Hint overlay is shown when true, hidden when false
        self.hovered_card = None # If a card is hovered, it is selected when clicked and brought to the front of other cards. This is a necessary logic check, because cards can have overlapping hitboxes. The first card hovered is prioritized.
        self.has_moved = True   # Boolean to record if the user can draw two extra cards or not
        self.fullscreen = False # Display in fullscreen if true, windowed if false.  

        # Main gameloop
        while self.running == True:
            self.mainloop() 

    def exit(self): # Exit code
        self.running = False
        pygame.display.quit
        pygame.quit()
        sys.exit()
        
    def mainloop(self): # This code is iterated through on each program cycle. Everything that needs to be consistently executed should be here.
        self.catch_events() # Handles pygame exit event.
        self.get_input() # Detects user input.
        self.game_logic() # Runs the graphical and logic components of the game
        self.restrict_clicks() # Prevents input spam. 
        pygame.display.update() # Updates the pygame window. 

    def catch_events(self): # Pygame template code. Close the window if the x is clicked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.exit()
                
    def get_input(self): # Pygame input handlers 
        self.keys = pygame.key.get_pressed() # Detects all keystrokes 
        self.mouse_pos = pygame.mouse.get_pos() # Updates mouse position

    def restrict_clicks(self): # self.can_click restricts every handled mouse input/keystroke to call only once when pressed. The input must be released before another can be called.
        if pygame.mouse.get_pressed()[0] or self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN] or self.keys[pygame.K_SPACE] or self.keys[pygame.K_F11] or self.keys[pygame.K_ESCAPE] or self.keys[pygame.K_RETURN]: self.can_click = False
        else: self.can_click = True

    def cash_card(self) -> int: # Cash in a matched card for points
        points = 0 # How many points to give the user. Set to zero initially in case there is no valid card to cash.
        if self.card_selection.match(self.grid.gridstate): # Check the selected card first and cash if valid
            points = self.card_selection.point_val
            self.card_gui.cards.remove(self.card_selection)
        else: # Otherwise, sheck every card and cash the first valid. If none, nothing happens.
            for card in self.card_gui.cards:
                if card.match(self.grid.gridstate):
                    points = card.point_val
                    self.card_gui.cards.remove(card)
                    break
        
        if len(self.card_gui.cards) == 0: # If the last card in the player's hand was cashed, end the turn and draw new cards.
            self.end_turn()
        else: # Otherwise, check that card selections are legal. Selection prefers first slot, discard selection prefers last slot. 
            if self.card_selection not in self.card_gui.cards: self.card_selection = self.card_gui.cards[0]
            if self.discard_selection not in self.card_gui.cards: self.discard_selection = self.card_gui.cards[len(self.card_gui.cards)-1]
        self.hovered_card = None # Reset hover to prevent hover logic calling a card that was cashed.
        self.get_move_solution() # Get a new optimal path and point sum 

        if points != 0: self.has_moved = True # Allow the user to draw more cards if they cash a card
        return points # Return points of cashed card

    def play_card(self): # Discard the discard selection to move
        self.card_gui.cards.remove(self.discard_selection) # Outer logic ensures discard selection is always in cardlist
        if self.discard_selection == self.card_selection and len(self.card_gui.cards) > 0: self.card_selection = self.card_gui.cards[0] # If the card selection was discarded, reset it
        if   len(self.card_gui.cards) == 0: # If the last card was discarded, end turn and handle logic there
            self.end_turn() 
        elif len(self.card_gui.cards) == 1: # If there's one card remaining, that has to be the discard selection. 
            self.discard_selection = self.card_gui.cards[0]
        elif len(self.card_gui.cards) > 1: # Otherwise, iterate from the back of the list to find the first card that isn't the target selection 
            cards = self.card_gui.cards.copy()
            cards.reverse()
            for card in cards:
                if card != self.card_selection: self.discard_selection = card ; break 
        
        self.has_moved = True # Allow player to draw two after moving 
        self.hovered_card = None # Reset card hover to prevent bad call
        self.record_move() # Record that the move happened and get a new solution

    def end_turn(self): # End turn and draw up to four cards. Also handles the draw two logic 
        if self.has_moved == True:
            self.info_gui.turn_num += 1

        if self.info_gui.num_cards < 4: # If less than four cards, draw up to four. Reset selections.
            self.card_gui.draw_up_to_four() 
            self.card_selection = self.card_gui.cards[0]
            self.discard_selection = self.card_gui.cards[len(self.card_gui.cards)-1]
            self.info_gui.num_cards = len(self.card_gui.cards)
        
        elif self.info_gui.turn_num > self.info_gui.last_skip + 1: # If legal, draw two extra cards and skip turn. 
            self.draw_cards()

    def draw_cards(self): # Draw two if legal. Set discard selection to last.  
        if self.has_moved == True:
            self.card_gui.draw_two()
            self.info_gui.last_skip = self.info_gui.turn_num 
            self.has_moved = False
            self.discard_selection = self.card_gui.cards[len(self.card_gui.cards)-1]
        self.info_gui.num_cards = len(self.card_gui.cards)

    def get_move_solution(self): # Solve the selected target card. 
        solutions = self.predictor.solve_target(self.grid.gridstate, self.card_selection.target_card)
        self.point_sum = solutions[0]
        self.best_pathset = solutions[1]
        self.best_flipset = solutions[2]

    def record_move(self): # Get a new solution and handle internal turn number logic. This is not for the end user, but instead determines when a turn can be exchanged for two cards. 
        self.get_move_solution()
        self.info_gui.total_moves += 1
        self.info_gui.num_cards = len(self.card_gui.cards)

    def game_logic(self): # Handles most of the game graphics and logic
        self.s.blit(self.bg, [0,0]) # Draw the background
        self.grid.draw_tiles() # Draw the tilegrid 

        self.info_gui.draw(self.point_sum) # Draw the info gui at the top of the screen 
        self.card_gui.draw(self.grid.gridstate, self.hovered_card) # Draw the card gui 

        if self.display_hint == True: # Overlay the optimal moveset onto the grid if true
            self.grid.draw_hint(self.best_pathset, self.best_flipset)

        
        #
        # BUTTONS 
        #

        # Check for button collisions/clicks
        for button in self.info_gui.buttons:
            if button.rect.collidepoint(self.mouse_pos):
                button.hover() # Highlight if hovered
                if pygame.mouse.get_pressed()[0] and self.can_click == True: # Left click 
                    if button.name == "NextTurn": # End Turn button
                        self.end_turn() 
                    elif button.name == "ShowHint": # Hint button
                        self.display_hint = not self.display_hint
                    self.can_click = False # Restrict to one input
        
        #
        # FULLSCREEN 
        #

        if self.keys[pygame.K_ESCAPE] and self.can_click == True and self.fullscreen == True:  # Exit fullscreen if ESC is pressed
            
            # Reset display size to initial parameters 
            self.s = pygame.display.set_mode((self.sx, self.sy)) 
            self.info_gui.sx = self.sx
            self.info_gui.sy = self.sy

            # Move elements to appropriate position 
            self.card_gui.coords[0] -= (GetSystemMetrics(0) - self.sx)/2
            self.card_gui.coords[1] -= (GetSystemMetrics(1) - self.sy)/2
            self.grid.pos[0]        -= (GetSystemMetrics(0) - self.sx)/2
            self.grid.pos[1]        -= (GetSystemMetrics(1) - self.sy)/2
            self.grid.update_rects()

            for card in self.card_gui.cards: 
                card.target_coords[0]  -= (GetSystemMetrics(0) - self.sx)/2
                card.coords[0]         -= (GetSystemMetrics(0) - self.sx)/2
                card.current_coords[0] -= (GetSystemMetrics(0) - self.sx)/2

                card.target_coords[1]  -= (GetSystemMetrics(1) - self.sy)/2
                card.coords[1]         -= (GetSystemMetrics(1) - self.sy)/2
                card.current_coords[1] -= (GetSystemMetrics(1) - self.sy)/2

            self.fullscreen = False
            self.can_click = False   

        elif self.keys[pygame.K_F11]    and self.can_click == True and self.fullscreen == False:  # Set to fullscreen if F11 is presssed 

            # Set display mode to fullscreen 
            self.s = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
            self.info_gui.sx = GetSystemMetrics(0)
            self.info_gui.sy = GetSystemMetrics(1)

            # Move elements to appropriate position 
            self.card_gui.coords[0] += (GetSystemMetrics(0) - self.sx)/2
            self.card_gui.coords[1] += (GetSystemMetrics(1) - self.sy)/2
            self.grid.pos[0]    += (GetSystemMetrics(0) - self.sx)/2
            self.grid.pos[1]    += (GetSystemMetrics(1) - self.sy)/2
            self.grid.update_rects()
            
            for card in self.card_gui.cards: 
                card.target_coords[0]  += (GetSystemMetrics(0) - self.sx)/2
                card.coords[0]         += (GetSystemMetrics(0) - self.sx)/2
                card.current_coords[0] += (GetSystemMetrics(0) - self.sx)/2

                card.target_coords[1]  += (GetSystemMetrics(1) - self.sy)/2
                card.coords[1]         += (GetSystemMetrics(1) - self.sy)/2
                card.current_coords[1] += (GetSystemMetrics(1) - self.sy)/2

            self.fullscreen = True
            self.can_click = False   

        #
        # TARGET CARDS  
        #
        
        # Check if a card is hovered and tag it if case. If not, set them to move to their initial position.
        for card in self.card_gui.cards: 
            if card != None:
                if card.brect.collidepoint(self.mouse_pos):
                    self.hovered_card = card
                card.target_coords[0] = card.coords[0]
                card.target_coords[1] = card.coords[1]

        if self.hovered_card != None: # If a card is hovered, offset its position a bit and allow selection logic. Deselect if mouse pos leaves. 
            if self.hovered_card.brect.collidepoint(self.mouse_pos):
                self.hovered_card.target_coords[0] = (self.hovered_card.coords[0] + self.hovered_card.speed*4 )
                self.hovered_card.target_coords[1] = (self.hovered_card.coords[1] - self.hovered_card.speed*2 )
                if pygame.mouse.get_pressed()[0] and self.can_click == True:
                        self.card_selection = self.hovered_card
                        self.get_move_solution()
                        self.can_click = False
                elif pygame.mouse.get_pressed()[2] and self.can_click == True:
                    self.discard_selection = self.hovered_card
            else: self.hovered_card = None

        #
        # TILES  
        #

        # This handles tile selection. When the mouse is clicked, check every tile for a collision and select if that's the case. Unselect any tiles that aren't colliding.
        if pygame.mouse.get_pressed()[0] and self.can_click == True:
            for tile in self.grid.tile_rects:
                if self.grid.tile_rects[tile].collidepoint(self.mouse_pos):
                    self.tile_selection = eval(tile)
                    break
                else: self.tile_selection = None                
            self.can_click = False

        
        #
        # MOVEMENT/FLIPS 
        # 

        if self.tile_selection != None: self.grid.highlight(self.tile_selection) # Highlight tile if selected
        if self.card_selection != None: self.card_selection.highlight_selection() # Highlight card selection
        if self.discard_selection != None: 
            self.discard_selection.highlight_discard_selection() # Highlight discard selection
            
            if self.tile_selection != None and self.can_click == True:

                # Switch selected tile left if valid
                if self.keys[pygame.K_LEFT]: 
                    if self.tile_selection[0] != 0:
                        self.grid.switch(self.tile_selection, [self.tile_selection[0]-1, self.tile_selection[1]]) ; self.tile_selection[0] -= 1 
                        self.play_card()
                    self.can_click = False

                # Switch selected tile right if valid
                elif self.keys[pygame.K_RIGHT]: 
                    if self.tile_selection[0] != 2:
                        self.grid.switch(self.tile_selection, [self.tile_selection[0]+1, self.tile_selection[1]]) ; self.tile_selection[0] += 1 
                        self.play_card()
                    self.can_click = False

                # Switch selected tile ip if valid
                elif self.keys[pygame.K_UP]: 
                    if self.tile_selection[1] != 0:
                        self.grid.switch(self.tile_selection, [self.tile_selection[0], self.tile_selection[1]-1]) ; self.tile_selection[1] -= 1 
                        self.play_card()
                    self.can_click = False 

                # Switch selected tile down if valid
                elif self.keys[pygame.K_DOWN]: 
                    if self.tile_selection[1] != 2:
                        self.grid.switch(self.tile_selection, [self.tile_selection[0], self.tile_selection[1]+1]) ; self.tile_selection[1] += 1 
                        self.play_card()
                    self.can_click = False

                # Flip the selected tile
                elif self.keys[pygame.K_SPACE]: 
                    self.grid.flip(self.tile_selection)
                    self.play_card()
                    self.can_click = False

        # Cash card if valid. Selection is preferred.
        if self.can_click == True:
            if self.keys[pygame.K_RETURN]: 
                points = self.cash_card()
                if points > 0:
                    self.info_gui.points += points 
                    self.info_gui.total_moves -= 1
                    self.record_move()
                self.can_click = False

# Initialize the program
if __name__ == '__main__':
    print(__file__)      
    PygameEnvironment(1200, 750, 'Shifting Stones', 0)
