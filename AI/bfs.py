from queue import PriorityQueue
from .utils import *


def solve_bfs(game: sg.SnakeGame):
    states = PriorityQueue()
    root_state = Node(game, None)
    h = heuristic(root_state)
    states.put((h, root_state))

    while not states.empty():
        (h, node) = states.get()
        if h == 0:
            return [node.move]
        else:
            next_moves = get_child_states(node)

            for n in next_moves:
                h = heuristic(n)
                if h == 0:
                    return collect_answer(n)
                states.put((h, n))
