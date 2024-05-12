import itertools as it
import math

from src.gui import TargetGUI

class Predictor():
    def __init__(self) -> None:
        self.point_sum = 0
        self.reserved_tiles = []

    def get_valid_pairs(self, gridstate, target_card):
        for c in target_card: 
            if type(c) != int:
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
            if type(c) != int:
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

    def is_valid_move(self, grid, x, y):
        """Check if a move is valid within the grid."""
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def find_paths(self, grid, start, end, path=[], all_paths=[]):
        """Find all possible paths from start to end on a grid."""
        x, y = start
        path.append(start)

        if start == end: all_paths.append(path[:])  # Add a copy of the current path
        else:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if abs(end[0] - new_x) > abs(end[0] - x) or abs(end[1] - new_y) > abs(end[1] - y): pass
                else:
                    if self.is_valid_move(grid, new_x, new_y) and (new_x, new_y) not in path:
                        self.find_paths(grid, (new_x, new_y), end, path, all_paths)
        path.pop()  # Backtrack, remove current position from the path

        r_val = []
        for p in all_paths:
            r = []
            for i in range(len(p)-1):
                r.append([p[i], p[i+1]])
            r_val.append(r)
        return r_val

    def solve_target(self, gridstate, target_card):    
            
            permutations = self.get_permutations(gridstate, target_card) # Get tile/target location pairings per legal target location
            best_point_sum = 1000  # Arbitrarily large to start. This will be reduced later
            best_move_set = []
            best_overlap_set = []
            pathlist = []   
            unique_targets = 0

            for x in target_card[0]:
                for xy in x:
                    if (xy != 9) and (xy != 8): unique_targets += 1

            for permutation in permutations: # Check every permutation 
                permutation_pathlist = []
                for pair in permutation: # Check every possible tile pairing 
                    pathlist = self.find_paths(gridstate, tuple(pair[0][1]),tuple(pair[1][1]), [], [])
                    permutation_pathlist.append(pathlist)

                permutated_paths = list(it.product(*permutation_pathlist))

                for set in permutated_paths:
                    # Per set variable definitions 
                    subtrehand = 0
                    point_sum  = 0
                    used           = []
                    overlap        = []
                    moved_fin_list = []
                    flip_set       = []

                    for path in set:point_sum += len(path)
                    for pair in permutation: 
                        if pair[0][0] != pair[1][0]: point_sum += 1 ; flip_set.append(pair[1][1])

                    for path in set:
                        for step in path:

                            for pair in permutation: 
                                if list(step[0]) == pair[0][1] == pair[1][1]:
                                    if pair not in moved_fin_list:
                                        subtrehand -= 1 ; moved_fin_list.append(pair) ; break
                                    else: subtrehand += 1 ; moved_fin_list.remove(pair)

                            for path_2 in set:
                                for step_2 in path_2:   
                                    if [path, path_2] not in used:
                                        if [step[0],step[1]] == [step_2[1], step_2[0]]: subtrehand += 1 ; used.append([path, path_2]) ; used.append([path_2, path]) ; overlap.append(step)

                    point_sum -= subtrehand
                    if point_sum < best_point_sum: 
                        best_point_sum = point_sum  
                        best_move_set = set 
                        best_overlap_set = overlap
                        best_flip_set = flip_set
            
            return [best_point_sum, best_move_set, best_flip_set, best_overlap_set]


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
