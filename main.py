# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
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

'''
input network 
'''
try:
# 	file_path = input("Please set input file path: ")
# 	reliability_goal = input("Please enter reliability goal: ")
# 	cost_constraint = input("Please enter cost constraint: ")
    file_path = 'input2.txt'
    reliability_goal = 0.9
    cost_constraint = 100
except(e):
    print(e)
    exit()

city_list, edge_list = edge_generator.generate(file_path)

print(city_list)
print(edge_list)

# for e in edge_list:
#     print('Cost:', e.getCost())
#     print("Reliability:", e.getReliability())
#     print(e.vertice_1)
#     print(e.vertice_2)

network = Network(city_list)

'''
Task 1: Meet a given reliability goal
'''
### Step 1: get MST

## 1.1. Create Maximum reliability spanning tree
# Create graph and add all the edges
g = Graph(len(city_list))
g = network.addEdgeList(g, edge_list)
# tie_sets = g.generateTieSet(verbose=False)
# network.print_tie_set(tie_sets)

# Generate MST through Kruskal's Algorithm 
result = g.KruskalMST(type = 'reliability')
print(result)
Rall, totalCost = network.evaluate_network_mst(result)

# Create a new graph of mst
mst = Graph(len(city_list))
mst = network.addEdgeList(mst,result)

# print("\n\nMST in numeric representation")
# mst.printGraph()

# test allTerminalRoutes()
# for route in mst.allTerminalRoutes():
#     for e in route:
#         print(e)
#     print("------")


## 1.2 Generate Tieset
print('\n\n------Tie Sets of MST------')
tie_sets = mst.generateTieSet(verbose=False)
network.print_tie_set(tie_sets)

copyy = copy.deepcopy(mst)
copyy.addEdge(network.city_letter_to_number[edge_list[0].vertice_2],network.city_letter_to_number[edge_list[0].vertice_1],edge_list[0].getReliability(),edge_list[0].getCost())
print(copyy.printGraph())
tie_sets1 = copyy.generateTieSet(verbose=False)
network.print_tie_set(tie_sets1)

for key,val in tie_sets1.items():
    print(key,val)

# my_dict = dict(tie_sets1)
# allNames = sorted(dict(tie_sets1))
# combinations = it.product(*(my_dict[Name] for Name in allNames))
# print(list(combinations))
# comb = list(combinations)
# print(comb)
#
# get length of values for each key
# for x in tie_sets1:
#     print(len(tie_sets1.get(x)))

mydict = ([dict(zip(tie_sets1.keys(),v)) for v in it.product(*tie_sets1.values())])

print([dict(zip(tie_sets1.keys(),v)) for v in it.product(*tie_sets1.values())])
print("Here")
print(mydict[0])
print(len(mydict))

def swap(list):
    swappedresult = copy.deepcopy(list)
    tmp = swappedresult[0]
    swappedresult[0] = swappedresult[1]
    swappedresult[1] = tmp
    return swappedresult

def prodofList(arr):
    prod = 1
    for x in arr:
        prod *= x
    return prod

def Prob(twodlist):
    valarr=[]
    for x in twodlist:
        valarr.append(x[2])
    product =  prodofList(valarr)
    return product

def findTotalProbability(dict):
    print(dict)
    relarr = [[]]
    finalarr = [[]]
    for key in dict:
        for x in dict.get(key):
            relarr.append(x)
    relarr.pop(0)
    print("rel")
    print(relarr)
    copyofrelarr = copy.deepcopy(relarr)
    for indx,r in enumerate(copyofrelarr):
        if (r in copyofrelarr[indx+1:]) or (swap(r) in copyofrelarr[indx+1:]):
            continue
        else:
            finalarr.append(r)
    finalarr.pop(0)
    print("pp")
    print(finalarr)
    probability = Prob(finalarr)
    print(probability)


for x in mydict:
    print("x")
    print(x)
    prob = findTotalProbability(x)

print("yoyo")
print(mydict)
print(tie_sets1)
# for y in list(tie_sets1):
#     print(y)
#     probb = findTotalProbability(y)

    # for key in x:
    #     print(len(x))
    #     print(len(x.get(key)))
    #     print(x.get(key)[0])

pairs = list(combinations(mydict,2))
print(pairs)
print(pairs[0])

def mergeDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value , dict1[key]]
    return dict3

def transformintoonedict(dicto):
    initial = dicto[0]
    print(initial)
    dicto = dicto[1:]
    print(dicto)
    dict3 = defaultdict(list)

    for x in dicto:
        # next = mergeDict(initial, x)
        # initial = next
        for k, v in chain(initial.items(), x.items()):
            dict3[k].append(v)

    return dict3

print("ok")
for x in pairs:
    print(x)
    print(type(x))
    onedict = transformintoonedict(x)
    print(onedict)
    print("pls")
    print(onedict[0])
    for key,val in onedict.items():
        print(val)
        onedict[key] = [e for sl in val for e in sl]
    print("plswork")
    print(onedict)
    plswork = findTotalProbability(onedict)
    print(plswork)

print("hi")
print(mydict)
res = str(mydict)[1:-1]
res = "%s" % res
print(res)
res = ast.literal_eval(res)
print("sss")
print(res)
print(type(res))
allintersection = transformintoonedict(res)
print("hhhh")
print(allintersection)
for key, val in allintersection.items():
    print(val)
    allintersection[key] = [e for sl in val for e in sl]
print("prettypls")
print(allintersection)
finallyw = findTotalProbability(allintersection)
print(finallyw)

# for p in pairs:
#     print("pls")
#     print(p[0])



# def findUnion():


# for x in mydict:
#     print(x)

# my_dict={'A':[[1,2]],'B':[[7,8],[9,4]],'C':[[3,5]]}
# allNames = sorted(my_dict)
# combinations = it.product(*(my_dict[Name] for Name in allNames))
# combo =(list(combinations))
# print(len(combo))

# def isminimaltieset(tiesets1):
#     for key,val in tiesets1.items():
#         for x in val:
#             print(x)
#
# isminimaltieset(tie_sets1)




# swappedresult = copy.deepcopy(result)
#
# for indx,x in enumerate(swappedresult):
#     tmp = x[0]
#     swappedresult[indx][0] = x[1]
#     swappedresult[indx][1] = tmp
# print("ol")
#
# for key,val in tie_sets.items():
#     mstcopy = copy.deepcopy(result)
#     graph = Graph(len(city_list))
#     val = [e for sl in val for e in sl]
#     finalrel = network.augmentation(key,val,graph,edge_list, result, swappedresult,mstcopy)
#     print(finalrel)




## 1.3 TODO: evaluate all terminal reliability thru tie set
# network.evaluate_relaibility_tie_set(tie_sets)

## 1.4 # TODO: augment and evaluate augmented mst
# augmented_mst = copy.deepcopy(mst)
# R = Rall 
# while(R < reliability_goal):



print('------------')


##### Minimum cost spanning tree
# # Generate MST through Kruskal's Algorithm 
# result = g.KruskalMST(type = 'cost') 
# print_network(result)


##### Step 2: augmentation until we meet the reliability target


'''
Task 2: Maximize reliability subject to a given cost constraint
'''


