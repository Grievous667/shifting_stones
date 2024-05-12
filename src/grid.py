# MRS: Shifting Stones GUI 
# Code by Luke Becker and Ryan Smith
# 5/11/2024
# This file handles classes related to the tile grid. 


import pygame # Pygame for display and blit functions
import random # Random is imported to distribute the game tiles initially
from src.helper import load_images # Helper function to load textures for the game

class AnimatedTile(): # This class holds graphical and positional information for the displayed tiles
    animated_tiles = [] # List to hold the nine relevant animated tiles
    def __init__(self, pygame_surf, org_coords, target_coords, tile_id, target_id, grid) -> None:
        self.images = load_images(grid.tile_size) # Load tile images
        self.pygame_surf = pygame_surf # Surface to draw on. Should be the main display for the window
        self.animation_speed = 4 # Tile animation speed
        self.org_coords = org_coords  # Coords the tile is moving from 
        self.target_coords = target_coords # Coords the tile is moving to
        self.tile_id = tile_id # What face does the tile show?
        self.target_id = target_id # What face does the target destination show?
        self.x_traveled = 0 # How far has the tile travelled horizontally?
        self.y_traveled = 0 # How far has the tile travelled vertically?
        self.rotation = random.randint(-2,2) # Small rotation value for asthetic purposes

        self.x_distance = self.target_coords[0]*(grid.tile_size + grid.tile_padding) + self.x_traveled - self.org_coords[0]*(grid.tile_size + grid.tile_padding) # X-distance to destination 
        self.y_distance = self.target_coords[1]*(grid.tile_size + grid.tile_padding) + self.y_traveled - self.org_coords[1]*(grid.tile_size + grid.tile_padding) # Y-distance to destination
        AnimatedTile.animated_tiles.append(self) # Append the constructed tile to the global list. 


