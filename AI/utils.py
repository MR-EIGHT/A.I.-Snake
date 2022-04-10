from math import sqrt
import snakegame as sg
from copy import deepcopy

from snakegame import SnakeGame
import pygame
import UI as ui

class Node:
    """Search Tree Node
        this class is used to record complete state and moves taken to that states from start to form a search tree
    Returns:
        Node: search tree node
    """

    def __init__(self, state: sg.SnakeGame, parent, move=None):
        self.move = move
        self.head = str([state.head[0], state.head[1]])
        print(self.head)
        self.state = state
        self.parent = parent

    def __lt__(self, nxt):
        return False

    def __eq__(self, __o: object) -> bool:
        return True

def g_dist(start: Node, end: Node):
    start_s = start.state
    end_s = end.state
    x_dist = abs(start_s.head[0] - end_s.head[0])
    y_dist = abs(start_s.head[1] - end_s.head[1])
    
    return x_dist + y_dist

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

    return sqrt(x_dist*x_dist + y_dist*y_dist)


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
    up = sg.SnakeGame.snapshot(root.state)
    down = sg.SnakeGame.snapshot(root.state)
    right = sg.SnakeGame.snapshot(root.state)
    left = sg.SnakeGame.snapshot(root.state)

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


def draw_total_moves(n: Node):
    font = pygame.font.Font('freesansbold.ttf', 20)
    game: SnakeGame = n.state
    cord = get_cord(game)
    text = font.render(str(game.total_moves).zfill(2), True, (0,0,0), (255,255,255))
    textRect = text.get_rect()
    textRect.topleft = cord
    ui.game_display.blit(text, textRect)

def draw_circle(game: SnakeGame):
    (i, j) = game.head
    s = pygame.Surface((ui.CUBE, ui.CUBE))
    s.set_alpha(32)
    s.fill((255, 0, 0))
    ui.game_display.blit(s, get_cord(game))
    pygame.display.update()
    
    

def get_cord(game: SnakeGame):
    (i, j) = game.head
    # offset = ui.CUBE // 2
    offset = 0
    return (i*ui.CUBE + offset, j*ui.CUBE + offset)

MAX_MOVES = 20
def get_radius(game: SnakeGame):
    total_move = game.total_moves
    full_rad = ui.CUBE // 2
    rad = (full_rad // MAX_MOVES) * total_move
    return rad