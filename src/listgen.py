import itertools
import sys


def get_permutations(tiles="abbcccddd"):
        return list(set(itertools.permutations(tiles)))

def get_flipped_permutations(unflipped_permutations, tiles):
    final = []
    progress = 0
    for i in range(len(unflipped_permutations)): 
        unflipped_permutations[i] = ''.join(unflipped_permutations[i])
        flips = list(set(map(''.join, itertools.product(*zip(str(unflipped_permutations[i]).upper(), str(unflipped_permutations[i]).lower())))))
        for flip in flips: final.append(flip)
        progress += 2**len(tiles)
        sys.stdout.write("\rFlipped Permutations Processed: " + str(progress))
    print()
    return list(set(final))

def txtify_permutations(permutations, tiles):
    progress = 0
    for i in range(len(permutations)):
        permutations[i] = permutations[i].replace('a', '000') # 000 or 0
        permutations[i] = permutations[i].replace('A', '001') # 001 or 1
        permutations[i] = permutations[i].replace('b', '010') # 010 or 2
        permutations[i] = permutations[i].replace('B', '011') # 011 or 3
        permutations[i] = permutations[i].replace('c', '100') # 100 or 4
        permutations[i] = permutations[i].replace('C', '101') # 101 or 5
        permutations[i] = permutations[i].replace('d', '110') # 110 or 6
        permutations[i] = permutations[i].replace('D', '111') # 111 or 7
        permutations[i] = str(int(permutations[i], 2)) + "\n"

        progress += 1
        if progress % 2**len(tiles) == 0 : sys.stdout.write("\rLines Processed: " + str(progress))
    print()
    print("Writing lines to file...")
    validBoardStates = open("validBoardStates.txt", "w") 
    validBoardStates.writelines(permutations)
    validBoardStates.close()
    print("Processing complete")



tiles = 'abbcccddd'

ufperms = get_permutations(tiles)
print("Unflipped Permutations:", len(ufperms))
flperms = get_flipped_permutations(ufperms, tiles)

txtify_permutations(flperms, tiles)