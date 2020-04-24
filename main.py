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
	file_path = input("Please set input file path: ")
	reliability_goal = float(input("Please enter reliability goal: "))
	cost_constraint = float(input("Please enter cost constraint: "))
#     file_path = 'input.txt'
#     reliability_goal = 0.95
#     cost_constraint = 100
except(e):
    print(e)
    exit()

# check input
if (reliability_goal >= 1.0):
    print("Reliability Goal is bigger than 1.")
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
                    augTieSet, augTerminal = val, key
                    finalrel, finalCost, finalGraph = rel, cost, graph
                # return as soon as the reliability goal is met
                if finalrel >= reliability_goal:
                    augTieSet, augTerminal = val, key
                    return finalrel, finalCost, finalGraph, augTieSet, augTerminal
            elif type == '2ndpart':
                # update optimal solution
                if (rel >= finalrel and cost <= cost_constraint):
                    augTieSet, augTerminal = val, key
                    finalrel, finalCost, finalGraph = rel, cost, graph
    # if type == '2ndpart':
    #     print("Best Augment", finalrel, finalCost)

    return finalrel, finalCost, finalGraph, augTieSet, augTerminal

def parallelEdges(aug_mst, original_aug_mst, store, mst, augTieSet, augTerminal, type ='1stpart'):
    '''
    The parallelEdges function adds parallel edges to each edge to the spanning tree. This
    'new' spanning tree with better reliabilities is then sent to the augmentation stage again
    '''
    result_sorted = copy.copy(aug_mst)
    # 1. sort on secondary key: increasing order of cost
    result_sorted = sorted(result_sorted, key=lambda x: x[3], reverse=False)
    # 2. sort on primary key: increasing order of reliability
    result_sorted = sorted(result_sorted, key=lambda x: x[2], reverse=False)
    # find the lowest reliability - this will be the one where parallel edges are added
    lowest = result_sorted[0]
    # find the index of the lowest reliability
    indx = aug_mst.index(lowest)
    # find the reliability of a parallel edge added to the edge with lowest reliability
    paralleledge = 1-pow((1-lowest[2]),2)


    # the following is done to check how many parallel edges have been added to a particular edge
    # if a parallel edge has been detected, then the formula changes in accordance to how many
    # parallel edges are added to one edge
    # Only takes place with 3 or more parallel edges in one edge
    if aug_mst[indx][2] != original_aug_mst[indx][2]:
        n = math.ceil((math.log10(1 - aug_mst[indx][2])) / (math.log10(1 - original_aug_mst[indx][2])))
        paralleledge = 1 - pow((1 - original_aug_mst[indx][2]), n + 1)

    # replace spanning tree with the new reliability
    aug_mst[indx][2] = paralleledge
    # append edges where a parallel edge was added - used to keep track of cost later on
    store.append(aug_mst[indx])

    # check whether it is the additional edge added in augmentation
    loopStart = augTieSet[0][0]
    loopEnd = augTerminal
    edge_list_copy = copy.deepcopy(edge_list)
    aug_mst_copy = copy.deepcopy(aug_mst)

    if (loopStart == lowest[0] and loopEnd == lowest[1] ) or (loopStart == lowest[1] and loopEnd == lowest[0]):
        # delete the addtional edge from the augmented mst
        aug_mst_copy.pop(indx)
        # modify reliability of the additional edge in the edge list
        edges = []
        for e in edge_list:
            edges.append([network.city_letter_to_number[e.vertice_1], network.city_letter_to_number[e.vertice_2]])
        try:
            indx = edges.index([lowest[0], lowest[1]])
        except:
            indx = edges.index([lowest[1], lowest[0]])
        edge_list_copy[indx].reliability = paralleledge

    else:
        # modify reliability of the parallel edge in the tie set
        edges = []
        for e in augTieSet:
            edges.append([e[0], e[1]])
        try:
            try:
                indx = edges.index([lowest[0], lowest[1]])
                augTieSet[indx][2] = paralleledge
            except:
                indx = edges.index([lowest[1], lowest[0]])
                augTieSet[indx][2] = paralleledge
        except:
            # do nothing
            print()

        # modify reliability of the additional edge in the edge list
        edges = []
        for e in edge_list:
            edges.append([network.city_letter_to_number[e.vertice_1], network.city_letter_to_number[e.vertice_2]])
        try:
            indx_in_edge_list = edges.index([loopStart, loopEnd])
        except:
            indx_in_edge_list = edges.index([loopEnd, loopStart])

        # delete the addtional edge from the augmented mst
        edges = []
        for e in aug_mst:
            edges.append([e[0], e[1]])
        try:
            indx = edges.index([loopStart, loopEnd])
        except:
            indx = edges.index([loopEnd, loopStart])

        edge_list_copy[indx_in_edge_list].reliability = aug_mst_copy[indx][2]
        aug_mst_copy.pop(indx)

    # perform augmentation step with new spanning tree
    rel, cost, graph = network.augmentation(augTerminal, augTieSet, Graph(len(city_list)), edge_list_copy, aug_mst_copy)
    graphcopy = copy.deepcopy(graph)

    return aug_mst, rel, cost, store, graphcopy

