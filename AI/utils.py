import snakegame as sg
from copy import deepcopy


class Node:
    def __init__(self, state, parent, move=None):
        self.move = move
        self.state = state
        self.parent = parent
        self.visited = False

    def __lt__(self, nxt):
        return False

    def __eq__(self, __o: object) -> bool:
        return True


def heuristic(node: Node):
    state: sg.SnakeGame = node.state

    x_dist = abs(state.head[0] - state.apple[0])
    y_dist = abs(state.head[1] - state.apple[1])

    return x_dist + y_dist


def collect_answer(n: Node):
    answer = []
    cur = n
    while cur:
        answer.append(cur.move)
        cur = cur.parent
    answer.pop()
    answer.reverse()
    return answer


def get_child_states(root: Node) -> list[Node]:
    children = []
    up = deepcopy(root.state)
    down = deepcopy(root.state)
    right = deepcopy(root.state)
    left = deepcopy(root.state)

    if up.move(sg.UP):
        children.append(
            Node(up, root, sg.UP)
        )
    if down.move(sg.DOWN):
        children.append(
            Node(down, root, sg.DOWN)
        )
    if right.move(sg.RIGHT):
        children.append(
            Node(right, root, sg.RIGHT)
        )
    if left.move(sg.LEFT):
        children.append(
            Node(left, root, sg.LEFT)
        )

    return children
