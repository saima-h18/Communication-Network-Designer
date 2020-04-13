import string
alphabet_list = list(string.ascii_uppercase)
from collections import defaultdict

# Class to represent a graph 
class Graph: 

	## === Works Cited (line 17 - 103)===
	# Geeksforgeeks.org: Kruskal’s Minimum Spanning Tree Algorithm | Greedy Algo-2
	# Python program for Kruskal's algorithm to find
	# Minimum Spanning Tree of a given connected,
	# undirected and weighted graph
	# This code is contributed by Neelam Yadav
	# https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
	## ====================

	def __init__(self,vertices): 
		self.V= vertices #No. of vertices 
		self.graph = [] # default dictionary 
								# to store graph 
# 		self.visited = [0 for _ in range(len(self.graph))]
								
	# function to add an edge to graph 
	def addEdge(self,u,v,w,c): 
		self.graph.append([u,v,w,c]) 

	# A utility function to find set of an element i 
	# (uses path compression technique) 
	def find(self, parent, i): 
		if parent[i] == i: 
			return i 
		return self.find(parent, parent[i]) 

	# A function that does union of two sets of x and y 
	# (uses union by rank) 
	def union(self, parent, rank, x, y): 
		xroot = self.find(parent, x) 
		yroot = self.find(parent, y) 

		# Attach smaller rank tree under root of 
		# high rank tree (Union by Rank) 
		if rank[xroot] < rank[yroot]: 
			parent[xroot] = yroot 
		elif rank[xroot] > rank[yroot]: 
			parent[yroot] = xroot 

		# If ranks are same, then make one as root 
		# and increment its rank by one 
		else : 
			parent[yroot] = xroot 
			rank[xroot] += 1

	# The main function to construct MST using Kruskal's 
		# algorithm 
	def KruskalMST(self, type = 'reliability'): 

		result =[] #This will store the resultant MST 

		i = 0 # An index variable, used for sorted edges 
		e = 0 # An index variable, used for result[] 

		# Step 1: Sort all the edges in decreasing 
		# order of their weight. If we are not allowed to change
		# the given graph, we can create a copy of graph 
		if (type == 'reliability'):
			print('Sorting in descending order of reliability...')
			self.graph = sorted(self.graph, key = lambda x: x[2], reverse = True)
		else:
			print('Sorting in ascending order of cost...')
			self.graph = sorted(self.graph, key = lambda x: x[3], reverse = False)

		parent = [] ; rank = [] 

		# Create V subsets with single elements 
		for node in range(self.V): 
			parent.append(node) 
			rank.append(0) 
	
		# Number of edges to be taken is equal to V-1 
		while e < self.V -1 : 

			# Step 2: Pick the largest edge and increment 
			# the index for next iteration 
			u,v,w,c = self.graph[i] 
			i = i + 1
			x = self.find(parent, u) 
			y = self.find(parent ,v) 

			# If including this edge does't cause cycle, 
			# include it in result and increment the index 
			# of result for next edge 
			if x != y: 
				e = e + 1	
				result.append([u,v,w,c]) 
				self.union(parent, rank, x, y)			 
			# Else discard the edge 

		# print the contents of result[] to display the built MST 
		# print "Following are the edges in the constructed MST"
# 		for u,v,weight in result: 
# 			#print str(u) + " -- " + str(v) + " == " + str(weight) 
# 			print ("%d -- %d == %.2f" % (u,v,weight)) 
		return result
	# ===== End of Works Cited ======
	
	def printGraph(self):
		for index, e in enumerate(self.graph):
			u = alphabet_list[e[0]]
			v = alphabet_list[e[1]]
			w,c = e[2], e[3]
			print('Edge',index ,': ', u,'--',v,w,c)

	def printSet(self,set):
		for index, e in enumerate(set):
			u = alphabet_list[e[0]]
			v = alphabet_list[e[1]]
			w,c = e[2], e[3]
			print(u,'--',v,w,c)

# 	def clearVistied(self):
# 	    self.visited = [0 for _ in range(len(self.graph))]

	def allTerminalRoutes(self, verbose = False):
		"""
		generate all possible routes from one fixed starting node in the network
		"""
		max_possible = 2**(len(self.graph))
		terminal = 0
		routes = []
		starting_node = self.graph[0][0]
		self.createRoute(starting_node, routes, visited = [starting_node], verbose = verbose)
	   # print("Routes:", routes)
		return routes


	def createRoute(self, starting_node, routes=[], route=[], visited=[], verbose = False):
		"""
		Append the edges that are attached to the current node to complete a terminal route

		Calls itself recursively until the next connected nodes are all visited. A route is thus complete and the appended to the routes list which keeps track of all the terminal routes

		"""
		connected_edges = self.findConnectedEdges(starting_node)
		if(verbose):
			print("Found Node", starting_node, 'in', connected_edges)
			print("Have visited node:", visited)
			print("Current Route:", route)
		if (connected_edges == None ): # should never happen if MST
			return route
		else:
			for (u,v,w,c) in connected_edges:
				# check whether the next node (v) the edge points to is visited or not
				if not(v in visited):
					if(verbose):print('-------\nVisit Node', v)
					# save a copy of visited so it does not affect the other routes in parallel
					visited_copy = visited.copy()
					visited_copy.append(v)
					try:
						# create a new branch of route by copying
						route_copy = route.copy()
						# append the new edge
						route_copy.append([u,v,w,c])
					except:
						# except block to prevent error rising from empty route
						route_copy=[[u,v,w,c]]
					routes.append(self.createRoute(v, routes,route_copy,visited_copy))
			if(verbose):
				print("Stop routing as all available nodes have been visitied")
			return route

	def findConnectedEdges(self, node):
		"""
		find all edges that are connected to the input node
		"""
		result = []
		for   (u,v,w,c) in self.graph:
			if u == node:
				result.append([u,v,w,c])
			elif v == node:
				# reverse the edge direction such that the
				# current node is always output as the first node,
				#making the next node easier to index
				result.append([v,u,w,c])
		return result

	def generateTieSet(self,verbose):
		"""
		generate the tiesets from the terminal routes

		"""
		routes = self.allTerminalRoutes(verbose=verbose)
		tie_set = defaultdict(list)
		for route in routes:
			u,v,w,c = route[-1]
			tie_set[v].append(route)
	   # print(tie_set.items())
		return tie_set