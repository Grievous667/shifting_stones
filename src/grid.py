import pygame, random
import math
from src.helper import load_images

class AnimatedTile():
    animated_tiles = []
    def __init__(self, pygame_surf, org_coords, target_coords, tile_id, target_id) -> None:
        self.images = load_images(TileGrid.tile_size)
        self.pygame_surf = pygame_surf
        self.animation_speed = 4
        self.org_coords = org_coords 
        self.target_coords = target_coords
        self.tile_id = tile_id
        self.target_id = target_id
        self.x_traveled = 0
        self.y_traveled = 0
        self.rotation = random.randint(-2,2)

        self.x_distance = self.target_coords[0]*(TileGrid.tile_size + TileGrid.tile_padding) + self.x_traveled - self.org_coords[0]*(TileGrid.tile_size + TileGrid.tile_padding)
        self.y_distance = self.target_coords[1]*(TileGrid.tile_size + TileGrid.tile_padding) + self.y_traveled - self.org_coords[1]*(TileGrid.tile_size + TileGrid.tile_padding)
        AnimatedTile.animated_tiles.append(self)


class TileGrid():
    tile_size = 200
    tile_padding = 10
    tile_xoffset = 150
    tile_yoffset = -110

    def __init__(self, pygame_surf) -> None:
        self.tile_choices = [[0,1], [2,3], [2,3], [4,5], [4,5], [4,5], [6,7], [6,7], [6,7]]
        self.gridstate = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.tile_size = TileGrid.tile_size
        self.tile_padding = TileGrid.tile_padding
        self.tile_xoffset = TileGrid.tile_xoffset
        self.tile_yoffset = TileGrid.tile_yoffset

        self.tile_rects = dict()
        
        
        self.pygame_surf = pygame_surf
        self.images = load_images(self.tile_size)
        

        for y in range(3):
            for x in range(3): 
                self.tile_rects['['+str(x)+','+str(y)+']'] = pygame.Rect((x+1)*self.tile_size + (self.tile_padding*x) + self.tile_xoffset, (y+1)*self.tile_size + (self.tile_padding*y)+self.tile_yoffset, self.tile_size, self.tile_size)
                tiletype = random.randint(0, len(self.tile_choices)-1)
                tileflip = random.randint(0,1)
                AnimatedTile(self.pygame_surf, [x, y], [x, y], self.tile_choices[tiletype][tileflip], self.tile_choices[tiletype][tileflip])
                self.gridstate[x][y] = self.tile_choices[tiletype][tileflip]
                self.tile_choices.remove(self.tile_choices[tiletype])
        

    def switch(self, tile1, tile2):  # Switch any two tiles on the board
        to_front = None
        for tile in AnimatedTile.animated_tiles:
            if   tile.target_coords == [tile1[1], tile1[0]]: tile.target_coords = [tile2[1], tile2[0]] ; to_front = tile
            elif tile.target_coords == [tile2[1], tile2[0]]: tile.target_coords = [tile1[1], tile1[0]] 
        
        AnimatedTile.animated_tiles.append(AnimatedTile.animated_tiles.pop(AnimatedTile.animated_tiles.index(to_front)))

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
            tile.x_distance = (((tile.target_coords[0]+1)*TileGrid.tile_size + (TileGrid.tile_padding*tile.target_coords[0]) - ((tile.org_coords[0]+1)*TileGrid.tile_size) - (TileGrid.tile_padding*tile.org_coords[0]))) - tile.x_traveled
            tile.y_distance = (((tile.target_coords[1]+1)*TileGrid.tile_size + (TileGrid.tile_padding*tile.target_coords[1]) - ((tile.org_coords[1]+1)*TileGrid.tile_size) - (TileGrid.tile_padding*tile.org_coords[1]))) - tile.y_traveled 
            
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
            
            brect =[(tile.org_coords[1]+1)*TileGrid.tile_size + (TileGrid.tile_padding*tile.org_coords[1]) + TileGrid.tile_xoffset + tile.y_traveled, (tile.org_coords[0]+1)*TileGrid.tile_size + (TileGrid.tile_padding*tile.org_coords[0])+TileGrid.tile_yoffset + tile.x_traveled, TileGrid.tile_size, TileGrid.tile_size] # Tile Rect
                
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

            tile.pygame_surf.blit(shadow_img, [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow
            tile.pygame_surf.blit(shadow_img, [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow
            tile.pygame_surf.blit(render_img, brect)


        # for x in range(3):
        #     for y in range(3):
        #         brect = [(x+1)*self.tile_size + (self.tile_padding*x) + self.tile_xoffset, (y+1)*self.tile_size + (self.tile_padding*y)+self.tile_yoffset, self.tile_size, self.tile_size] # Tile Rect
            
                

                # self.pygame_surf.blit(self.images[12], [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow
                # self.pygame_surf.blit(self.images[12], [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow

                # if   self.gridstate[y][x] == 0: self.pygame_surf.blit(self.images[0], brect) # Sun
                # elif self.gridstate[y][x] == 1: self.pygame_surf.blit(self.images[1], brect) # Moon
                # elif self.gridstate[y][x] == 2: self.pygame_surf.blit(self.images[2], brect) # Fish
                # elif self.gridstate[y][x] == 3: self.pygame_surf.blit(self.images[3], brect) # Bird
                # elif self.gridstate[y][x] == 4: self.pygame_surf.blit(self.images[4], brect) # Horse
                # elif self.gridstate[y][x] == 5: self.pygame_surf.blit(self.images[5], brect) # Boat
                # elif self.gridstate[y][x] == 6: self.pygame_surf.blit(self.images[6], brect) # Seed
                # elif self.gridstate[y][x] == 7: self.pygame_surf.blit(self.images[7], brect) # Tree
            

  

        #             direction = 0
        #             index = self.animated_tiles.index([y,x])
        #             if index % 2 == 1: index -= 1
        #             else: index += 1


        #             self.pygame_surf.blit(self.images[12], [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow
        #             self.pygame_surf.blit(self.images[12], [brect[0]-35, brect[1]-15, brect[2], brect[3]]) # Shadow

        #             if   self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 0: self.pygame_surf.blit(self.images[0], brect) # Sun
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 1: self.pygame_surf.blit(self.images[1], brect) # Moon
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 2: self.pygame_surf.blit(self.images[2], brect) # Fish
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 3: self.pygame_surf.blit(self.images[3], brect) # Bird
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 4: self.pygame_surf.blit(self.images[4], brect) # Horse
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 5: self.pygame_surf.blit(self.images[5], brect) # Boat
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 6: self.pygame_surf.blit(self.images[6], brect) # Seed
        #             elif self.gridstate[self.animated_tiles[index][0]][self.animated_tiles[index][1]] == 7: self.pygame_surf.blit(self.images[7], brect) # Tree
        # # self.animated_tiles = []


                # if self.animated_pairs != []:
                #     if (self.animation_xoffset[0][0] > 0 and abs(self.animation_xoffset[0][0]) >= (self.tile_padding + self.tile_size)) or (self.animation_xoffset[0][0] < 0 and abs(self.animation_xoffset[0][0]) >= (self.tile_padding + self.tile_size)) or (self.animation_yoffset[0][0] > 0 and abs(self.animation_yoffset[0][0]) >= (self.tile_padding + self.tile_size)) or (self.animation_yoffset[0][0] < 0 and abs(self.animation_yoffset[0][0]) >= (self.tile_padding + self.tile_size)):
                #         temp = self.gridstate[self.animated_pairs[0][1][0]][self.animated_pairs[0][1][1]]
                #         self.gridstate[self.animated_pairs[0][1][0]][self.animated_pairs[0][1][1]] = self.gridstate[self.animated_pairs[0][0][0]][self.animated_pairs[0][0][1]]
                #         self.gridstate[self.animated_pairs[0][0][0]][self.animated_pairs[0][0][1]] = temp
                        

                #         self.animation_xoffset.pop(0)
                #         self.animation_yoffset.pop(0)
                #         self.animated_tiles.pop(0*2)
                #         self.animated_tiles.pop(0*2)
                #         self.animated_pairs.pop(0)
                    

                
                

    def highlight(self, tile):
        brect = [(tile[0]+1)*self.tile_size + (self.tile_padding*tile[0]) + self.tile_xoffset, (tile[1]+1)*self.tile_size + (self.tile_padding*tile[1])+self.tile_yoffset, self.tile_size, self.tile_size]
        pygame.draw.rect(self.pygame_surf, 'RED', brect, 5)


