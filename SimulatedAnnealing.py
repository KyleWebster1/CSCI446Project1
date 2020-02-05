import random
import math

class SimulatedAnnealing:
    """
    domain: The number of colors allowed to be used
    vectorSize: The size of the graph calculated as number of nodes
    graph: The graph represented as an adjacency matrix
    """
    def __init__(self, domain, graph):
        self.domain = domain
        self.vectorSize = len(graph)
        self.graph = graph

    def schedule(self, t):
        """
        Calculates teh schedule to update the T value
        :param t: The number of rounds that have been completed
        :return: Returns the new temperature value
        """
        return 1000/(1+t)

    def initState(self, domain):
        """
        Initializes a state to expand upon
        :param domain: The number of colors allowed
        :return: Returns a state list
        """
        state = []
        for x in range(self.vectorSize):
            state.append(random.choice(range(domain)))
        return state

    def getConflicts(self, current):
        """
        Determines the locations of each of the conflicts
        :param current: The current state
        :return: Returns a dictionary of the conflicts created
        """
        conflicts = {}
        for x in range(len(self.graph)):
            for i, y in enumerate(self.graph[x]):
                if y == 1:
                    if current[x] == current[i]:
                        try:
                            conflicts[x].append(i)
                            conflicts[i].append(x)
                        except:
                            conflicts[x] = [i]
                            conflicts[i] = [x]
        return conflicts

    def minConflict(self, current):
        """
        Determines the single change that has to be made that will have the minimum conflict
        :param current: The current state to be modified
        :return: The modified state
        """
        for i in range(10*self.vectorSize):
            conflicts = self.getConflicts(current)
            dom = list(set(range(self.domain)))
            if conflicts == {}:
                return current
            var = random.choice(list(conflicts.keys()))
            v = current[var]
            conCount = self.getConflictCount(var, v, current)
            dom.remove(v)
            for i in dom:
                newCount = self.getConflictCount(var, i, current)
                if newCount < conCount:
                    v = i
                    conCount = newCount
            current[var] = v

        return current

    def getConflictCount(self, n, v, current):
        """
        Determines the number of conflicts
        :param n: The vertex to be tested
        :param v: The input value of the vertex
        :param current: The current state of the algorithm
        :return: Returns the number of conflicts at a given vertex
        """
        conflict = 0
        for i, x in enumerate(self.graph[n]):
            if x == 1:
                if v == current[i]:
                    conflict += 1
        return conflict

    def value(self, state):
        """
        Determines the value of a given state based on the cost and conflicts
        :param state: The state to be evaluated
        :return: The integer value of the cost of the state
        """
        cost = 0
        for x in range(len(state)):
            for i,y  in enumerate([self.graph[x]]):
                if y == 1:
                    if state[x] == state[i]:
                        cost += 1
        cost += len(set(state))
        return cost

    def decision(self, E, T, k):
        """
        Returns the true or false value to accept the worse state
        :param E: The level of change (intended to be negative)
        :param T: The temperature value
        :param k: The tunable parameter k, can be multiplied to T
        :return:
        """
        return random.random() < math.exp(E/(k*T))

    def sa(self):
        """
        Simulated annealing algorithm where the changes occur in a primarily hill climbing method
        :return: Returns a match or failed state
        """
        current = self.initState(self.domain)
        t = 1
        while True:
            T = self.schedule(t)
            if T < 0.1:
                if self.value(current) <= self.domain:
                    return "Found a match", current
                else:
                    return "Failed to Find a match", current
            next = self.minConflict(current)
            E = self.value(next)-self.value(current)
            if E < 0:
                current = next
            else:
                if self.decision(E, T, 1):
                    current = next
            t += 1