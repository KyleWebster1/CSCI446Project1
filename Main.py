import Backtracking
import SimulatedAnnealing
import random
import time


def randomAM(n):
    """
    Randomly generates a graph with the only constraint of no loops and non directional represented as an adjacency matrix
    :param n: The size of the adjacency matrix
    :return: Returns a graph adjacency matrix
    """
    matrix = [[random.randint(0, 1) for i in range(n)] for j in range(n)]

    # No vertex connects to itself
    for i in range(n):
        matrix[i][i] = 0

    # If i is connected to j, j is connected to i
    for i in range(n):
        for j in range(n):
            matrix[j][i] = matrix[i][j]

    return matrix


testingGraph = randomAM(3)

# testingGraph = [[0,1,1,0,0],
#                 [1,0,1,1,0],
#                 [1,1,0,1,1],
#                 [0,1,1,0,0],
#                 [0,0,1,0,0]]


for k in [4]:
    numColor = k
    print("Color size", k)
    for n in [10,20,30,40,50,60,70,80,90,100]:
        initTime = time.time()
        testingGraph = randomAM(n)
        backtrack = Backtracking.Backtracking(numColor, testingGraph)
        print("Graph Size", n)
        if backtrack.standardBacktracking():
            print("Standard Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
        else:
            print("Standard Failed. Cost:", backtrack.getCost())
        print("Time taken:", time.time()-initTime)
        backtrack.resetValues()
        initTime = time.time()
        if backtrack.forwardChecking():
            print("Forward Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
        else:
            print("Forward Backtrack Failed. Cost:", backtrack.getCost())
        print("Time taken:", time.time()-initTime)
        backtrack.resetValues()
        initTime = time.time()
        dl = backtrack.arcConsistancy()
        if backtrack.backtrackAC(dl, 0):
            print("Arc Consistency Backtracking:\n" + str(backtrack.getFinalState()), "\nCost:", backtrack.getCost())
        else:
            print("Arc Consistency Failed. Cost:", backtrack.getCost())
        print("Time taken:", time.time()-initTime)
        initTime = time.time()
        SA = SimulatedAnnealing.SimulatedAnnealing(numColor, testingGraph)
        print(SA.sa())
        print("Time taken:", time.time()-initTime)
