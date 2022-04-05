from copy import deepcopy
from heapq import *
import snakegame as sg

class ANode:
    def __init__(self, state, parent, move=None):
        self.move = move
        self.state = deepcopy(state)
        self.parent = parent
        
    def __lt__(self, nxt):
        return False
    
    def __eq__(self, __o: object) -> bool:
        return True
        


def solve_astar(game: sg.SnakeGame):
    root_state = ANode(game, None)
    
    state_list = []
    heapify(state_list)
    
    next_moves = get_child_states(root_state)
    
    for nm in next_moves:
        h = heuristic(nm)
        if h == 0:
            return [nm.move]
        g = 1
        f = h + g
        heappush(state_list, (f, nm))
        
    while len(state_list) != 0:
        nm: ANode = heappop(state_list)[1]
        
        next_moves = get_child_states(nm)
        
        for n in next_moves:
            h = heuristic(n)
            # if h == 1:
            #     print("close to answer")
            if h == 0:
                return collect_answer(n)
            g = n.state.total_moves
            f = h + g
            heappush(state_list, (f, n))
    

def heuristic(node: ANode):
    state: sg.SnakeGame = node.state
    
    x_dist = abs(state.head[0] - state.apple[0])
    y_dist = abs(state.head[1] - state.apple[1])
    
    return x_dist + y_dist

def collect_answer(n: ANode):
    answer = []
    cur = n
    while cur:
        answer.append(cur.move)
        cur = cur.parent
    answer.pop()
    answer.reverse()
    return answer
    

def get_child_states(root: ANode) -> ANode:
    children = []
    up = deepcopy(root.state)
    down = deepcopy(root.state)
    right = deepcopy(root.state)
    left = deepcopy(root.state)
    
    if up.move(sg.UP):
        children.append(
            ANode(up, root, sg.UP)
        )
    if down.move(sg.DOWN):
        children.append(
            ANode(down, root, sg.DOWN)
        )
    if right.move(sg.RIGHT):
        children.append(
            ANode(right, root, sg.RIGHT)
        )
    if left.move(sg.LEFT):
        children.append(
            ANode(left, root, sg.LEFT)
        )
    
    return children