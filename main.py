# ECSE 422 Programming Assignment: Communication Network Designer
# Saima Haneef - 260744058
# Rebecca Xiong - 260711605

# Task 1: Meet a given reliability goal
# Task 2: Maximize reliability subject to a given cost constraint

# The input file must be in the following format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)

# import statements
import edge_generator
from graph import Graph
from network import Network
import copy
import math

try:
# 	file_path = input("Please set input file path: ")
# 	reliability_goal = input("Please enter reliability goal: ")
# 	cost_constraint = input("Please enter cost constraint: ")
    file_path = 'input2.txt'
    reliability_goal = 0.95
    cost_constraint = 100
except(e):
    print(e)
    exit()

# generate city and edge lists
city_list, edge_list = edge_generator.generate(file_path)
print('-------------------------')
print("The list of cities in the network are: " + str(city_list))
print("The cost and reliability between each city is shown below: ")
print(edge_list)
print("Design Specifications:")
print("PART 1: Reliability Goal = ", reliability_goal)
print("PART 2: Cost Constraint = ", cost_constraint)

'''
Task 1: Meet a given reliability goal
'''
# Step 1: Find maximum reliability spanning tree
# Step 2: If reliability is not met, proceed to augmentation stage, where one edge will
# be added iteratively to the spanning tree until the reliability condition is met
# Step 3: If reliability condition is still not met, add parallel edges to each edge in the
# spanning tree and try augmentation again until the reliability condition is met

print('-------------------------\n')
print('PART 1: Meet a given reliability goal\n')

def augmentationStage(mst, type ="1stpart"):
    '''
    The augmentationStage function takes in the spanning tree (for each part) as an argument and augments
    an edge to the spanning tree to increase the reliability of the system.
    This is done using tie sets from each source node to a destination node. An extra edge is augmented between
    the source and destination node in the tie set to create a loop in the design. The reliability of the loop
    is then found. The reliability of the remaining edges in the spanning tree is then calculated along with
    the reliability of the loop to find the overall reliability of the system
    '''
    # initialize mst graph to generate tie sets
    mst_graph = Graph(len(city_list))
    mst_graph = network.addEdgeList(mst_graph, mst)
    finalrel = 0
    finalCost = 0
    finalGraph = copy.deepcopy(mst_graph)
    for r in range(0, len(city_list)-1):
        # configure tie sets from all nodes as sources
        tie_sets = mst_graph.generateTieSet(r, verbose = False)
        # iterate through each tie set
        for key, val in tie_sets.items():
            graph = Graph(len(city_list))
            # transform the tie set from a 3D list to a 2D list
            val = [e for sl in val for e in sl]
            # network.augmentation performs the actual augmentation
            rel, cost, graph = network.augmentation(key, val, graph, edge_list, mst)
            # if this is the first part of the project just check if reliability goal is met otherwise check if
            # both cost constraint and reliability is met
            # print("Augment btw", network.city_number_to_letter[r], "and", network.city_number_to_letter[key], rel, cost)
            if type == "1stpart":
                # update optimal solution
                if (rel >= finalrel):
                    finalrel, finalCost, finalGraph = rel, cost, graph
                # return as soon as the reliability goal is met
                if finalrel >= reliability_goal:
                    return finalrel, finalCost, finalGraph
            elif type == '2ndpart':
                # update optimal solution
                if (rel >= finalrel and cost <= cost_constraint):
                    finalrel, finalCost, finalGraph = rel, cost, graph
    # if type == '2ndpart':
    #     print("Best Augment", finalrel, finalCost)
    return finalrel, finalCost, finalGraph

def parallelEdges(result, original_result, store, type ='1stpart'):
    '''
    The parallelEdges function adds parallel edges to each edge to the spanning tree. This
    'new' spanning tree with better reliabilities is then sent to the augmentation stage again
    '''
    result_sorted = copy.copy(result)
    # 1. sort on secondary key: increasing order of cost
    result_sorted = sorted(result_sorted, key=lambda x: x[3], reverse=False)
    # 2. sort on primary key: increasing order of reliability
    result_sorted = sorted(result_sorted, key=lambda x: x[2], reverse=False)
    # find the lowest reliability - this will be the one where parallel edges are added
    lowest = result_sorted[0]
    # find the index of the lowest reliability
    indx = result.index(lowest)
    # find the reliability of a parallel edge added to the edge with lowest reliability
    paralleledge = 1-pow((1-lowest[2]),2)


    # the following is done to check how many parallel edges have been added to a particular edge
    # if a parallel edge has been detected, then the formula changes in accordance to how many
    # parallel edges are added to one edge
    # Only takes place with 3 or more parallel edges in one edge
    if result[indx][2] != resultcopy[indx][2]:
        n = (math.log10(1-result[indx][2]))/(math.log10(1-original_result[indx][2]))
        paralleledge = 1 - pow((1 - lowest), n+1)

    # replace spanning tree with the new reliability
    result[indx][2] = paralleledge

    # perform augmentation step with new spanning tree
    if type == '1stpart':
        reliability, cost, graph = augmentationStage(result, type ='1stpart')
    else:
        reliability, cost, graph = augmentationStage(result, type ='2ndpart')

    graphcopy = copy.deepcopy(graph)
    # append edges where a parallel edge was added - used to keep track of cost later on
    store.append(result[indx])
    return result, reliability, cost, store, graphcopy

