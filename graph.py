import string

alphabet_list = list(string.ascii_uppercase)
from collections import defaultdict
from edge import Edge
import edge_generator

class Graph:

    ## === Works Cited (line 17 - 103)===
    # Geeksforgeeks.org: Kruskal’s Minimum Spanning Tree Algorithm | Greedy Algo-2
    # Contributed by Neelam Yadav
    # https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    ## ====================

    def __init__(self, nodes):
        self.V = nodes
        self.graph = []

    # find root of a particular set
    def retrieve(self, parent, i):
        if parent[i] == i:
            return i
        return self.retrieve(parent, parent[i])

    # add an edge to the graph
    def addEdge(self, start, end, r, c):
        self.graph.append([start, end, r, c])

    # add new node to the root of the other node it is being unioned to
    def join(self, parent, rank, x, y):
        root1 = self.retrieve(parent, x)
        root2 = self.retrieve(parent, y)

        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root2] = root1
            rank[root1] += 1

    def spanningTree(self, type='reliability'):

        # initializations
        MST = []
        parentarr = []
        rankarr = []
        # indices of the sorted graph and resulting spanning tree
        indx1 = 0
        indx2 = 0

        if (type == 'reliability'):
            # 1. sort on secondary key: increasing order of cost
            self.graph = sorted(self.graph, key=lambda x: x[3], reverse=False)
            # 2. sort on primary key: decreasing order of reliability
            self.graph = sorted(self.graph, key=lambda x: x[2], reverse=True)
        else:
            # 1. sort on secondary key: decreasing order of reliability
            self.graph = sorted(self.graph, key=lambda x: x[2], reverse=True)
            # 2. sort on primary key: increasing order of cost
            self.graph = sorted(self.graph, key=lambda x: x[3], reverse=False)

        for node in range(self.V):
            parentarr.append(node)
            rankarr.append(0)

        while indx2 < self.V - 1:
            s, d, r, c = self.graph[indx1]
            indx1 = indx1 + 1
            x = self.retrieve(parentarr, s)
            y = self.retrieve(parentarr, d)
            # add edge to result if a loop is not formed
            if x != y:
                indx2 = indx2 + 1
                MST.append([s, d, r, c])
                self.join(parentarr, rankarr, x, y)

        return MST

    # ===== End of Works Cited ======

    def printGraph(self, edge_list):
        for index, e in enumerate(self.graph):
            u = alphabet_list[e[0]]
            v = alphabet_list[e[1]]
            for edge in edge_list:
                if (u == edge.vertice_1 and v == edge.vertice_2) or (u == edge.vertice_2 and v == edge.vertice_1):
                    w, c = edge.getReliability(), edge.getCost()
            print('Edge', index, ': ', u, '--', v, w, c)

    def printSet(self, set):
        for index, e in enumerate(set):
            u = alphabet_list[e[0]]
            v = alphabet_list[e[1]]
            w, c = e[2], e[3]
            print(u, '--', v, w, c)

    # 	def clearVistied(self):
    # 	    self.visited = [0 for _ in range(len(self.graph))]

    def allTerminalRoutes(self, x, verbose=False):
        """
		generate all possible routes from one fixed starting node in the network
		"""
        max_possible = 2 ** (len(self.graph))
        terminal = 0
        routes = []
        # starting_node = self.graph[x][y]
        starting_node = x
        self.createRoute(starting_node, routes, visited=[starting_node], verbose=verbose)
        return routes

    def createRoute(self, starting_node, routes=[], route=[], visited=[], verbose=False):
        """
		Append the edges that are attached to the current node to complete a terminal route
		Calls itself recursively until the next connected nodes are all visited. A route is thus complete
		and the appended to the routes list which keeps track of all the terminal routes
		"""
        connected_edges = self.findConnectedEdges(starting_node)
        if (verbose):
            print("Found Node", starting_node, 'in', connected_edges)
            print("Have visited node:", visited)
            print("Current Route:", route)
        if (connected_edges == None):  # should never happen if MST
            return route
        else:
            for (u, v, w, c) in connected_edges:
                # check whether the next node (v) the edge points to is visited or not
                if not (v in visited):
                    if (verbose): print('-------\nVisit Node', v)
                    # save a copy of visited so it does not affect the other routes in parallel
                    visited_copy = visited.copy()
                    visited_copy.append(v)
                    try:
                        # create a new branch of route by copying
                        route_copy = route.copy()
                        # append the new edge
                        route_copy.append([u, v, w, c])
                    except:
                        # except block to prevent error rising from empty route
                        route_copy = [[u, v, w, c]]
                    routes.append(self.createRoute(v, routes, route_copy, visited_copy))
            if (verbose):
                print("Stop routing as all available nodes have been visitied")
            return route

    def findConnectedEdges(self, node):
        """
		find all edges that are connected to the input node
		"""
        result = []
        for (u, v, w, c) in self.graph:
            if u == node:
                result.append([u, v, w, c])
            elif v == node:
                # reverse the edge direction such that the
                # current node is always output as the first node,
                # making the next node easier to index
                result.append([v, u, w, c])
        return result

    def generateTieSet(self, x, verbose):
        """
		generate the tiesets from the terminal routes
		"""
        routes = self.allTerminalRoutes(x, verbose=verbose)
        tie_set = defaultdict(list)
        for route in routes:
            u, v, w, c = route[-1]
            tie_set[v].append(route)
        return tie_set