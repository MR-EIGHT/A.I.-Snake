from heapq import *
from .utils import *


def solve_astar(game: sg.SnakeGame):
    root_state = Node(game, None)

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
        nm: Node = heappop(state_list)[1]

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