# Create a network object (used to generate tie sets)
network = Network(city_list)
# Create a graph object (used to create the spanning trees)
g = Graph(len(city_list))
# Add edges to the network
g = network.addEdgeList(g, edge_list)

# Generate Max reliability spanning tree through Kruskal's Algorithm
result = g.spanningTree(type ='reliability')
# make a copy of result
resultcopy = copy.deepcopy(result)
# Find the reliability and cost of the spanning tree
Rall, totalCost = network.evaluate_network_mst(result, type = 'reliability')

# If reliability goal is met, just output the spanning tree
if Rall >= reliability_goal:
    print("The final network design for Part 1 is made up of the following edges: ")
    g.printGraph(edge_list)
    print("The reliability of this system is %.4f" % (Rall))
    print("The cost of this system is " + str(Rall))
# otherwise perform augmentation
else:
    relofaugmentedMST, costofaugmentedMST, graph = augmentationStage(result, type='1stpart')
    if relofaugmentedMST >= reliability_goal:
        print("The final network design for Part 1 is made up of the following edges: ")
        graph.printGraph(edge_list)
        print("The reliability of this system is %.4f" % (relofaugmentedMST))
        print("The cost of this system is " + str(costofaugmentedMST))
    # if augmentation is not enough, add parallel edges
    else:
        reliability = Rall
        store = []
        while reliability < reliability_goal:
            result, reliability, cost, store, graphcopy = parallelEdges(result, resultcopy, store, type='1stpart')
        for x in store:
            graphcopy.addEdge(x[0], x[1], x[2], x[3])
        print("The final network design for Part 1 is made up of the following edges: ")
        graphcopy.printGraph(edge_list)
        # calculate cost
        for x in store:
            cost += x[3]
        print("The reliability of this system is %.4f" % (reliability))
        print("The cost of this system is " + str(cost))

'''
Task 2: Maximize reliability subject to a given cost constraint
'''
# Step 1: Find minimum cost spanning tree
# Step 2: If reliability condition and cost constraint is not met, proceed to augmentation stage
# until the cost is below the cost constraint and reliability is above the reliability condition
# Step 3: If reliability condition is still not met, add parallel edges to each edge in the
# spanning tree and try augmentation again until the reliability condition is met and cost constraint is obeyed

print('-------------------------\n')
print('PART 2: Maximize reliability subject to a given cost constraint\n')

# Generate minimum cost spanning tree
result = g.spanningTree(type ='cost')
# make a copy of result
resultcopy = copy.deepcopy(result)
# Find the reliability and cost of the spanning tree
Rall, totalCost = network.evaluate_network_mst(result, type ='cost')

# if cost constraint and reliability is already met, output spanning tree
if totalCost >= cost_constraint:
    print("The minimum cost spanning tree already meets/exceeds the cost constraint")
    print("The final network design for Part 2 is made up of the following edges: ")
    graph.printGraph(edge_list)
    print("The reliability of the system is %.4f" % (Rall))
    print("The cost of the system is " + str(totalCost))

# otherwise perform augmentation and if that is not enough, add parallel edges
else:
    finalRel, finalCost, finalGraph = augmentationStage(result, type='2ndpart')
    finalStore = []
    cost = totalCost
    while cost < cost_constraint:
        # add parallel edges to the edge present in the network which has the lowest reliability
        result, rel, cost, store, graph = parallelEdges(result, resultcopy, copy.copy(finalStore), type ='2ndpart')
        for x in store:
            cost += x[3]
        # check whether cost is exceeded through the last edge addition
        if cost > cost_constraint:
            break
        else:
            finalStore = copy.copy(store)
            finalRel = rel
            finalCost = cost
            finalGraph = copy.deepcopy(graph)
    for x in finalStore:
        finalGraph.addEdge(x[0], x[1], x[2], x[3])

    print("The final network design for Part 2 is made up of the following edges: ")
    finalGraph.printGraph(edge_list)
    print("The reliability of the system is %.4f" % (finalRel))
    print("The cost of the system is " + str(finalCost))