# Create a network object (used to generate tie sets)
network = Network(city_list)
# Create a graph object (used to create the spanning trees)
g = Graph(len(city_list))
# Add edges to the network
g = network.addEdgeList(g, edge_list)

# Generate Max reliability spanning tree through Kruskal's Algorithm
mst = g.spanningTree(type ='reliability')
# Find the reliability and cost of the spanning tree
Rall, totalCost = network.evaluate_network_mst(mst, type = 'reliability')

# If reliability goal is met, just output the spanning tree
if Rall >= reliability_goal:
    print("The final network design for Part 1 is made up of the following edges: ")
    mst_graph = Graph(len(city_list))
    mst_graph = network.addEdgeList(mst_graph, mst)
    mst_graph.printGraph(edge_list)
    print("The reliability of this system is", Rall)
    print("The cost of this system is", totalCost)
# otherwise perform augmentation
else:
    relofaugmentedMST, costofaugmentedMST, graph, augTieSet, augTerminal = augmentationStage(mst, type='1stpart')
    if relofaugmentedMST >= reliability_goal:
        print("The final network design for Part 1 is made up of the following edges: ")
        graph.printGraph(edge_list)
        print("The reliability of this system is", (relofaugmentedMST))
        print("The cost of this system is " + str(costofaugmentedMST))
    # if augmentation is not enough, add parallel edges
    else:
        aug_mst = graph.graph
        original_aug_mst = copy.deepcopy(aug_mst)
        reliability = Rall
        store = []
        while reliability < reliability_goal:
            aug_mst, reliability, cost, store, graphcopy = parallelEdges(aug_mst, original_aug_mst, store, mst,
                                                                        augTieSet, augTerminal)
        print("The final network design for Part 1 is made up of the following edges: ")
        graphcopy.printGraph_parallel(edge_list, store)
        # calculate cost
        for x in store:
            cost += x[3]
        print("The reliability of this system is", (reliability))
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
mst = g.spanningTree(type ='cost')
# Find the reliability and cost of the spanning tree
Rall, totalCost = network.evaluate_network_mst(mst, type ='cost')

# if cost constraint and reliability is already met, output spanning tree
if totalCost >= cost_constraint:
    print("The Minimum Cost Spanning Tree already meets/exceeds the cost constraint")
    print("The final network design for Part 2 is made up of the following edges: ")
    mst_graph = Graph(len(city_list))
    mst_graph = network.addEdgeList(mst_graph, mst)
    mst_graph.printGraph(edge_list)
    print("The reliability of the system is" , (Rall))
    print("The cost of the system is " + str(totalCost)+ ", the cost constraint cannot be met")
    exit()

# otherwise perform augmentation and if that is not enough, add parallel edges
else:
    finalRel, finalCost, finalGraph, augTieSet, augTerminal = augmentationStage(mst, type='2ndpart')
    aug_mst = finalGraph.graph
    original_aug_mst = copy.deepcopy(aug_mst)
    store = []
    finalStore = []
    cost = totalCost
    while cost < cost_constraint:
        # add parallel edges to the edge present in the network which has the lowest reliability
        aug_mst, rel, cost, store, graph = parallelEdges(aug_mst, original_aug_mst, store, mst,
                                                                     augTieSet, augTerminal)
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
        if rel >= 1:
            print("Reliability is high enough. Exiting....")
            break

    print("The final network design for Part 2 is made up of the following edges: ")
    finalGraph.printGraph_parallel(edge_list, finalStore)
    print("The reliability of the system is" , (finalRel))
    print("The cost of the system is " + str(finalCost))
    exit()



