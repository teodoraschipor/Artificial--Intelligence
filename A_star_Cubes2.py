
### A* ALGORITHM

from itertools import permutations
import time


###----------------READ DATA FROM FILE--------------
initial_config = []
#f = input("file name: ")
#file = open(f, "r")
file = open("drum lungime 3-5.txt", "r")
FILE = open("out.txt", "w")

K = int(file.readline())
N = int(file.readline())  # N = number of stacks

for i in range(N):
    stack = []
    number_of_blocks = file.readline()
    if number_of_blocks == 0:
        stack.append("")
    else:
        for j in range(int(number_of_blocks)):
            stack.append(file.readline().rstrip('\n'))
    initial_config.append(stack)


###-----------------PROBLEM----------------------


 #class Node refers to the nodes actually in the graph
 #a node represents the current configuration
class Node:
    # node initialization
    def __init__(self, stacks):
        ###PURPOSE OF THE FUNCTION: initialization node's properties
        self.info = stacks
        self.h = 0

        # heuristic 1:   h =   how many stacks that don't check the scope condition (scope condition = the stack has only one type of permutation)
       # for stack in stacks:
        #    if len(stack) > 1 : # if stack is empty or it has only one cube, we continue with other stacks
         #       for cube in stack:
          #          permutation1 = [''.join(p) for p in permutations(cube)]
           #         permutation2 = [''.join(p) for p in permutations(stack[1])]
            #        permutation1.sort()
             #       permutation2.sort()
              #      if permutation1 != permutation2:
               #         self.h += 1

        # heuristic 2:   h =  sum of:  how many differences are in each stack - 1
      #  all_permutations = []
      #  for stack in stacks:
       #     for cube in stack:
        #        p = [''.join(p) for p in permutations(cube)]  # we find the permutation for the cube
         #       p.sort()
          #      all_permutations.append(p)

            # how many differences are in the stack - 1 (if there are 3 different permutations => 3-1)
           # count = -1
            #while all_permutations:
             #   first = all_permutations[0]
              #  all_permutations = [i for i in all_permutations if i != first]
               # count += 1
            #self.h += count

    def __str__ (self):
        return "({}, h={})".format(self.info, self.h)
    def __repr__ (self):
        return f"({self.info}, h={self.h})"



class Edge:
    def __init__(self, end, node):
        ###PURPOSE OF THE FUNCTION: initialize edge
        self.end = end
        self.node = node



#class Problem contains the particular data of the problem
class Problem:
    def __init__(self):
        ###PURPOSE OF THE FUNCTION: initialize the problem data
        self.nodes = [Node(initial_config)]
        self.edges = []
        self.start_node = self.nodes[0] # = initial configuration


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
        #(return None)

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
        ### return (successor, cost edge node - successor) or an empty list if there's no successor .... the first object = Node; the second = integer

        stacks = self.graph_node.info
        successors = [] #LIST
        all_permutations = []

        # !!! IF THE NUMBER OF STACKS ISN'T ENOUGH (< NUMBER OF PERMUTATIONS) => WE CAN'T REACH A FINAL STATE !!!
        for stack in stacks:
            for cube in stack:
                p = [''.join(p) for p in permutations(cube)]  # we find the permutation for the cube
                p.sort()
                all_permutations.append(p)

        # how many permutations are in all stacks
        count_permutations = 0
        while all_permutations:
            first = all_permutations[0]
            all_permutations = [i for i in all_permutations if i != first]
            count_permutations += 1

        if len(stacks) < count_permutations:
            FILE.write("WE CAN'T REACH A FINAL STATE!")
            return []

        # !!! WE TAKE ALL THE COMBINATIONS TO POP FROM A STACK AND ADD TO ANOTHER !!!
        for source_stack in range(N):
            for destination_stack in range(N):
                if not stacks[source_stack]: # we can't move from an empty stack
                    continue

                if source_stack == destination_stack: # we don't make any move. We don't want to move the block on the same stack
                    continue

                # retain the last cube
                cube_to_move = stacks[source_stack][-1]
              #  print("cube to move=", cube_to_move, type(cube_to_move))
                if len(stacks[destination_stack]) == 0:
                    last_cube_on_destination_stack = 0
                else:
                    last_cube_on_destination_stack = len(set(stacks[destination_stack][-1]))

#                print('last cube', r)
 #               print('len cube to move', (len(set(cube_to_move))))
  #              print('len last cube', last_cube_on_destination_stack)
   #             print('module', abs(len(set(cube_to_move))- last_cube_on_destination_stack))

                if abs(len(set(cube_to_move)) - last_cube_on_destination_stack) > K: # the condition to move the block
                    continue


                new_stacks = [] #LIST
                for i in range(N):
                    if i == source_stack:
                        new_stack = stacks[i][:-1] # copy without the last block
                    elif i == destination_stack:
                        # add the moved cube
                        new_stack = stacks[i] + [cube_to_move]
                    else: # the others remain the same
                        new_stack = stacks[i]

                    new_stacks.append(new_stack)

                # !!! THIS CONFIGURATION MUST NOT HAVE BEEN DONE BEFORE OTHERWISE WE WILL HAVE AN INFINITE CYCLE. !!!
                # VERIFY:
                successor = problem.search_node_name(new_stacks)
                if not successor:
                    new_node = Node(new_stacks)
                    problem.nodes.append(new_node)
                    successor = new_node

                #cost = 1 # !!!!! any move costs 1
                cost = len(cube_to_move)
                successors.append((successor, cost))

        return successors


    def ScopeTest(self):
        ###PURPOSE OF THE FUNCTION: check if the current configuration is the final configuration

        for stack in self.graph_node.info: # info = stacks
            if len(stack) > 1 : # if stack is empty or it has only one cube, we continue with other stacks
                for cube in stack:
                    permutation1 = [''.join(p) for p in permutations(cube)]
                    permutation2 = [''.join(p) for p in permutations(stack[1])]
                    permutation1.sort()
                    permutation2.sort()
                    if permutation1 != permutation2:
                        return False
        return True


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
    open_list = []
    open_list.append(root) # discovered nodes that have not been expanded yet!!
    closed = []				# discovered and expanded nodes
    #both lists contain CurrentNode type objects

    while open_list: # while we have discovered nodes
        # remove the node from open_list
        current_node = open_list.pop(0)

        # add the node in closed
        closed.append(current_node)
        if current_node.ScopeTest(): # the config is final
            break

        path = current_node.tree_path()

        for successor, cost in current_node.expand():
            if in_list(path, successor):
                continue

            open_node = in_list(open_list, successor) # search the open_node in open list
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
                    open_list.append(closed_node) # MOVE the node in open list to expand again when is necessary
            else:
                # the node is neither in open nor i
                #
                #
                # n closed => create e new node and add it to open list
                new_node = CurrentNode(graph_node=successor,parent=current_node,g=g_new)
                open_list.append(new_node)


        open_list.sort(key=lambda node: node.f) # sort by the value of function => always pop the minimum

#answer:

    if(len(open_list) == 0):
        FILE.write("\nANSWER: \nList <OPEN> is empty. \nWe don't have any path from start node to scope node")
    else:
        FILE.write("\nANSWER: \nPath with minimum cost:\n " + DisplayInfoNode(current_node.tree_path()))



if __name__ == "__main__":
    problem = Problem()
    CurrentNode.problem = problem
    Astar()
    time = int(round(time.time() * 1000))
    FILE.write("\n\nTime:  " + str(time) + " milliseconds")