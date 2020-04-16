import copy
import itertools as it
from itertools import combinations
from itertools import chain
import numpy as np
import math
import multiprocessing

class Reliability():
    def __init__(self, tie_set, edges):
        '''
        generate combinations of all tie_sets
        :param tie_set: all terminal tie set
        :param edges: all edges in the graph
        '''
        tie_set_flat = [ts for t in tie_set.values() for ts in t]
        print("Tie set size:", len(tie_set_flat))

        # Find the different combinations of tie sets
        self.combos = ([dict(zip(tie_set.keys(), v)) for v in it.product(*tie_set.values())])
        # for combo in self.combos:
        #     print(combo)

        # Convert to list of edges and reorder the vertices such that v[0] < v[1]
        self.combos = [self.comboDictToList(combo) for combo in self.combos]
        # for combo in self.combos:
        #     print(combo)

        # Get unique edges in all tie set
        self.all_unique_edges = np.array(edges)
        self.unique_elems = self.all_unique_edges.shape[0]
        print(self.all_unique_edges)

        # Probability for all the unique elements in the entire tie set system
        self.all_edge_prob = self.Prob(range(self.unique_elems))
        print(self.all_edge_prob)

    # def swap(self, list):
    #     '''
    #     Swap vertice 1 and 2 since they are equivalent
    #     '''
    #     swappedresult = copy.deepcopy(list)
    #     if (swappedresult[0] > swappedresult[1]):
    #         tmp = swappedresult[0]
    #         swappedresult[0] = swappedresult[1]
    #         swappedresult[1] = tmp
    #     return swappedresult
    #
    # def prodofList(self, arr):
    #     prod = 1
    #     for x in arr:
    #         prod *= x
    #     return prod
    #
    # def Prob(self, twodlist):
    #     # find reliability of 2D list
    #     valarr=[]
    #     for x in twodlist:
    #         valarr.append(x[2])
    #     product =  self.prodofList(valarr)
    #     return product

    # def Prob(self, twodlist):
    #     '''
    #     find reliability of 2D list
    #     :param twodlist: list of edges
    #     :return:
    #     '''
    #     val_arr = np.array([e[2] for e in twodlist])
    #     return float(np.product(val_arr))
    def Prob(self, twodlist):
        '''
        find reliability of 2D list
        :param twodlist: list of edges
        :return:
        '''
        e = np.array(twodlist)
        val_arr = self.all_unique_edges[e,2]
        return float(np.product(val_arr))
    # def removeOverlap(self, rel_arr):
    #     '''Check for equivalent edges or overlapped edges'''
    #     final_arr = []
    #     for indx, r in enumerate(rel_arr):
    #         # if (r in copy_of_rel_arr[indx + 1:]) or (self.swap(r) in copy_of_rel_arr[indx + 1:]):
    #         #     continue
    #         if (r in rel_arr[indx + 1:]):
    #             continue
    #         else:
    #             final_arr.append(r)
    #     return final_arr

    def removeOverlap(self, rel_arr):
        '''Check for equivalent edges or overlapped edges'''
        return list(set(rel_arr))

    # def comboDictToList(self, combo, verbose = 0):
    #     '''
    #     Place all values in dictionary in 2D list
    #
    #     :param combo:
    #     :param verbose:
    #     :return:
    #     '''
    #     rel_arr = []
    #     for key, value in combo.items():
    #         for edge in combo.get(key):
    #             # edge_swapped = self.swap(edge)
    #             # rel_arr.append(edge_swapped)
    #             rel_arr.append(edge[-1])
    #     if(verbose): print("Edges:", rel_arr)
    #     # Check for equivalent edges or overlapped edges
    #     return self.removeOverlap(rel_arr)

    # def comboToList(self, combo, verbose = 0):
    #     '''Place all values in dictionary in 2D list'''
    #     rel_arr = []
    #     for edge in combo:
    #         rel_arr.append(edge)
    #     if(verbose): print("Edges:", rel_arr)
    #     # Check for equivalent edges or overlapped edges
    #     return self.removeOverlap(rel_arr)

    def groupToList(self, group, verbose = 0):
        '''
        Place all values in a group of dictionary in 2D list

        :param group: generator of combinations
        :param verbose:
        :return:
        '''
        # rel_arr = []
        # for combo in group:
        #     for edge in combo:
        #         rel_arr.append(edge)
        # print(np.array(list(group))[:])

        rel_arr = list(chain.from_iterable(group))
        # print(rel_arr)
        if(verbose): print("Edges:", rel_arr)
        # Check for equivalent edges or overlapped edges
        return self.removeOverlap(rel_arr)

    def findTotalProbability(self, final_arr, verbose = 0):
        if(verbose): print("Unique Edges:", final_arr)
        # Skip calculation if all edges are found
        if len(final_arr) == len(self.all_unique_edges):
            if(verbose): print("All edges found, skip")
            return self.all_edge_prob
        # Find probability of 2D list
        probability = self.Prob(final_arr)
        return probability

    def groupsProbability(self, groups, len_depth, verbose = 0):
        total = 0
        display = 0
        # if (len_depth> 50000):
        #     display = 1
        # Find probability of all the combinations of tie sets
        for index, group in enumerate(groups):
            # if(display and index % 50000 == 0):
            #     print("evaluating", index, "/", int(len_depth), "total = ", total, "...")
            prob = self.findTotalProbability(self.groupToList(group), verbose = verbose)
            total += prob
        # print(total)
        return total


    def calculateReliability(self, depth):
        groups = list(combinations(self.combos, depth))
        # print("at depth ", y, ", current prob:", total, ", a total of ", len(groups), "groups to evaluate")
        pairedprob = self.groupsProbability(groups, verbose = 0)
        return pairedprob

    def Union(self, depth = None):
        print("Evaluating the union's expression...")
        total = 0
        added = False
        if (depth == None):
            depth = len(self.combos)
        # # Find probability of all the combinations of tie sets
        # for combo in self.combos:
        #     prob = self.findTotalProbability(self.comboToList(combo))
        #     total += prob

        # pool = multiprocessing.Pool(depth)
        # unions = [*pool.map(self.calculateReliability, range(1, depth))]
        #
        # print(unions)
        #
        # # Add/ subtract probability for different combinations of tie sets
        # for y in range(1, depth):
        #     # Add or subtract based on the amount of terms in combinations
        #     # based on union formula
        #     if y % 2 == 0:
        #         total -= unions[y-1]
        #         added = False
        #     else:
        #         total += unions[y-1]
        #         added = True


        # Find probability for different combinations of tie sets
        for y in range(1, depth):
            print('------\nTaking combos for depth', y)
            len_depth = math.factorial(len(self.combos))
            len_depth /= math.factorial(y) * math.factorial(len(self.combos) - y)
            print("At depth ", y, ", current prob:", total, ", a total of ", \
                  len_depth, "groups to evaluate")
            pairedprob = self.groupsProbability(combinations(self.combos, y), len_depth, verbose = 0)
            # Add or subtract based on the amount of terms in combinations
            # based on union formula
            if y % 2 == 0:
                total -= pairedprob
                added = False
            else:
                total += pairedprob
                added = True

        # Add all edge probability in the end (treated separately to save time)
        # Add or subtract the last element in union formula
        if added == True:
            final = total - self.all_edge_prob
        else:
            final = total + self.all_edge_prob

        return final
