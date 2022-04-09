from .utils import *


def solve_dfs(game: sg.SnakeGame):
    root_state = Node(game, None)
    return DFS(root_state)


def DFS(s):
    answer = []
    stack = [s]

    while len(stack) > 0:
        s = stack.pop()
        if s.visited is False:
            answer.append(s.move)
            print(answer)
            if heuristic(s) == 0:
                answer.pop(0)
                print(answer)
                return answer
            s.visited = True

        next_moves = get_child_states(s)
        for node in next_moves:
            if node.visited is False:
                print(heuristic(node))
                if heuristic(node) == 0:
                    answer.append(node.move)
                    answer.pop(0)
                    print(answer)
                    return answer
                stack.append(node)