class TileGrid(): # Main tilegrid object to handle tile logic
    tile_size = 200
    tile_padding = 10

    def __init__(self, pygame_surf, pos=[550, 100]) -> None:
        self.tile_choices = [[0,1], [2,3], [2,3], [4,5], [4,5], [4,5], [6,7], [6,7], [6,7]] # Intitial list of tiles to fill the board with
        self.gridstate = [[0, 0, 0],[0, 0, 0],[0, 0, 0]] # Initial gridstate set to an empty 3x3
        
        self.tile_size = TileGrid.tile_size # How big is a tile?
        self.tile_padding = TileGrid.tile_padding # How much space between tiles? 
        self.pos = pos # Where is the tilegrid drawn?

        self.tile_rects = dict() # Dictionary of tile hitboxes
        
        self.pygame_surf = pygame_surf # Surface to draw on 
        self.images = load_images(self.tile_size) # Load tile images
        

        # Initialize a random, legal board 
        for y in range(3):
            for x in range(3): 
                self.tile_rects['['+str(x)+','+str(y)+']'] = pygame.Rect((x+1)*self.tile_size + (self.tile_padding*x) + self.pos[0] - self.tile_size, (y+1)*self.tile_size + (self.tile_padding*y)+self.pos[1] - self.tile_size, self.tile_size, self.tile_size)
                tiletype = random.randint(0, len(self.tile_choices)-1)
                tileflip = random.randint(0,1)
                AnimatedTile(self.pygame_surf, [x, y], [x, y], self.tile_choices[tiletype][tileflip], self.tile_choices[tiletype][tileflip], self)
                self.gridstate[x][y] = self.tile_choices[tiletype][tileflip]
                self.tile_choices.remove(self.tile_choices[tiletype])
    
    def update_rects(self): # Ensure that the tile rects match their images
        for y in range(3):
            for x in range(3): 
                self.tile_rects['['+str(x)+','+str(y)+']'] = pygame.Rect((x+1)*self.tile_size + (self.tile_padding*x) + self.pos[0] - self.tile_size, (y+1)*self.tile_size + (self.tile_padding*y)+self.pos[1] - self.tile_size, self.tile_size, self.tile_size)

    def switch(self, tile1, tile2):  # Switch any two tiles on the board, with a pretty animation 
        to_front = None
        for tile in AnimatedTile.animated_tiles: # Tell the graphics to move
            if   tile.target_coords == [tile1[1], tile1[0]]: tile.target_coords = [tile2[1], tile2[0]] ; to_front = tile 
            elif tile.target_coords == [tile2[1], tile2[0]]: tile.target_coords = [tile1[1], tile1[0]] 
        AnimatedTile.animated_tiles.append(AnimatedTile.animated_tiles.pop(AnimatedTile.animated_tiles.index(to_front))) # Set the moved tile to the frot of the list so that is drawn on top, rather than under other tiles

        # Swap the identities 
        temp = self.gridstate[tile1[1]][tile1[0]]
        self.gridstate[tile1[1]][tile1[0]] = self.gridstate[tile2[1]][tile2[0]]
        self.gridstate[tile2[1]][tile2[0]] = temp


    def flip(self, tile): # Flip a tile
        if self.gridstate[tile[1]][tile[0]] % 2 == 0: 
            self.gridstate[tile[1]][tile[0]] += 1
            for t in AnimatedTile.animated_tiles:
                if t.target_coords == [tile[1], tile[0]]: t.tile_id += 1 ; break
        else: 
            self.gridstate[tile[1]][tile[0]] -= 1
            for t in AnimatedTile.animated_tiles:
                if t.target_coords == [tile[1], tile[0]]: t.tile_id -= 1 ; break

    def draw_tiles(self):
        for tile in AnimatedTile.animated_tiles:
            tile.x_distance = (((tile.target_coords[0]+1)*self.tile_size + (self.tile_padding*tile.target_coords[0]) - ((tile.org_coords[0]+1)*self.tile_size) - (self.tile_padding*tile.org_coords[0]))) - tile.x_traveled
            tile.y_distance = (((tile.target_coords[1]+1)*self.tile_size + (self.tile_padding*tile.target_coords[1]) - ((tile.org_coords[1]+1)*self.tile_size) - (self.tile_padding*tile.org_coords[1]))) - tile.y_traveled 
            
            error_margin = 5
            if abs(tile.x_distance) < error_margin and abs(tile.y_distance) < error_margin: 
                tile.org_coords = tile.target_coords ; tile.x_traveled = 0 ; tile.y_traveled = 0
            else:
                if abs(tile.x_distance) > error_margin:
                    speed = tile.animation_speed/2 + ((2*tile.animation_speed) * (abs(tile.x_distance)/100))
                    if tile.x_distance > 0: 
                        tile.x_traveled += speed
                        tile.x_distance -= speed
                        if tile.rotation < 5: tile.rotation += random.randint(0,2)/10
                    elif tile.x_distance < 0: 
                        tile.x_traveled -= speed
                        tile.x_distance += speed
                        if tile.rotation > -5: tile.rotation -= random.randint(0,2)/10

                if abs(tile.y_distance) > error_margin:
                    speed = tile.animation_speed/2 + ((2*tile.animation_speed) * (abs(tile.y_distance)/100))
                    if tile.y_distance > 0: 
                        tile.y_traveled += speed
                        tile.y_distance -= speed
                        if tile.rotation > -5: tile.rotation -= random.randint(0,2)/10
                    elif tile.y_distance < 0: 
                        tile.y_traveled -= speed
                        tile.y_distance += speed
                        if tile.rotation < 5: tile.rotation += random.randint(0,2)/10
            
            brect =[(tile.org_coords[1]+1)*self.tile_size + (self.tile_padding*tile.org_coords[1]) + self.pos[0] + tile.y_traveled - self.tile_size, (tile.org_coords[0]+1)*self.tile_size + (self.tile_padding*tile.org_coords[0])+self.pos[1] + tile.x_traveled - self.tile_size, self.tile_size, self.tile_size] # Tile Rect
                
            if   tile.tile_id == 0: render_img = tile.images[0] # Sun
            elif tile.tile_id == 1: render_img = tile.images[1] # Moon
            elif tile.tile_id == 2: render_img = tile.images[2] # Fish
            elif tile.tile_id == 3: render_img = tile.images[3] # Bird
            elif tile.tile_id == 4: render_img = tile.images[4] # Horse
            elif tile.tile_id == 5: render_img = tile.images[5] # Boat
            elif tile.tile_id == 6: render_img = tile.images[6] # Seed
            elif tile.tile_id == 7: render_img = tile.images[7] # Tree

            shadow_img = pygame.transform.rotate(tile.images[12], tile.rotation)
            render_img = pygame.transform.rotate(render_img, tile.rotation)

            tile.pygame_surf.blit(shadow_img, [brect[0]-self.tile_size/10, brect[1]-self.tile_size/9, brect[2], brect[3]]) # Shadow
            tile.pygame_surf.blit(shadow_img, [brect[0]-self.tile_size/10, brect[1]-self.tile_size/9, brect[2], brect[3]]) # Shadow
            tile.pygame_surf.blit(render_img, brect)

    def draw_hint(self, pathset, flips):
        for tilepath in pathset:
            for step in tilepath:
                if [list(step[1]) == tile.target_coords for tile in AnimatedTile.animated_tiles]:
                    x1 = self.pos[0] + (self.tile_size+self.tile_padding)*step[0][1] + self.tile_size/2
                    y1 = self.pos[1] + (self.tile_size+self.tile_padding)*step[0][0] + self.tile_size/2

                    x2 = self.pos[0] + (self.tile_size+self.tile_padding)*step[1][1] + self.tile_size/2
                    y2 = self.pos[1] + (self.tile_size+self.tile_padding)*step[1][0] + self.tile_size/2

                    if step[0][1] != step[1][1]: 
                        loc = [x1-self.images[17].get_width()/2 + (x2-x1)/2, y1-self.images[17].get_height()/2]
                        self.pygame_surf.blit(self.images[17], loc)
                    else:
                        img = pygame.transform.rotate(self.images[17], 90)
                        loc = [x1-img.get_width()/2, y1-img.get_height()/2 + (y2-y1)/2]
                        self.pygame_surf.blit(img, loc)
        for tile in flips:
            x = self.pos[0] + (self.tile_size+self.tile_padding)*tile[1]
            y = self.pos[1] + (self.tile_size+self.tile_padding)*tile[0] + 10
            self.pygame_surf.blit(self.images[16], [x,y])

    def highlight(self, tile):
        brect = [(tile[0]+1)*self.tile_size + (self.tile_padding*tile[0]) + self.pos[0] - self.tile_size, (tile[1]+1)*self.tile_size + (self.tile_padding*tile[1])+self.pos[1] - self.tile_size, self.tile_size, self.tile_size]
        pygame.draw.rect(self.pygame_surf, 'ORANGE', brect, 5)


