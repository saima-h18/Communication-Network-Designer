from edge import Edge 
import types 
from collections import defaultdict
import copy
# toolfunctions
class Network():
    def __init__(self, city_list):
        '''
        Create letter to number and number to letter dictionaries 
        '''
        self.city_letter_to_number = {}
        self.city_number_to_letter = {}
        i = 0
        for c in city_list:
            self.city_letter_to_number.update({c : i})
            self.city_number_to_letter.update({i : c})
            i += 1
        # print(city_letter_to_number)
        # print(city_number_to_letter)

    def evaluate_network_mst(self, result):
        Rall = 1
        totalCost = 0
        # print the contents of result to display the built MST 
        print("Following are the edges in the constructed MST")
        for u,v,weight,cost in result:
            c1 = self.city_number_to_letter[u]
            c2 = self.city_number_to_letter[v]
            Rall *= weight
            totalCost += cost
            print (c1 + " -- " + c2 +" (%.2f, %.2f) " % (weight,cost)) 
        print("Terminal Reliability of the MST is: %.2f" % (Rall))
        print("Total Cost of the MST is: %.2f" % (totalCost))
        return Rall, totalCost

    def print_tie_set_with_index(self, tie_sets):
        for terminal, ts in tie_sets.items():
            print("Tie-Sets to reach terminal:", self.city_number_to_letter[terminal])
            for index, result in enumerate(ts):
                print("TS " + self.city_number_to_letter[terminal] + str(index) + ":")
                Rts = 1
                totalCost = 0
                # print the contents of result to display the detected Tie Set
                for u, v, w, c, i  in result:
                    c1 = self.city_number_to_letter[u]
                    c2 = self.city_number_to_letter[v]
                    Rts *= w
                    totalCost += c
                    print("Edge", i , ":", c1 + " -- " + c2 + " (%.2f, %.2f)" % (w, c))
                print("Reliability of the TS is: %.2f" % (Rts))
                print("Total Cost of the TS is: %.2f\n---" % (totalCost))

    def print_tie_set(self, tie_sets):
        for terminal, ts in tie_sets.items():
            print("Tie-Sets to reach terminal:", self.city_number_to_letter[terminal])
            for index, result in enumerate(ts):
                print("TS "+self.city_number_to_letter[terminal]+str(index)+":")
                Rts = 1
                totalCost = 0
                # print the contents of result to display the detected Tie Set
                for u,v,w,c in result:
                    c1 = self.city_number_to_letter[u]
                    c2 = self.city_number_to_letter[v]
                    Rts *= w
                    totalCost += c
                    print (c1 + " -- " + c2 +" (%.2f, %.2f)" % (w,c)) 
                print("Reliability of the TS is: %.2f" % (Rts))
                print("Total Cost of the TS is: %.2f\n---" % (totalCost))
    
    def evaluate_relaibility_tie_set(self, tie_sets):
        tie_set_reliabilities = defaultdict(list)
        for terminal, ts in tie_sets.items():
            for index, result in enumerate(ts):
                Rts = 1
                for u,v,w,c in result:
                    c1 = self.city_number_to_letter[u]
                    c2 = self.city_number_to_letter[v]
                    Rts *= w
                    # print (c1 + " -- " + c2 +" == %.2f, %.2f" % (w,c)) 
                tie_set_reliabilities[terminal].append(Rts)
                # print("Reliability of the TS is: %.2f" % (Rts))
        for terminal, rs in tie_set_reliabilities.items():
            print(self.city_number_to_letter[terminal], rs)
        Rall = 1 
        for terminal, rs in tie_set_reliabilities.items():
            ts_reliability = 1
            for r in rs:
                # TODO: figure out the tie set reliability here # 
                ts_reliability += r
                
                
                
            Rall *= ts_reliability
        return Rall
        
    def addEdgeList(self, g, edge_list):
        i = 0
        # add edges to graph 
        if isinstance(edge_list[0], Edge):
            for e in edge_list:

                g.addEdge(self.city_letter_to_number[e.vertice_1],
                self.city_letter_to_number[e.vertice_2],
                e.getReliability(), e.getCost())
                i += 1
        # add edges in list represetation [u,v,w,c] to graph 
        else:
            for e in edge_list:
                g.addEdge(e[0],e[1], e[2], e[3])
                i += 1
        # g.clearVisted()
        return g

    def prodofList(self, arr):
        prod = 1
        for x in arr:
            prod *= x
        return prod

    def augmentation(self, k, v, graph, edgelist, result, swappedresult, mstcopy):
        print(v)
        start = self.city_number_to_letter[v[0][0]]
        stop = self.city_number_to_letter[k]
        costs = []
        rel = []
        for edge in edgelist:
            if (edge.vertice_1==start and edge.vertice_2==stop) or (edge.vertice_1==stop and edge.vertice_2==start):
                c = edge.getCost()
                w = edge.getReliability()
                costs.append(c)
                rel.append(w)
        graph.addEdge(self.city_letter_to_number[start],self.city_letter_to_number[stop],w,c)

        for x in range(0,len(v)):
            graph.addEdge(v[x][0],v[x][1],v[x][2],v[x][3])
            costs.append(v[x][3])
            rel.append(v[x][2])
        print(graph.printGraph())

        RelofLoop = self.prodofList(rel)

        for indx, r in enumerate(rel):
            copy = rel.copy()
            failure = 1-r
            copy.pop(indx)
            tmp = self.prodofList(copy)
            product = failure * tmp
            RelofLoop += product
        # print(RelofLoop)

        # for indx,(x,x2) in enumerate(zip(mstcopy, swappedresult)):
        #     if (x in v) or (x2 in v):
        #         mstcopy.pop(indx)


        for x in v:
            if x in result:
                mstcopy.pop(mstcopy.index(x))
            elif x in swappedresult:
                try:
                    mstcopy.pop(mstcopy.index(x))
                except:
                    copyofx = x.copy()
                    tmp = x[0]
                    copyofx[0] = x[1]
                    copyofx[1] = tmp
                    mstcopy.pop(mstcopy.index(copyofx))
        # for indx,x in enumerate(mstcopy):

        # print(result)
        # print("pop")
        # print(mstcopy)
        rel2 = []
        for x in mstcopy:
            rel2.append(x[2])
        restofrel = self.prodofList(rel2)
        # print(restofrel)

        finalrel = restofrel*RelofLoop
        return finalrel