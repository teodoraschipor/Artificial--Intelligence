### A* ALGORITHM

#It is considered that we have an equal number (denoted by N) of cannibals and missionaries on the bank of a river.
# They want to cross the river with the help of a boat with M seats.
#If on one of the banks or in the boat, the number of cannibals is higher (strictly) than the number of missionaries,
# then cannibals will eat the missionaries.
#The boat cannot move empty from one bank to another.
#What is the sequence of actions that must be performed so that the missionaries do not become lunch for cannibals?

#The classic problem is with N = 3 (cannibals = missionaries = 3) and M = 2 (seats in the boat).
#The boat and the 2 * N individuals are initially on the east bank, and at the end they all must arrive on the west bank.


###-----------INPUT------------

#number of cannibals = number of missionaries
N = 3

#seats in boat
M = 2


###-------------PROBLEM--------------

#class Node refers to the nodes actually in the graph
#a node represents the current configuration
class Node:
	def __init__(self, info):
        ###PURPOSE OF THE FUNCTION: initialization node's properties
		self.info = info
        # calculate heuristic for this node
		self.h = (info[0] + info[1]) / (M - 1)

	def __str__ (self):
		return "({}, h={})".format(self.info, self.h)
	def __repr__ (self):
		return f"({self.info}, h={self.h})"


class Edge:
	def __init__(self, end, node, cost):
        ###PURPOSE OF THE FUNCTION: initialize edge
		self.end = end
		self.node = node
		self.cost = cost


#class Problem contains the particular data of the problem
class Problem:
    ###PURPOSE OF THE FUNCTION: initialize the problem data
	def __init__(self):
        # Node(N, N, 0) = 3 missionaries, 3 cannibals, the boat is going to the west bank;
        # Node(0, 0, 1) = 0 missionaries, 0 cannibals, the boat is going to the east bank bank.
		self.nodes = [Node((N, N, 0)),Node((0, 0, 1))]
		self.start_node = self.nodes[0]     # Node type object
		self.scope_node = self.nodes[1].info # --- without h

	def search_node_name(self, info):
        ###	PURPOSE OF THE FUNCTION: SEARCH FOR A NODE WITH THE INFO EQUAL TO A CERTAIN INFO
        ###"info" = the information we know about a node
        ###return None if there is no node with that info
        ###ELSE !!!return Node(type object)
		for node in self.nodes:
			if node.info == info:
				return node
		#(return None ---- implicit)


### end of the problem definition



### A* classes

class CurrentNode:
	### = has the info of a node from open/closed lists
	### + f, g - functions from A* algorithm
	problem = None


	def __init__(self, graph_node, parent=None, g=0, f=None):
        ###PURPOSE OF THE FUNCTION: initialization of the current node's properties
		self.graph_node = graph_node	# Node object
		self.parent = parent		# Node object
		self.g = g					# A* function = cost of the path: root -> current node
		if f is None :
			self.f = self.g + self.graph_node.h # FORMULA FROM A* ALGORITHM
		else:
			self.f = f


	def tree_path(self):
		###PURPOSE OF THE FUNCTION: find the path from current node to root
		### PATH - from parent to parent (root is the last)
		current_node = self #current node
		path = [current_node]

        # Until we get to the ROOT!!!
		while current_node.parent is not None :
			path = [current_node.parent] + path # add (parent)node to list
			current_node = current_node.parent # = A LIST with the path's nodes
		return path


	def contain_in_path(self, node):
        ###Verify if the "node" is in the path ( root -> current node(self))
        ###PURPOSE OF THE FUNCTION: to AVOID the formation of cycles!!!

        ###node - Node type object
		current_node = self
		while current_node:
			if current_node.graph_node.info == node.info:
				return True
			current_node = current_node.parent
		return False

	#se modifica in functie de problem
	def expand(self):
		###PURPOSE OF THE FUNCTION: find all the current node's successors
		### return (successor, cost edge node - successor) -tuple .... the first object = Node; the second = integer
		successors = [] #LIST
		missionary_start_bank, cannibal_start_bank, boat = self.graph_node.info
		missionary_destination_bank, cannibal_destination_bank = N - missionary_start_bank, N - cannibal_start_bank

        # !!! WE TAKE ALL THE COMBINATIONS TO TRANSPORT THE MISSIONARIES AND CANNIBALS!!!
        # the next 2 X for will do:
        # 0 missionaries and 0 cannibals, 0 missionaries and 1 cannibal ..... 0 missionaries and M cannibals
        # 1 missionary and 0 cannibals, 1 missionary and 1 cannibal .....  1 missionary and M cannibals
        # .....
        # M missionaries and 0 cannibals, M missionaries and 1 cannibals ..... M missionaries and M cannibals
		for missionary_transport in range(M + 1):
			for cannibal_transport in range(M + 1):
				# the capacity of the boat can't be exceeded
				if missionary_transport + cannibal_transport > M:
					continue
				# the boat must not be empty!!
				if missionary_transport + cannibal_transport == 0:
					continue
				# missionaries must be >= cannibals
				if missionary_transport and cannibal_transport > missionary_transport:
					continue

                #if the boat is leaving the east bank to go to west bank
				if boat == 0:
                    # update the number of missionaries and cannibals on the east and on the west bank
					new_missionary_start_bank = missionary_start_bank - missionary_transport
					new_cannibal_start_bank = cannibal_start_bank - cannibal_transport
					new_missionary_destination_bank = missionary_destination_bank + missionary_transport
					new_cannibal_destination_bank = cannibal_destination_bank + cannibal_transport
				else:#if the boat is leaving the west bank to go to east bank
                    # update the number of missionaries and cannibals on the east and on the west bank
					new_missionary_start_bank = missionary_start_bank + missionary_transport
					new_cannibal_start_bank = cannibal_start_bank + cannibal_transport
					new_missionary_destination_bank = missionary_destination_bank - missionary_transport
					new_cannibal_destination_bank = cannibal_destination_bank - cannibal_transport

				if new_missionary_start_bank and new_cannibal_start_bank > new_missionary_start_bank:
                    #If there are missionaries on the bank after you have made a transport and the number of cannibals on the east bank is is higher than the number of missionaries there
                    #Then do not consider this variant
					continue

				if new_missionary_destination_bank and new_cannibal_destination_bank > new_missionary_destination_bank:
                    # If there are missionaries on the bank after you have made a transport and the number of cannibals on the west bank is is higher than the number of missionaries there
                    # Then do not consider this variant
					continue

				new_info = (new_missionary_start_bank, new_cannibal_start_bank, 1 - boat)

				successors.append((Node(new_info), 1))

		return successors


	def scope_test(self):
        ###PURPOSE OF THE FUNCTION: check if the current configuration is the final configuration
		return self.graph_node.info == self.problem.scope_node


	def __str__ (self):
		parent = self.parent if self.parent is None else self.parent.graph_node.info
		return f"({self.graph_node}, parent={parent}, f={self.f}, g={self.g})"



