from queue import PriorityQueue
from .utils import *


def solve_bfs(game: sg.SnakeGame):
    states = PriorityQueue()
    root_state = Node(game, None)
    states.put((0, root_state))

    while not states.empty():
        u = states.get()[1]
        if heuristic(u) == 0:
            return [u.move]
        else:
            next_moves = get_child_states(u)

            for n in next_moves:
                if n.visited is False:
                    n.visited = True
                    h = heuristic(n)
                    if h == 0:
                        return collect_answer(n)
                    states.put((h + 1, n))
