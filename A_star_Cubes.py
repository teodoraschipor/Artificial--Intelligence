### A* ALGORITHM

#The cubes are placed in N stacks. We can also have empty stacks (without cubes).
#An initial configuration of the cubes placed in the stacks is given and also a final configuration.
#It requires the sequence of moves (intermediate configurations) to get
#from the initial state to the final state. In a move, we can only take one cube
#in the top of one stack and we can only put it on top of another stack.


#---------------INPUT--------------


# number of stacks
N = 3

# cubes' tags
cubes = ['a', 'b', 'c', 'd']

# number of cubes
M = len(cubes)

# Initial configuration
initial_config = [['a'],['c', 'b'],['d']]

# Final configuration
final_config = [['b', 'c'], [],	['d', 'a']]

def ExtractPositions(stacks):
    # !!! In the dictionary we retain that letter X is in the stack "i" on the position "j" !!!
    positions = {}
    for i, stack in enumerate(stacks):
        for j, cube in enumerate(stack):
            positions[cube] = (i, j)
    return positions

final_positions = ExtractPositions(final_config)


###-----------------PROBLEM----------------------


 #class Node refers to the nodes actually in the graph
 #a node represents the current configuration
class Node:
    # node initialization
    def __init__(self, stacks):
        ###PURPOSE OF THE FUNCTION: initialization node's properties
        self.info = stacks
        # calculate heuristic for this node
        self.h = 0
        distance = 0
        # Positions of the cubes(in this configuration)
        positions = ExtractPositions(stacks)

        #We take the cubes one by one and verify if it is in the right place (like in the final configuration)
        for cube in cubes:
            if positions[cube] != final_positions[cube]:
                distance += 1 # !!!if the position is not the final one, increase distance!!! =>
                              # => example: if the X cube is initially on the position (0,1) and in the final configuration is also on the position (0, 1), its distance will be 0.
                              # => according to our input, all the cubes will have distance = 1

    def __str__ (self):
        return "({}, h={})".format(self.info, self.h)
    def __repr__ (self):
        return f"({self.info}, h={self.h})"


class Edge:
    def __init__(self, end, node):
        ###PURPOSE OF THE FUNCTION: initialize edge
        self.end = end
        self.node = node
        self.cost = 1 # DE SCHIMBAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # each move costs 1

#class Problem contains the particular data of the problem
class Problem:
    def __init__(self):
        ###PURPOSE OF THE FUNCTION: initialize the problem data
        self.nodes = [Node(initial_config)]
        self.edges = []
        self.start_node = self.nodes[0] # = initial configuration
        self.scope_node = final_config

    def contain_in_path(self, node):
        ###Verify if the "node" is in the path ( root -> current node(self))
        ###PURPOSE OF THE FUNCTION: to AVOID the formation of cycles!!!

        ###node - Node type object
        current_node = self #CurrentNode type object
        while current_node:
            if current_node.graph_node.info == node.info: #we compare ONLY the info property
                return True
            current_node = current_node.parent #we search from parent to parent
        return False

    def search_node_name(self, info):
        ###	PURPOSE OF THE FUNCTION: SEARCH FOR A NODE WITH THE INFO EQUAL TO A CERTAIN INFO
        ###"info" = the information we know about a node
        ###return None if there is no node with that info
        ###ELSE !!!return Node(type object)
        for node in self.nodes:
            if node.info == info:
                return node
        #(return None ---- implicit)

### end of problem definition



