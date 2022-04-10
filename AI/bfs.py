from queue import PriorityQueue
from .utils import *


def solve_bfs(game: sg.SnakeGame):
    states = PriorityQueue()
    root_state = Node(game, None)
    h = heuristic(root_state)
    states.put((h, root_state))
    visited = set()
    visited.add(root_state.head)

    while not states.empty():
        (h, node) = states.get()
        
        # draw heatmap
        pygame.time.delay(50)
        draw_circle(node.state)
        draw_total_moves(node)
        
        if h == 0:
            return [node.move]
        else:
            next_moves = get_child_states(node)

            for n in next_moves:
                if n.head in visited:
                    print(n.head, " was visited")
                    continue
                visited.add(n.head)
                
                h = heuristic(n)
                if h == 0:
                    return collect_answer(n)
                states.put((h, n))
