# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator
# from tool_functions import *
from graph import Graph
from network import Network
from reliability import Reliability
from collections import defaultdict
import copy
import itertools as it
from itertools import combinations
import json
import ast
from itertools import chain
from collections import defaultdict
import numpy as np
'''
input network 
'''
try:
# 	file_path = input("Please set input file path: ")
# 	reliability_goal = input("Please enter reliability goal: ")
# 	cost_constraint = input("Please enter cost constraint: ")
    file_path = 'input2.txt'
    reliability_goal = 0.89
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


# Try one edge augmentation to MST

# totaledgelist = [[]]
# for p in edge_list:
#     totaledgelist.append([network.city_letter_to_number[p.vertice_1],network.city_letter_to_number[p.vertice_2],p.getReliability(),p.getCost()])
#     totaledgelist.append([network.city_letter_to_number[p.vertice_2],network.city_letter_to_number[p.vertice_1],p.getReliability(),p.getCost()])
# totaledgelist.pop(0)
# print(totaledgelist)
#
# for x in totaledgelist:
#     if x or reliability.swap(x) not in result:
#         copyy = copy.deepcopy(mst)
#         copyy.addEdge(x[0],x[1],x[2],x[3])
#         tie_sets1 = copyy.generateTieSet(verbose=False)
#         network.print_tie_set(tie_sets1)
#         print(copyy.printGraph())
#         reliability = Reliability(tie_sets1)
#         finalreliability = reliability.Union()
#         print("finalrel")
#         print(finalreliability)
#         if finalreliability > reliability_goal:
#             print(copyy.printGraph())
#             print("final reliability is "+ str(finalreliability))
#             break

copyy = copy.deepcopy(mst)
copyy.addEdge(network.city_letter_to_number[edge_list[14].vertice_1],network.city_letter_to_number[edge_list[14].vertice_2],edge_list[14].getReliability(),edge_list[14].getCost())
tie_sets1 = copyy.generateTieSet(verbose=False)
network.print_tie_set(tie_sets1)
print(copyy.printGraph())
reliability = Reliability(tie_sets1)
finalreliability = reliability.Union()
print("finalrel")
print(finalreliability)



print('------------')


##### Minimum cost spanning tree
# # Generate MST through Kruskal's Algorithm 
# result = g.KruskalMST(type = 'cost') 
# print_network(result)


##### Step 2: augmentation until we meet the reliability target


'''
Task 2: Maximize reliability subject to a given cost constraint
'''


