from logging import error
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import snakegame as sg
from AI import astar
from AI import bfs

SNAKE_COLOR = (255, 0, 0)
APPLE_COLOR = (0, 255, 0)


def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x += size_between
        y += size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

    pass


def redraw_window(surface):
    global scale, wsize, snake_game
    surface.fill((0, 0, 0))
    draw_snake(surface)
    draw_apple(surface)
    draw_grid(wsize, scale, surface)
    pygame.display.update()
    pass


def draw_snake(surface):
    global scale, wsize, snake_game

    # calculate cube size
    cube = wsize // scale

    # draw head
    head = snake_game.head
    i = head[0]
    j = head[1]
    pygame.draw.rect(surface, SNAKE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))
    cntr = cube // 2
    radius = 3
    circle_middle = (i * cube + cntr - radius, j * cube + 8)
    circle_middle2 = (i * cube + cube - radius * 2, j * cube + 8)
    pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
    pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)

    # draw
    for body_part in snake_game.body:
        i = body_part[0]
        j = body_part[1]
        pygame.draw.rect(surface, SNAKE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))
        pygame.draw.rect(surface, SNAKE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))


def draw_apple(surface):
    global scale, wsize, snake_game

    # calculate cube size
    cube = wsize // scale

    # draw apple
    apple = snake_game.apple
    i = apple[0]
    j = apple[1]
    pygame.draw.rect(surface, APPLE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))


def random_snack(item):
    global rows
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

    pass


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except Exception as e:
        print(e)

    pass


def game_over(snake):
    print("Score:", len(snake.body))
    message_box('You Win!', 'Play again...')


def main(algo='A*'):
    global scale, wsize, snake_game
    wsize = 500  # window width and height
    scale = 5  # game grid size

    win = pygame.display.set_mode((wsize, wsize), depth=2)
    clock = pygame.time.Clock()

    while True:
        snake_game = sg.SnakeGame(scale)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # spawn a new apple
            if snake_game.eaten:
                snake_game.spawn_apple()

            redraw_window(win)
            # solve

            if algo == 'BFS':
                print("<- Entering BFS")
                moves = bfs.solve_bfs(snake_game)
                print("-> Exiting BFS")

            else:
                print("<- Entering A*")
                # print("Apple: ", snake_game.apple)
                moves = astar.solve_astar(snake_game)

                print("-> Exiting A*")
            # if game ends
            if moves is None or len(moves) == 0:
                game_over(snake_game)
                break

            for m in moves:

                pygame.time.delay(100)  # lowering this will make it faster
                clock.tick(5)  # lowering this will make it slower

                cm = snake_game.move(m)
                # if not cm:
                #     cm = snake_game.move(m)
                redraw_window(win)

                if not cm:
                    error("Something went wrong with the algorithm solution")
                    pygame.quit()
                    break


if __name__ == '__main__':
    main('BFS')
