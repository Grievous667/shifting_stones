f = open("validBoardStates.txt", "r") 
array = []
for line in f:
    array.append(f.readline())
f.close()
array.sort()
f = open("sortedBoardStates.txt", "w")
f.writelines(array)
f.close()