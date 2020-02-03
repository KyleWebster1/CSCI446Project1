import Backtracking
import random

def random_adjacency_matrix(n):
    matrix = [[random.randint(0,1) for i in range(n)] for j in range(n)]

    # No vertex connects to itself
    for i in range(n):
        matrix[i][i] = 0

    # If i is connected to j, j is connected to i
    for i in range(n):
        for j in range(n):
            matrix[j][i] = matrix[i][j]

    return matrix

testingGraph = random_adjacency_matrix(10)

# testingGraph = [[0,1,1,0,0],
#                 [1,0,1,1,0],
#                 [1,1,0,1,1],
#                 [0,1,1,0,0],
#                 [0,0,1,0,0]]
numColor = 4

backtrack = Backtracking.Backtracking(numColor, testingGraph)

for i in testingGraph:
    print(i)

if backtrack.standardBacktracking():
    print("Standard Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
else:
    print("Failed. Cost:", backtrack.getCost())
backtrack.resetValues()
if backtrack.forwardChecking():
    print("Forward Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
else:
    print("Failed. Cost:", backtrack.getCost())
backtrack.resetValues()
dl = backtrack.arcConsistancy()
if backtrack.backtrackAC(dl, 0):
    print("Arc Consistency Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
else:
    print("Failed. Cost:", backtrack.getCost())
