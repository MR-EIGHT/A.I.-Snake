from heapq import *
from logging import root

from snakegame import SnakeGame

from .utils import *

import UI as ui
import pygame


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
    visited = set()
    visited.add(root_state.head)
    heapify(state_list)

    # adding root state to priority queue
    h = heuristic(root_state)
    g = 0
    heappush(state_list, (h + g, root_state))

    # fetching nodes with minimum heuristic and move count and checking if they're the answer, otherwise pushing them to priority queue
    while len(state_list) != 0:
        heapify(state_list)
        (f, nm) = heappop(state_list)
        
        next_moves = get_child_states(nm)

        for n in next_moves:
            if n.head in visited:
                print(n.head, " was visited")
                continue
            visited.add(n.head)
            
            # draw heatmap
            pygame.time.delay(50)
            # ui.clock.tick(5)
            draw_circle(n.state)
            draw_total_moves(n)
            
            h = heuristic(n)
            if h == 0:
                return collect_answer(n)
            g = n.state.total_moves
            f = h*2 + g
            heappush(state_list, (f, n))



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