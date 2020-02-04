import random
import math

class SimulatedAnnealing:
    def __init__(self, domain, graph):
        self.domain = domain
        self.vectorSize = len(graph)
        self.graph = graph

    def schedule(self, t):
        return 1000/(1+t)

    def initState(self, domain):
        state = []
        for x in range(self.vectorSize):
            state.append(random.choice(range(domain)))
        return state
    def getConflicts(self, current):
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
        conflict = 0
        for i, x in enumerate(self.graph[n]):
            if x == 1:
                if v == current[i]:
                    conflict += 1
        return conflict

    def value(self, state):
        cost = 0
        for x in range(len(state)):
            for i,y  in enumerate([self.graph[x]]):
                if y == 1:
                    if state[x] == state[i]:
                        cost += 1
        cost += len(set(state))
        return cost

    def decision(self, E, T, k):
        return random.random() < math.exp(E/(T))

    def sa(self):
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
                if self.decision(E, T, .01):
                    current = next
            t += 1