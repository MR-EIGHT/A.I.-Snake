import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple
import UI

ALF = 3

M_WIDTH = (UI.W_SIZE * 3) // 2 // 3
M_HEIGHT = UI.W_SIZE // 3


surface = create_example_window('Snake Game', (M_WIDTH, M_HEIGHT))
algorithm = 'A*'


def set_algorithm(selected: Tuple, val) -> None:
    global algorithm
    algorithm = selected[0][0]


def start_the_game() -> None:
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    """

    # menu.disable()
    menu.full_reset()
    UI.main(algorithm)
    menu.close()


menu = pygame_menu.Menu(
    height=M_HEIGHT,
    theme=pygame_menu.themes.THEME_DARK,  # you can set the menu's theme here.
    title='Snake Game',
    width=M_WIDTH
)

menu.add.selector('Algorithm: ', [('A*', 1), ('BFS', 2), ('DFS', 3), ('Human', 4)], onchange=set_algorithm)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


def show_menu():
    global surface
    surface = create_example_window('Snake Game', (M_WIDTH, M_HEIGHT))
    menu.mainloop(surface)