# A* classes

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
        current_node = self # current node
        path = [current_node]

        #Until we get to the ROOT!!!
        while current_node.parent is not None :
            path = [current_node.parent] + path # add (parent)node to list
            current_node = current_node.parent # from parent to parent
        return path # = A LIST with the path's nodes


    def expand(self):
        ###PURPOSE OF THE FUNCTION: find all the current node's successors
        ### return (successor, cost edge node - successor) -tuple .... the first object = Node; the second = integer

        stacks = self.graph_node.info
        successors = [] #LIST


        # !!! WE TAKE ALL THE COMBINATIONS TO POP FROM A STACK AND ADD TO ANOTHER !!!
        for source_stack in range(N):
            for destination_stack in range(N):
                if not stacks[source_stack]: #empty stack
                    continue
                if source_stack == destination_stack: # we don't make any move. It's ok so far. We move on.
                    continue
                # retain the last cube
                cube_to_move = stacks[source_stack][-1]

                new_stacks = [] #LIST
                for i in range(N):
                    if i == source_stack:
                        new_stack = stacks[i][:-1]
                    elif i == destination_stack:
                        # add the moved cube
                        new_stack = stacks[i] + [cube_to_move]
                    else:
                        new_stack = stacks[i]

                    new_stacks.append(new_stack)

                # !!! THIS CONFIGURATION MUST NOT HAVE DONE BEFORE OTHERWISE WE WILL HAVE AN INFINITE CYCLE. !!!
                # VERIFY:
                successor = problem.search_node_name(new_stacks)
                if not successor:
                    new_node = Node(new_stacks)
                    problem.nodes.append(new_node)
                    successor = new_node

                cost = 1 # !!!!! any move costs 1
                successors.append((successor, cost))

        return successors


    def ScopeTest(self):
        ###PURPOSE OF THE FUNCTION: check if the current configuration is the final configuration
        return self.graph_node.info == self.problem.scope_node


    def __str__ (self):
        if self.parent is None :
            parent = self.parent
        else :
            parent = self.parent.graph_node.info
        return f"({self.graph_node}, parent={parent}, f={self.f}, g={self.g})"



### A* ALGORITHM


def DisplayInfoNode(List):
    ###PURPOSE OF THE FUNCTION: display node's information
    s = "{ "
    for i in List:
        s += str(i) + "  "
    s += " }"
    return s


def DisplayCostSucc(List):
    ###PURPOSE OF THE FUNCTION: display successors' cost
    s = ""
    for (i, cost) in List:
        s += "\nnode: " + str(i) + ", edge cost:" + str(cost)
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
    open = [root]			# discovered nodes that have not been expanded yet!!
    closed = []				# discovered and expanded nodes
    #both lists contain CurrentNode type objects

    while open: # while we have discovered nodes
        # remove the node from open
        current_node = open.pop(0)
        # add the node in closed
        closed.append(current_node)
        if current_node.ScopeTest(): # the config is final
            break

        path = current_node.tree_path()

        for successor, cost in current_node.expand():
            if in_list(path, successor):
                continue

            open_node = in_list(open, successor) # search the open_node in open list
            closed_node = in_list(closed, successor) # search the closed_node in closed list

            g_new = current_node.g + cost # = distance to successor

            if open_node: # if the open_node is in open list
                if g_new < open_node.g: # if we found a better(smaller) distance => UPDATE
                    open_node.g = g_new
                    open_node.f = g_new + open_node.graph_node.h
                    open_node.parent = current_node

            elif closed_node: # if the closed_node is in closed list => calculate f
                f_new = g_new + closed_node.graph_node.h
                if f_new < closed_node.f:# if we found a better(smaller) distance => UPDATE
                    closed_node.g = g_new
                    closed_node.f = f_new + closed_node.graph_node.h
                    closed_node.parent = current_node
                    open.append(closed_node) # MOVE the node in open list to expand again when is necessary
            else:
                # the node is neither in open nor in closed => create e new node and add it to open list
                new_node = CurrentNode(graph_node=successor,parent=current_node,g=g_new)
                open.append(new_node)

        open.sort(key=lambda node: node.f) # sort by the value of function => always pop the minimum

#answer:
    if(len(open) == 0):
        print("\nANSWER: \nList <OPEN> is empty. \nWe don't have any path from start node to scope node")
    else:
        print("\nANSWER: Path with minimum cost: " + DisplayInfoNode(current_node.tree_path()))



if __name__ == "__main__":
    problem = Problem()
    CurrentNode.problem = problem
    Astar()