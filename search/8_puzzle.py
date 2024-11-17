import time
import copy
from heapq import heappush, heappop

dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]

class PriorityQueue():

    def __init__(self):
        self.heap = []

    def push(self, k):
        heappush(self.heap, k)

    def pop(self):
        return heappop(self.heap)

    def empty(self):
        if not self.heap:
            return True
        else:
            return False


class State():
    def __init__(self, parent, data, empty_cell, cost, level) -> None:
        self.parent = parent
        self.data = data
        self.empty_cell = empty_cell
        self.cost= cost
        self.level= level

    def __lt__(self, nxt):
        return (self.cost) < (nxt.cost)
    
vis = set()
    
def operation(curr, empty_tile_pos, new_empty_tile_pos, level, parent, final_state) -> State:
                
    new_state = copy.deepcopy(curr)

    x1 = empty_tile_pos[0]
    y1 = empty_tile_pos[1]
    x2 = new_empty_tile_pos[0]
    y2 = new_empty_tile_pos[1]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]

    
    cost = calculate_cost(new_state, final_state)

    return State(parent, new_state, new_empty_tile_pos,cost, level+1)

def find_cell(data, tile = 0):
    for(i) in range(3):
        for (j) in range(3):
            if(data[i][j]==tile): return (i, j)

def manhatan(ini, dest) -> int:
    xi, yi = ini
    xd, yd = dest   
    return (abs(xi-xd) + abs(yi-yd))

def calculate_cost(initial_state, final_state):
    cost = 0
    for(i) in range(3):
        for (j) in range(3):
            if((initial_state[i][j]) and initial_state[i][j] !=final_state[i][j]):
                cost += (1 + manhatan((i, j), find_cell(final_state, initial_state[i][j])) ) 
    return cost

def print_matrix(mat):    
    print(*(f" {x[0]}  {x[1]}  {x[2]} " for x in mat), sep = "\n")
    print(" -------- ")

def print_path(root):
    if root == None: return
    
    print_path(root.parent)
    print_matrix(root.data)
    print()

def hash(data):
    h = 0
    pw = 1
    for i in range(3):
        for j in range(3):
            h+= (data[i][j] * pw)
            pw*=11

    return h


def solve(initial_state, final_state):

    pq = PriorityQueue()

    state = State(None,
     initial_state,
     find_cell(initial_state),
     calculate_cost(initial_state, final_state),
     0
    )

    pq.push(state)

    while (not pq.empty()):

        min_cost = pq.pop()
        
        h = hash(min_cost.data)

        if (h in vis): continue
        vis.add(h)

        if(min_cost.cost == 0):
            print_path(min_cost)
            return

        for (u, v) in dirs:
            new_empty_tile = (
                min_cost.empty_cell[0] + u,
                min_cost.empty_cell[1] + v,
            )

            if((0<=new_empty_tile[0] and new_empty_tile[0] <3) and (0<=new_empty_tile[1] and new_empty_tile[1]<3)):
                pq.push(operation(min_cost.data, min_cost.empty_cell, new_empty_tile, min_cost.level, min_cost, final_state))




initial_state = [ 
            [ 2, 8, 3 ], 
            [ 1, 6, 4 ], 
            [ 7, 0, 5 ]  
    ]
final_state = [ 
          [ 1, 2, 3 ], 
          [ 8, 0, 4 ], 
          [ 7, 6, 5 ]
    ]

solve(initial_state, final_state)