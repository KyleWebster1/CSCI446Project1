import queue

class Backtracking:
    """
    numVertices = number of vertices in the graph
    numColor = size of color domain
    graph = adjacency matrix representation of a graph structure
    state = saved state for access to print after conclusion
    cost = cost value calculated as the number of backtracks that are required
    """
    def __init__(self, numColor, graph):
        self.numVertices = len(graph)
        self.numColor = numColor
        self.graph = graph
        self.state = []
        self.cost = 0

    def resetValues(self):
        """
        Resets the reporting values for each experiment
        :return:
        """
        self.state = []
        self.cost = 0

    def getCost(self):
        return self.cost

    def getFinalState(self):
        """
        Converts final state to color words and returns the list of the state
        :return: Returns the final state in color terms
        """
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
        """
        Standard Backtracking that will backtrack when a state fails the constraint
        :param state: Current state where the state are the vertices that have been assigned
        :return: Boolean if there is a solution
        """
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
        """
        Determines the size of the domain of the neighbor based on an input state
        :param neighbor: Vertex to check the domain
        :param state: Input state
        :return: Size of the domain of neighbor
        """
        domain = set(range(self.numColor))
        assigned = set()
        for i, x in enumerate(self.graph[neighbor]):
            if i < len(state):
                if x == 1:
                    assigned.add(state[i])
        return len(domain - assigned)

    def forwardChecking(self, state=[]):
        """
        Backtracking with forward checking established
        :param state: Current assigned colors for the vertices
        :return: Returns true if the state is a valid solution
        """
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
        """
        Checks if there exists a value in domain y that does not contradict assigned state a
        :param a: An assigned value for some vertex
        :param y: Input domain to determine contradictions
        :return: True if y has a b that is not a contradiction to a
        """
        passed = False
        for b in list(y):
            if b != a:
                passed = True
        return passed

    def revise(self, q):
        """
        Determines if for a given tuple q, if values in domX have to be removed to make domY valid
        :param q: Tuple (x, y, domX, domY) where x is a vertex x, y is a vertex y, domX is the domain of x, domY is the domain of y
        :return: Returns an edited tuple q
        """
        (x,y,domX,domY) = q
        newdomX = domX.copy()
        for a in list(domX):
            if not self.domainCheck(a, domY):
                newdomX.remove(a)

        return (x,y,newdomX,domY)

    def arcConsistancy(self, dl = 0):
        """
        Arc consistancy revises possible domains for each vertex
        :param dl: domain list where dl is a dictionary of possible domains for each vertex
        :return: the revised domain list for each vertex
        """
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
        """
        Integration of backtrack algorithm with arc consistancy
        :param domainList: Dictionary of possible domains for each vertex
        :param index: The current vertex being looked at
        :param state: The state of assigned vertices
        :return: Returns true if a possible solution exists
        """
        if len(state) == len(self.graph):
            return True
        for i in domainList[index]:
            #print(domainList)
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
        """
        Checks the validity of a given state

        :param state: Input state to determine if it is valid
        :return: Returns a boolean value for the validity of the state
        """
        lastVertex = len(state) - 1
        for i, x in enumerate(self.graph[lastVertex]):
            if i < lastVertex:
                if x == 1:
                    if state[i] == state[-1]:
                        self.cost += 1
                        return False
        return True