### A* ALGORITHM

def DisplaySuccessorsCost(List):
	###PURPOSE OF THE FUNCTION: display successors' cost
	s = ""
	for (x, cost) in List:
		s += "\nnode: " + str(x) + ", edge cost:" + str(cost)

	return s

def DisplayInfoNodes(l):
	###PURPOSE OF THE FUNCTION: display node's information
	s = "{ "
	for x in l:
		s += str(x) + "  "
	s += " }"
	return s

def in_list(List, node):
	###PURPOSE OF THE FUNCTION: check if the node is in List
	# node - Node type object
	# List - contains CurrentNode type objects
	for i in range(len(List)):
		if List[i].graph_node.info == node.info:
			return List[i]
	return None


def Astar():
    ###PURPOSE OF THE FUNCTION: find the cheapest path from root (initial configuration) to scope node (final configuration).
	root = CurrentNode(CurrentNode.problem.start_node)
	open = [root]		# discovered nodes that have not been expanded yet!!
	closed = []			# discovered and expanded nodes
	#both lists contain CurrentNode type objects

	while open: # while we have discovered nodes
		# remove the node from open
		current_node = open.pop(0)
        # add the node in closed
		closed.append(current_node)

		if current_node.scope_test(): # we found the final configuration
			break

		path = current_node.tree_path()

		for succesor, cost in current_node.expand():
			if in_list(path, succesor):
				continue

			open_node = in_list(open, succesor) # search the open_node in open list
			closed_node = in_list(closed, succesor) # search the closed_node in closed list

			g_new = current_node.g + cost# = distance to successor

			if open_node: # if the open_node is in open list
				if g_new < open_node.g: # if we found a better(smaller) distance => UPDATE
					open_node.g = g_new
					open_node.f = g_new + open_node.graph_node.h
					open_node.parent = current_node

			elif closed_node: # if the closed_node is in closed list => calculate f
				f_new = g_new + closed_node.graph_node.h
				if f_new < closed_node.f: # if we found a better(smaller) distance => UPDATE
					closed_node.g = g_new
					closed_node.f = f_new + closed_node.graph_node.h
					closed_node.parent = current_node
					open.append(closed_node)# MOVE the node in open list to expand again when is necessary
			else:
				# the node is neither in open nor in closed => create e new node and add it to open list
				new_node = CurrentNode(graph_node=succesor,parent=current_node,g=g_new)

				open.append(new_node)
		open.sort(key=lambda node: node.f) # sort by the value of function => always pop the minimum

#answer
	if(len(open) == 0):
		print("\nANSWER: Open list is empty, we don't have any path from start node(root//initial configuration) to scope node(final configuration)")
	else:
		print("\nANSWER: Path with minimum cost: " + DisplayInfoNodes(current_node.tree_path()))





if __name__ == "__main__":
	problem = Problem()
	CurrentNode.problem = problem
	Astar()