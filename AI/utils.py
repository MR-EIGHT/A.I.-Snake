import snakegame as sg
from copy import deepcopy


class Node:
    """Search Tree Node
        this class is used to record complete state and moves taken to that states from start to form a search tree
    Returns:
        Node: search tree node
    """
    
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
    """heuristic function
    this function calculates manhattan distance of the snake head from the apple

    Args:
        node (Node): current game state

    Returns:
        int: manhattan distance from snakes head to the apple on the board
    """
    state: sg.SnakeGame = node.state

    x_dist = abs(state.head[0] - state.apple[0])
    y_dist = abs(state.head[1] - state.apple[1])

    return x_dist + y_dist


def collect_answer(n: Node):
    """Collect answer moves
    by walking through search tree from goal node to root using node.parent field

    Args:
        n (Node): goal node

    Returns:
        list: list of moves that leads snake to eat the apple
    """
    answer = []
    cur = n
    while cur:
        answer.append(cur.move)
        cur = cur.parent
    answer.pop()
    answer.reverse()
    return answer


def get_child_states(root: Node) -> list:
    """Returns branchings of root node
    by creating 4 copies up, down, right, left and trying to moves the snake to that direction

    Args:
        root (Node): an states of the game

    Returns:
        list: list of new states of the game branched from 'root'
    """
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
