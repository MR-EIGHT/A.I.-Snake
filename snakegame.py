import numpy as np
import random

UP = np.array([0, -1])
DOWN = np.array([0, 1])
RIGHT = np.array([1, 0])
LEFT = np.array([-1, 0])


class SnakeGame:

    def __init__(self, scale) -> None:
        self.scale = scale
        self.upper_bound = np.array([scale, scale])
        self.lower_bound = np.array([0, 0])
        self.eaten = False
        # self.board = [[0] * scale] * scale
        # self.board = [[0 for i in range(scale)] for j in range(scale)]
        self.body = []
        center = scale // 2
        self.head = np.array([center, center])
        # self.board[self.head[0]][self.head[1]] = 1
        self.spawn_apple()
        self.len = 0
        self.total_moves = 0

    def spawn_apple(self):
        while True:
            # create a random apple
            apple = np.array([random.randint(0, self.scale - 1), random.randint(0, self.scale - 1)])
            # check if apple didn't fall on snakes head
            if (apple == self.head).all():
                continue
            # check if apple didn't fall on snakes body
            failed = False
            for bodypart in self.body:
                if (bodypart == apple).all():
                    failed = True
                    break

            # accept apple and return
            if not failed:
                self.apple = apple
                break
        self.eaten = False

    def move(self, move):
        # storing head for later
        new_head = np.copy(self.head)

        # change head position
        # if move == Move.Up:
        #     new_head[1] += Move.Up
        # if move == Move.Down:
        #     new_head[1] += Move.D
        # if move == Move.Right:
        #     new_head[0] += 1
        # if move == Move.Left:
        #     new_head[0] -= 1
        new_head += move

        # check for Border Collision
        if (new_head >= self.upper_bound).any() or (new_head < self.lower_bound).any():
            return False

        # check for Body Collision
        for bodypart in self.body:
            if (new_head == bodypart).all():
                return False

        # if self.board[new_head[0]][new_head[1]] == 1:
        #     return False

        # check for Apple Eating
        grow = False
        if (new_head == self.apple).all():
            if self.len != 0:
                self.body.append(
                    self.body[self.len - 1].copy()
                )
            else:
                self.body.append(
                    self.head.copy()
                )
            self.len += 1
            self.eaten = True
            grow = True

        prev = self.head
        self.head = new_head

        self.total_moves += 1
        
        # moving body forward
        if self.len > 0:
            if grow:
                r = self.len - 1
                self.total_moves = 0
            else:
                r = self.len

            for i in range(0, r):
                new_pos = prev
                prev = self.body[i]
                self.body[i] = new_pos

        # # cleaning tail cell in board
        # if not grow:
        #     tail = prev
        #     self.board[tail[0]][tail[1]] = 0

        # # mark new head possition on board
        # self.board[self.head[0]][self.head[1]] = 1
        # self.print_board()
        return True

    def print_board(self):
        scale = self.scale
        head = self.head
        apple = self.apple

        # create empty board
        board = np.zeros((scale, scale), dtype=int)
        # mark head
        board[head[0]][head[1]] = 1
        # mark body
        for bodypart in self.body:
            board[bodypart[0]][bodypart[1]] = 1
        # mark apple
        board[apple[0]][apple[1]] = 2

        # print board
        for y in range(scale):
            for x in range(scale):
                print(board[x][y], " ", end='')
            print()
        print()


# sg = SnakeGame(11)

# sg.move(Down)
# sg.move(Down)
# sg.move(Down)
# sg.move(Down)
# sg.move(Down)
# sg.move(Down)

# sg.print_board()
