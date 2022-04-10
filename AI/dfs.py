from .utils import *


def solve_dfs(game: sg.SnakeGame):
    root_state = Node(game, None)
    return DFS(root_state)


def DFS(s):
    # answer = []
    stack = [s]
    visited = set()
    visited.add(s.head)

    while len(stack) > 0:
        s = stack.pop()
        # draw heatmap
        pygame.time.delay(50)
        draw_circle(s.state)
        draw_total_moves(s)

        if s.head not in visited:
            # answer.append(s.move)
            if heuristic(s) == 0:
                return collect_answer(s)
            visited.add(s.head)

        next_moves = get_child_states(s)
        for node in next_moves:
            if node.head not in visited:
                stack.append(node)
