from heapq import *

from .utils import *


def solve_astar(game: sg.SnakeGame):
    """A* algorithm implementation to solve Snake Game

    Args:
        game (SnakeGame): game object

    Returns:
        list: moves that should be taken to eat the apple
    """
    
    # root node of the search tree of the game
    root_state = Node(game, None)

    # creating a priority queue to store and fetch Nodes with node.minimum(g + h)
    state_list = []
    heapify(state_list)
    
    # adding root state to priority queue
    h = heuristic(root_state)
    g = 0
    heappush(state_list, (h+g, root_state))

    # fetching nodes with minimum heuristic and move count and checking if they're the answer, otherwise pushing them to priority queue
    while len(state_list) != 0:
        (h, nm) = heappop(state_list)
        if h == 0:
            return collect_answer(nm)

        next_moves = get_child_states(nm)

        for n in next_moves:
            h = heuristic(n)
            g = n.state.total_moves
            heappush(state_list, (h+g, n))
