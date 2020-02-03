import Node
import queue

class Backtracking:
    def __init__(self, numColor, graph):
        self.numVertices = len(graph)
        self.numColor = numColor
        self.graph = graph
        self.state = []
        self.cost = 0

    def resetValues(self):
        self.state = []
        self.cost = 0

    def getCost(self):
        return self.cost

    def getFinalState(self):
        for v in range(len(self.state)):
            if self.state[v] == 0:
                self.state[v] = "Red"
            elif self.state[v] == 1:
                self.state[v] = "Yellow"
            elif self.state[v] == 2:
                self.state[v] = "Green"
            elif self.state[v] == 3:
                self.state[v] = "Purple"
        return self.state

    def standardBacktracking(self, state=[]):
        if len(state) == len(self.graph):
            return True

        for i in range(self.numColor):
            state.append(i)
            if self.checkValid(state):
                if self.standardBacktracking(state):
                    self.state = state
                    return True
            state.pop()

        return False

    def checkDomain(self, neighbor, state):
        domain = set(range(self.numColor))
        assigned = set()
        for i, x in enumerate(self.graph[neighbor]):
            if i < len(state):
                if x == 1:
                    assigned.add(state[i])
        return len(domain - assigned)

    def forwardChecking(self, state=[]):
        if len(state) == len(self.graph):
            return True

        for i in range(self.numColor):
            state.append(i)
            if self.checkValid(state):
                neighbors = []
                for j, x in enumerate(self.graph[len(state) - 1]):
                    if x == 1:
                        neighbors.append(j)
                anyFailed = False
                for k in neighbors:
                    domainSize = self.checkDomain(k, state)
                    if domainSize == 0:
                        self.cost += 1
                        anyFailed = True
                if not anyFailed:
                    if self.forwardChecking(state):
                        self.state = state
                        return True
            state.pop()
        return False

    def domainCheck(self, a, y):
        passed = False
        for b in list(y):
            if b != a:
                passed = True
        return passed

    def revise(self, q):
        (x,y,domX,domY) = q
        newdomX = domX.copy()
        for a in list(domX):
            if not self.domainCheck(a, domY):
                newdomX.remove(a)

        return (x,y,domX,domY)

    def arcConsistancy(self, dl = 0):
        q = queue.Queue()
        domainList = {}
        if dl == 0:
            for i,x in enumerate(self.graph):
                for j,y in enumerate(self.graph[i]):
                    if y == 1:
                        q.put((i, j, set(range(self.numColor)), set(range(self.numColor))))
        else:
            for i, x in enumerate(self.graph):
                for j, y in enumerate(self.graph[i]):
                    if y == 1:
                        domX = set()
                        domY = set()
                        for val in dl[i]:
                            domX.add(val)
                        for val in dl[j]:
                            domY.add(val)
                        q.put((i, j, domX, domY))
        while not q.empty():
            original = q.get()
            temp = self.revise(original)
            if temp != original:
                for j,y in enumerate(self.graph[temp[0]]):
                    q.put((j, temp[0], set(range(self.numColor)), temp[2]))
            else:
                domainList[temp[0]] = temp[2]

        return domainList
    def backtrackAC(self, domainList, index,  state=[]):
        if len(state) == len(self.graph):
            return True
        for i in domainList[index]:
            print(domainList)
            state.append(i)
            if self.checkValid(state):
                newDomainList = domainList.copy()
                newDomainList[index] = set([i])
                newDomainList = self.arcConsistancy(newDomainList)
                if self.backtrackAC(newDomainList, index+1, state):
                    self.state = state
                    return True
                domainList = newDomainList
            state.pop()

        return False

    def checkValid(self, state):
        lastVertex = len(state) - 1
        for i, x in enumerate(self.graph[lastVertex]):
            if i < lastVertex:
                if x == 1:
                    if state[i] == state[-1]:
                        self.cost += 1
                        return False
        return True
