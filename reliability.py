
import edge_generator
# from tool_functions import *
from graph import Graph
from network import Network
from collections import defaultdict
import copy
import itertools as it
from itertools import combinations
import json
import ast
from itertools import chain
from collections import defaultdict
import numpy as np


class Reliability():


    def __init__(self, tie_sets1):
        # find the different combinations of tie sets
        self.mydict = ([dict(zip(tie_sets1.keys(), v)) for v in it.product(*tie_sets1.values())])
        tiesetcopy = copy.deepcopy(tie_sets1)

        for key,val in tiesetcopy.items():
            # turn 3D list to 2D list
            tiesetcopy[key] = [e for sl in val for e in sl]
        for key,val in tiesetcopy.items():
            print(key,val)

        dictValues = list (tiesetcopy.values())
        # print(dictValues)
        dictValues = [e for sl in dictValues for e in sl]
        # print(dictValues)
        val = np.unique(dictValues, axis=0)
        # print(val)
        copyofval = copy.deepcopy(np.ndarray.tolist(val))
        self.finalarr1 = []
        # check for the same edges in the list of unique elements
        for indx,x in enumerate(copyofval):

            if (x in copyofval[indx + 1:]) or (self.swap(x) in copyofval[indx + 1:]):
                continue
            else:
                self.finalarr1.append(x)
        self.uniqueelems = len(self.finalarr1)
        print(self.finalarr1)
        # probability for all the unique elements in the entire tie set system
        self.maxprob = self.Prob(self.finalarr1)

    def swap(self, list):
        # swap vertice 1 and 2 since they are equivalent
        swappedresult = copy.deepcopy(list)
        tmp = swappedresult[0]
        swappedresult[0] = swappedresult[1]
        swappedresult[1] = tmp
        return swappedresult

    def prodofList(self, arr):
        prod = 1
        for x in arr:
            prod *= x
        return prod

    def Prob(self, twodlist):
        # find reliability of 2D list
        valarr=[]
        for x in twodlist:
            valarr.append(x[2])
        product =  self.prodofList(valarr)
        return product

    def findTotalProbability(self, dict):
        relarr = [[]]
        finalarr = [[]]
        # place all values in dictionary in 2D list to find probability
        for key in dict:
            for x in dict.get(key):
                relarr.append(x)
        relarr.pop(0)

        copyofrelarr = copy.deepcopy(relarr)
        # check for equivalent edges or overlapped edges
        for indx,r in enumerate(copyofrelarr):
            if (r in copyofrelarr[indx+1:]) or (self.swap(r) in copyofrelarr[indx+1:]):
                continue
            else:
                finalarr.append(r)
            # if len(finalarr)== uniqueelems+1:
            #     break
        # pop the first empty element
        finalarr.pop(0)
        # find probability of 2D list
        probability = self.Prob(finalarr)
        return probability


    # def transformintoonedict(self, dicto):
    #     initial = dicto[0]
    #     dicto = dicto[1:]
    #     dict3 = defaultdict(list)
    #
    #     for x in dicto:
    #         for k, v in chain(initial.items(), x.items()):
    #             dict3[k].append(v)
    #     return dict3

    def arrayofval(self, dicts):
        arr=[]
        for y in dicts:
            # print(y)
            for k,v in y.items():
                for s in y.get(k):
                    arr.append(s)

                if (all((x or self.swap(x)) in arr for x in self.finalarr1)):
                    return self.maxprob

        finalarr = [[]]
        for indx,r in enumerate(arr):
            if (r in arr[indx+1:]) or (self.swap(r) in arr[indx+1:]):
                continue
            else:
                finalarr.append(r)
            if len(finalarr)== self.uniqueelems+1:
                break
        finalarr.pop(0)
        probability = self.Prob(finalarr)
        return probability

    def pairsProbability(self, pairs):
        total = 0
        result = {}
        # find probability for each pair or other combination
        for x in pairs:
            another = self.arrayofval(x)
            total += another
        return total

    # def intersection(self, mydict):
    #     res = str(mydict)[1:-1]
    #     res = "%s" % res
    #     res = ast.literal_eval(res)
    #     allintersection = self.transformintoonedict(res)
    #
    #     for key, val in allintersection.items():
    #         val1 = np.asarray(val)
    #         # allintersection[key] = np.ndarray.tolist(val1.reshape((val1.shape[0], -1), order='F'))
    #         allintersection[key] = [e for sl in val for e in sl]
    #
    #     finallyw = self.findTotalProbability(allintersection)
    #     return finallyw

    # perform the union of the tie sets
    def Union(self):
        total = 0
        # find probability of all the combinations of tie sets
        for x in self.mydict:
            prob = self.findTotalProbability(x)
            total += prob
        # find probability for different combinations of tie sets
        for y in range(2, len(self.mydict)):
            pairs = list(combinations(self.mydict, y))
            pairedprob = self.pairsProbability(pairs)
            # add or subtract based on the amount of terms in combinations
            # based on union formula
            if y % 2 == 0:
                total -= pairedprob
                added = False
            else:
                total += pairedprob
                added = True
        interprob = self.maxprob
        # interprob = self.intersection(self.mydict)

        # add or subtract the last element in union formula
        if added == True:
            final = total - interprob
        else:
            final = total + interprob

        return final
