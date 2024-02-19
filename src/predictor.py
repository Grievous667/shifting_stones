import itertools as it

from src.gui import TargetGUI

class Predictor():
    def __init__(self) -> None:
        self.point_sum = 0
        self.reserved_tiles = []
    
    def solve_target(self, gridstate, target_card):
        # self.reserved_tiles = []
        # solutions = []

        target_locations = []
        potential_matches = []

        for x in range(3):
            for y in range(3):
                if target_card[0][x][y] != 9 and target_card[0][x][y] != 8:
                    # solutions.append(self.get_shortest(gridstate, [x,y], target_card[0][x][y]))
                    target_locations.append([target_card[0][x][y], [x,y]])
                    for match in self.get_valid_tiles(gridstate, target_card[0][x][y]):
                        potential_matches.append([gridstate[match[0]][match[1]], match])

        # print("Target Locations:", target_locations)
        # print("Matches:",          potential_matches)

        
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

        # print("Unique Targets:", unique_targets)

        move_list = []
        for combo in it.combinations(combo_list, unique_targets):
            combo = list(combo)
            move_list.append(combo)
            for i in range(len(combo)):   
                if self.remove_repeats(i, combo, unique_targets) == True: 
                    move_list.remove(combo)
                    break

        # print('\nMoves:')

        best_point_sum = 999
        for moveset in move_list:
            # print(moveset)
            point_sum = 0
            for move in moveset:
                point_sum += abs(move[0][1][0] - move[1][1][0]) + abs(move[0][1][1] - move[1][1][1])
                if move[0][0] != move[1][0]: point_sum += 1
            if point_sum < best_point_sum: best_point_sum = point_sum
        # print("Point Sum:", best_point_sum)
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
                        valid_tiles.append([x,y])
                else: 
                    if gridstate[x][y] == target_type or gridstate[x][y] == target_type - 1:
                        valid_tiles.append([x,y])
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


        

