from edge import Edge

class Network():
    def __init__(self, city_list):
        '''
        Create letter to number and number to letter dictionaries
        '''
        self.city_letter_to_number = {}
        self.city_number_to_letter = {}
        i = 0
        for c in city_list:
            self.city_letter_to_number.update({c: i})
            self.city_number_to_letter.update({i: c})
            i += 1

    def evaluate_network_mst(self, result, type='reliability'):
        Rall = 1
        totalCost = 0
        # print the contents of result to display the built MST
        if type == 'reliability':
            print("The Maximum Reliability Spanning Tree is made up of the following edges:")
        else:
            print("The Minimum Cost Spanning Tree is made up of the following edges:")
        for u, v, weight, cost in result:
            c1 = self.city_number_to_letter[u]
            c2 = self.city_number_to_letter[v]
            Rall *= weight
            totalCost += cost
            print(c1 + " <-> " + c2 + " (%.2f, %.2f) " % (weight, cost))
        print("Terminal Reliability of the MST is: %.2f" % (Rall))
        print("Total Cost of the MST is: %.2f" % (totalCost) + "\n")
        return Rall, totalCost

    def print_tie_set(self, tie_sets):
        for terminal, ts in tie_sets.items():
            print("Tie-Sets to reach terminal:", self.city_number_to_letter[terminal])
            for index, result in enumerate(ts):
                print("TS " + self.city_number_to_letter[terminal] + str(index) + ":")
                Rts = 1
                totalCost = 0
                # print the contents of result to display the detected Tie Set
                for u, v, w, c in result:
                    c1 = self.city_number_to_letter[u]
                    c2 = self.city_number_to_letter[v]
                    Rts *= w
                    totalCost += c
                    print(c1 + " -- " + c2 + " (%.2f, %.2f)" % (w, c))
                print("Reliability of the TS is: %.2f" % (Rts))
                print("Total Cost of the TS is: %.2f\n---" % (totalCost))

    def addEdgeList(self, g, edge_list):
        i = 0
        # add edges to graph
        if isinstance(edge_list[0], Edge):
            for e in edge_list:
                g.addEdge(self.city_letter_to_number[e.vertice_1],
                          self.city_letter_to_number[e.vertice_2],
                          e.getReliability(), e.getCost())
                i += 1
        # add edges in list representation [u,v,w,c] to graph
        else:
            for e in edge_list:
                g.addEdge(e[0], e[1], e[2], e[3])
                i += 1
        # g.clearVisted()
        return g

    def prodofList(self, arr):
        # multiplies values in an array - useful for reliability
        prod = 1
        for x in arr:
            prod *= x
        return prod

    def additionofList(self, arr):
        # adds values in an array - useful for cost
        total = 0
        for x in arr:
            total += x
        return total

    def augmentation(self, k, v, graph, edgelist, mst):
        import copy
        '''
        Augments an edge between each source and destination node for each tie set
        Finds the final reliability, cost and outputs the graph with the added edge
        '''
        # Initializations
        costs = []
        rel_ring = []
        rel_others = []
        mstcopy = copy.deepcopy(mst)

        # copy the spanning tree to check for swapped nodes (means its the same edge)
        swappedmst = copy.deepcopy(mst)
        # generate edges with swapped nodes since those edges are equivalent (e.g. AB and BA are same edge)
        for indx, x in enumerate(swappedmst):
            tmp = x[0]
            swappedmst[indx][0] = x[1]
            swappedmst[indx][1] = tmp

        # get the source node of the tie set
        start = self.city_number_to_letter[v[0][0]]
        # get the destination node of the tie set
        stop = self.city_number_to_letter[k]

        # add an edge between source and destination node to create a loop
        for edge in edgelist:
            if (edge.vertice_1 == start and edge.vertice_2 == stop) or (
                    edge.vertice_1 == stop and edge.vertice_2 == start):
                # add the corresponding values to their respective arrays
                c = edge.getCost()
                w = edge.getReliability()
                costs.append(c)
                rel_ring.append(w)
        graph.addEdge(self.city_letter_to_number[start], self.city_letter_to_number[stop], w, c)

        # add all the costs and reliabilities in original tie set to arrays and add those edges to the graph
        for x in range(0, len(v)):
            graph.addEdge(v[x][0], v[x][1], v[x][2], v[x][3])
            costs.append(v[x][3])
            rel_ring.append(v[x][2])

        # Reliability calculation of loop
        # follow the reliability formula for a loop = P(all success) + P(one failure)
        # find probability of all edges being successful = product of all values in reliability array
        RelofLoop = self.prodofList(rel_ring)
        # add probabilities where one and only one edge fails
        for indx, r in enumerate(rel_ring):
            copy = rel_ring.copy()
            failure = 1 - r
            copy.pop(indx)
            tmp = self.prodofList(copy)
            product = failure * tmp
            RelofLoop += product

        # steps to find the remaining edges in the spanning tree not included in the loop
        # those remaining edges are multiplied by the reliability of the loop
        for x in v:
            # pop all edges included in the tie set
            if x in mst:
                mstcopy.pop(mstcopy.index(x))
            elif x in swappedmst:
                try:
                    mstcopy.pop(mstcopy.index(x))
                except:
                    copyofx = x.copy()
                    tmp = x[0]
                    copyofx[0] = x[1]
                    copyofx[1] = tmp
                    mstcopy.pop(mstcopy.index(copyofx))

        # add all reliabilities, costs and edges not in the loop but in the network to new array
        for x in mstcopy:
            rel_others.append(x[2])
            costs.append(x[3])
            graph.addEdge(x[0], x[1], x[2], x[3])

        # find final reliability and cost
        restofrel = self.prodofList(rel_others)
        finalCost = self.additionofList(costs)
        finalrel = restofrel * RelofLoop
        return finalrel, finalCost, graph