import itertools as it
import math

from src.gui import TargetGUI

class Predictor():
    def __init__(self) -> None:
        self.point_sum = 0
        self.reserved_tiles = []

    def get_valid_pairs(self, gridstate, target_card):
        for c in target_card: 
            target_locations = []
            potential_matches = []
            for x in range(3):
                for y in range(3):                            
                    if c[x][y] != 9 and c[x][y] != 8:
                        target_locations.append([c[x][y], [x,y]])
                        for match in self.get_valid_tiles(gridstate, c[x][y]):
                            potential_matches.append([gridstate[match[0]][match[1]], match])
            
            # Targetmatchlist holds all potential matches and the target locations. Permutations are made, and every combo without a target location is culled.
                # This means that the result of all the shennanigans here is that all the combinations of tile to target location get put in combo_list
            targetmatchlist = potential_matches.copy()
            targetmatchlist.extend(target_locations)

            combos = it.permutations(targetmatchlist, 2)
            combo_list = []

            unique_targets = 1
            for combo in combos:
                combo = list(combo)
                if (combo[0] in target_locations and combo[1] not in target_locations) or (combo[0] in target_locations and combo[1] in target_locations and combo[1] in potential_matches) or (combo[0] in target_locations and combo[1] in target_locations and combo[0] == combo[1]):
                    if combo[0][0] == combo[1][0] or combo[0][0] % 2 == 0 and combo[0][0] == combo[1][0]-1 or combo[0][0] % 2 != 0 and combo[0][0] == combo[1][0]+1 :
                        if combo not in combo_list:
                            if len(combo_list) >= 1 and combo[0] != combo_list[len(combo_list)-1][0]: unique_targets += 1
                            combo_list.append(combo)    

            # This upcoming code justs culls repeats
            pairlist = []
            for combo in it.combinations(combo_list, unique_targets):
                combo = list(combo)
                pairlist.append(combo)
                for i in range(len(combo)):   
                    if self.remove_repeats(i, combo, unique_targets) == True: 
                        pairlist.remove(combo)
                        break
            return pairlist
        

    def get_permutations(self, gridstate, target_card):
       
            
            # For each valid success state in the current target card
        #   Append each tile that isn't blank to the target_locations list
        #   Then append each tile on the current board that can potentially match a target tile to the potential_matches list
        move_list = []
        for c in target_card: 
            target_locations = []
            potential_matches = []
            for x in range(3):
                for y in range(3):                            
                    if c[x][y] != 9 and c[x][y] != 8:
                        target_locations.append([c[x][y], [x,y]])
                        for match in self.get_valid_tiles(gridstate, c[x][y]):
                            potential_matches.append(match)
            
            # Targetmatchlist holds all potential matches and the target locations. Permutations are made, and every combo without a target location is culled.
                # This means that the result of all the shennanigans here is that all the combinations of tile to target location get put in combo_list
            targetmatchlist = potential_matches.copy()
            targetmatchlist.extend(target_locations)

            combos = it.permutations(targetmatchlist, 2)
            combo_list = []

            unique_targets = 1
            for combo in combos:
                combo = list(combo)
                if (combo[0] in target_locations and combo[1] not in target_locations) or (combo[0] in target_locations and combo[1] in target_locations and combo[1] in potential_matches) or (combo[0] in target_locations and combo[1] in target_locations and combo[0] == combo[1]):
                    if combo[0][0] == combo[1][0] or combo[0][0] % 2 == 0 and combo[0][0] == combo[1][0]-1 or combo[0][0] % 2 != 0 and combo[0][0] == combo[1][0]+1 :
                        if combo not in combo_list:
                            if len(combo_list) >= 1 and combo[0] != combo_list[len(combo_list)-1][0]: unique_targets += 1
                            combo_list.append(combo)    

            # This upcoming code justs culls repeats
            
            for combo in it.combinations(combo_list, unique_targets):
                combo = list(combo)
                move_list.append(combo)
                for i in range(len(combo)):   
                    if self.remove_repeats(i, combo, unique_targets) == True: 
                        move_list.remove(combo)
                        break
        return move_list
            
    def get_steps(self, tile_pair):
        targetc = tile_pair[0][1] # Target Location
        tilec   = tile_pair[1][1] # Selected Tile 

        steplist = []

        for x in range(3):
            for y in range(3):
                if ((y >= targetc[1] and y <= tilec[1]) or (y <= targetc[1] and y >= tilec[1])):
                    if (x >= targetc[0] and x < tilec[0]): steplist.append(((x+1,y), (x,y)))
                    if (x <= targetc[0] and x > tilec[0]): steplist.append(((x,y), (x-1,y)))
                if ((x >= targetc[0] and x <= tilec[0]) or (x <= targetc[0] and x >= tilec[0])):
                    if (y >= targetc[1] and y < tilec[1]): steplist.append(((x,y+1), (x,y)))
                    if (y <= targetc[1] and y > tilec[1]): steplist.append(((x,y), (x,y-1)))


        return steplist

    def solve_target(self, gridstate, target_card):    
            permutations = self.get_permutations(gridstate, target_card)

            best_point_sum = 1000

            for permutation in permutations:
                steplist = []
                point_sum = 0
                for pair in permutation:
                    steplist.extend(self.get_steps(pair))
                
                    point_sum += abs(pair[0][1][0] - pair[1][1][0]) + abs(pair[0][1][1] - pair[1][1][1])
                    if pair[0][0] != pair[1][0]: point_sum += 1


                overlap = math.ceil((len(steplist) - len(set(steplist)))/len(permutation))

                for pair in permutation: 
                    if pair[0][1] == pair[1][1]:
                        for step in steplist: 
                            if [step[0][0], step[0][1]] == pair[0][1] or [step[1][0], step[1][1]] == pair[0][1]:
                                overlap -= 1
                                break

                if math.floor(point_sum - overlap) < best_point_sum: best_point_sum = math.floor(point_sum - overlap)

            print("Point Sum",best_point_sum)
            return best_point_sum
            

    
    def solve_target2(self, gridstate, target_card):
        best_point_sum = 999

        # For each valid success state in the current target card
        #   Append each tile that isn't blank to the target_locations list
        #   Then append each tile on the current board that can potentially match a target tile to the potential_matches list

        for c in target_card: 
            target_locations = []
            potential_matches = []
            for x in range(3):
                for y in range(3):                            
                    if c[x][y] != 9 and c[x][y] != 8:
                        target_locations.append([c[x][y], [x,y]])
                        for match in self.get_valid_tiles(gridstate, c[x][y]):
                            potential_matches.append([gridstate[match[0]][match[1]], match])
            
            # Targetmatchlist holds all potential matches and the target locations. Permutations are made, and every combo without a target location is culled.
                # This means that the result of all the shennanigans here is that all the combinations of tile to target location get put in combo_list
            targetmatchlist = potential_matches.copy()
            targetmatchlist.extend(target_locations)

            combos = it.permutations(targetmatchlist, 2)
            combo_list = []

            unique_targets = 1
            for combo in combos:
                combo = list(combo)
                if (combo[0] in target_locations and combo[1] not in target_locations) or (combo[0] in target_locations and combo[1] in target_locations and combo[1] in potential_matches) or (combo[0] in target_locations and combo[1] in target_locations and combo[0] == combo[1]):
                    if combo[0][0] == combo[1][0] or combo[0][0] % 2 == 0 and combo[0][0] == combo[1][0]-1 or combo[0][0] % 2 != 0 and combo[0][0] == combo[1][0]+1 :
                        if combo not in combo_list:
                            if len(combo_list) >= 1 and combo[0] != combo_list[len(combo_list)-1][0]: unique_targets += 1
                            combo_list.append(combo)    

            # This upcoming code justs culls repeats
            move_list = []
            for combo in it.combinations(combo_list, unique_targets):
                combo = list(combo)
                move_list.append(combo)
                for i in range(len(combo)):   
                    if self.remove_repeats(i, combo, unique_targets) == True: 
                        move_list.remove(combo)
                        break
            
            # Pick the best set of moves.
            # This is where intersection calculations come in
            for moveset in move_list:
                point_sum = 0
                for move in moveset:
                    point_sum += abs(move[0][1][0] - move[1][1][0]) + abs(move[0][1][1] - move[1][1][1])
                    if move[0][0] != move[1][0]: point_sum += 1
                if point_sum < best_point_sum: best_point_sum = point_sum
        return best_point_sum


    def remove_repeats(self, i, combo, unique_targets):
        for j in range(1, unique_targets):
            if i >= j and combo[i][0] == combo[i-j][0]: return True
            if i >= j and combo[i][1] == combo[i-j][1]: return True
        return False



    def get_valid_tiles(self, gridstate, target_type):
        valid_tiles = []
        for x in range(3):
            for y in range(3):
                if target_type % 2 == 0:
                    if gridstate[x][y] == target_type or gridstate[x][y] == target_type + 1:
                        valid_tiles.append([gridstate[x][y], [x,y]])
                else: 
                    if gridstate[x][y] == target_type or gridstate[x][y] == target_type - 1:
                        valid_tiles.append([gridstate[x][y], [x,y]])
        return valid_tiles


    def get_shortest(self, gridstate, loc, target_type):
        valid_tiles = self.get_valid_tiles(gridstate, target_type)
        
 
        dist = 10
        closest_tile = None
        for tile in valid_tiles: 
            if tile not in self.reserved_tiles:
                if gridstate[tile[0]][tile[1]] == target_type: 
                    if abs(tile[0] - loc[0]) + abs(tile[1] - loc[1]) < dist: 
                        closest_tile = tile
                        dist = abs(tile[0] - loc[0]) + abs(tile[1] - loc[1])
                
                elif gridstate[tile[0]][tile[1]] != target_type: 
                    if abs(tile[0] - loc[0]) + abs(tile[1] - loc[1]) + 1 < dist: 
                        closest_tile = tile
                        dist = abs(tile[0] - loc[0]) + abs(tile[1] - loc[1]) + 1

        self.reserved_tiles.append(closest_tile)
        return [loc, closest_tile, dist]


        

