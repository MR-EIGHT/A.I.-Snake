from logging import error
import random
import pygame
import tkinter as tk
from tkinter import messagebox

import Menu
import snakegame as sg
from AI import astar
from AI import bfs

SNAKE_COLOR = (255, 0, 0)
APPLE_COLOR = (0, 255, 0)

SCALE = 8
W_SIZE = 500
CUBE = W_SIZE // SCALE

game_display = None

SNAKE_HEAD = pygame.transform.scale(
    pygame.image.load('./assets/head.png'),
    (CUBE, CUBE)
)
SNAKE_BODY = pygame.transform.scale(
    pygame.image.load('./assets/body.png'),
    (CUBE, CUBE)
)
SNAKE_BEND = pygame.transform.scale(
    pygame.image.load('./assets/bend.png'),
    (CUBE, CUBE)
)
SNAKE_TAIL = pygame.transform.scale(
    pygame.image.load('./assets/tail.png'),
    (CUBE, CUBE)
)

APPLE = pygame.transform.scale(
    pygame.image.load("./assets/apple.png"),
    (CUBE, CUBE)
)


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


def redraw_window(surface, move):
    global snake_game
    surface.fill((60, 60, 60))
    draw_snake(surface, move)
    draw_apple(surface)
    # draw_grid(wsize, scale, surface)
    pygame.display.update()
    pass


last_rot = 0


def transform_body(start, end):
    global last_rot
    (h_i, h_j) = start
    (b_i, b_j) = end

    body_img = None
    if h_i > b_i and h_j == b_j:
        body_img = pygame.transform.rotate(SNAKE_BODY, -90)
        last_rot = -90
    elif h_i < b_i and h_j == b_j:
        body_img = pygame.transform.rotate(SNAKE_BODY, 90)
        last_rot = 90
    elif h_i == b_i and h_j < b_j:
        body_img = pygame.transform.rotate(SNAKE_BODY, 0)
        last_rot = 0
    elif h_i == b_i and h_j > b_j:
        body_img = pygame.transform.rotate(SNAKE_BODY, 180)
        last_rot = 180
    elif h_i > b_i and h_j < b_j:
        if last_rot == 0:
            body_img = pygame.transform.flip(SNAKE_BEND, True, False)
            body_img = pygame.transform.rotate(body_img, -90)
            last_rot = 90
        else:
            body_img = SNAKE_BEND
            last_rot = 0
    elif h_i < b_i and h_j < b_j:
        if last_rot == 90:
            body_img = pygame.transform.flip(SNAKE_BEND, True, False)  # ------
            last_rot = 0
        else:
            body_img = pygame.transform.rotate(SNAKE_BEND, 90)
            last_rot = 90  # newnwnwnwnw
    elif h_i > b_i and h_j > b_j:
        if last_rot == -90 or last_rot == 90:
            body_img = pygame.transform.flip(SNAKE_BEND, False, True)
            last_rot = 180
        else:
            body_img = pygame.transform.rotate(SNAKE_BEND, -90)
            last_rot = -90
    else:
        if last_rot == 180:
            body_img = pygame.transform.rotate(SNAKE_BEND, -90)
            body_img = pygame.transform.flip(body_img, True, False)
            last_rot = 90

            # last_rot = 90
        else:
            body_img = pygame.transform.rotate(SNAKE_BEND, 180)
            last_rot = 180

    return body_img


def draw_snake(surface, move):
    global snake_game

    # draw head
    head = snake_game.head
    i = head[0]
    j = head[1]

    head_img = None
    global last_rot
    if (move == sg.UP).all():
        last_rot = 0
        head_img = SNAKE_HEAD
    elif (move == sg.DOWN).all():
        last_rot = 180.0
        head_img = pygame.transform.rotate(SNAKE_HEAD, 180.0)
    elif (move == sg.RIGHT).all():
        last_rot = -90
        head_img = pygame.transform.rotate(SNAKE_HEAD, -90.0)
    else:
        last_rot = 90
        head_img = pygame.transform.rotate(SNAKE_HEAD, 90.0)

    game_display.blit(head_img, (i * CUBE, j * CUBE))
    # pygame.draw.rect(surface, SNAKE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))
    # cntr = cube // 2
    # radius = 3
    # circle_middle = (i * cube + cntr - radius, j * cube + 8)
    # circle_middle2 = (i * cube + cube - radius * 2, j * cube + 8)
    # pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
    # pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)

    if snake_game.len == 0:
        return

    # draw tail
    if snake_game.len == 1:
        (i, j) = snake_game.body[snake_game.len - 1]
        tail_img = pygame.transform.rotate(SNAKE_TAIL, last_rot)
        game_display.blit(tail_img, (i * CUBE, j * CUBE))
        return

    # draw neck
    neck_img = transform_body(snake_game.head, snake_game.body[1])
    (i, j) = snake_game.body[0]
    game_display.blit(neck_img, (i * CUBE, j * CUBE))

    # draw body parts
    for x in range(1, snake_game.len - 1):
        (i, j) = snake_game.body[x]
        start = snake_game.body[x - 1]
        end = snake_game.body[x + 1]
        body_img = transform_body(start, end)
        game_display.blit(body_img, (i * CUBE, j * CUBE))

    # draw tail
    (i, j) = snake_game.body[snake_game.len - 1]
    (b_i, b_j) = snake_game.body[snake_game.len - 2]
    tail_img = None
    if i > b_i:
        tail_img = pygame.transform.rotate(SNAKE_TAIL, 90)
    elif i < b_i:
        tail_img = pygame.transform.rotate(SNAKE_TAIL, -90)
    elif j > b_j:
        tail_img = SNAKE_TAIL
    else:
        tail_img = pygame.transform.rotate(SNAKE_TAIL, 180)
    game_display.blit(tail_img, (i * CUBE, j * CUBE))
    # for body_part in snake_game.body:
    #     i = body_part[0]
    #     j = body_part[1]
    #     pygame.draw.rect(surface, SNAKE_COLOR, (i * CUBE + 1, j * CUBE + 1, CUBE - 2, CUBE - 2))
    #     pygame.draw.rect(surface, SNAKE_COLOR, (i * CUBE + 1, j * CUBE + 1, CUBE - 2, CUBE - 2))


def draw_apple(surface):
    global snake_game

    # draw apple
    apple = snake_game.apple
    i = apple[0]
    j = apple[1]
    game_display.blit(APPLE, (i * CUBE, j * CUBE))
    # pygame.draw.rect(surface, APPLE_COLOR, (i * cube + 1, j * cube + 1, cube - 2, cube - 2))


def random_snack(item):
    positions = item.body
    while True:
        x = random.randrange(SCALE)
        y = random.randrange(SCALE)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y


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
    Menu.show_menu()


def main(algo='A*'):
    global snake_game, game_display

    game_display = pygame.display.set_mode((W_SIZE, W_SIZE), depth=2)
    clock = pygame.time.Clock()

    while True:
        snake_game = sg.SnakeGame(SCALE)
        last_move = sg.UP

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # spawn a new apple
            if snake_game.eaten:
                snake_game.spawn_apple()

            redraw_window(game_display, last_move)
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
                last_move = m
                pygame.time.delay(100)  # lowering this will make it faster
                clock.tick(5)  # lowering this will make it slower

                cm = snake_game.move(m)
                # if not cm:
                #     cm = snake_game.move(m)
                redraw_window(game_display, m)

                if not cm:
                    error("Something went wrong with the algorithm solution")
                    pygame.quit()
                    break


if __name__ == '__main__':
    Menu.show_menu()
    # main('BFS')
