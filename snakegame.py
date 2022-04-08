import numpy as np
import random

# constats for snake moves
UP = np.array([0, -1])
DOWN = np.array([0, 1])
RIGHT = np.array([1, 0])
LEFT = np.array([-1, 0])


class SnakeGame:
    """Snake Game class

    SnakeGame class creates and records a new snake game state and provides methods for playing the game

    Returns:
    SnakeGame: snake game object storing current game state like snake body and head possition on the board, total moves, snake length and some other data
    """

    def __init__(self, scale) -> None:
        self.scale = scale
        self.upper_bound = np.array([scale, scale])
        self.lower_bound = np.array([0, 0])
        self.eaten = False
        self.body = []
        center = scale // 2
        self.head = np.array([center, center])
        self.spawn_apple()
        self.len = 0
        self.total_moves = 0

        
    def spawn_apple(self):
        """Apple spawner
            spawns a new apple on the board
        """
        
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

        
    def move(self, move) -> bool:
        """Move snake
            moves snake head to specified direction if possible and returns True, otherwise returns false
        """
        
        # storing head for later
        new_head = np.copy(self.head)

        # moving new_head
        new_head += move

        # check for Border Collision
        if (new_head >= self.upper_bound).any() or (new_head < self.lower_bound).any():
            return False

        # check for Body Collision
        for bodypart in self.body:
            if (new_head == bodypart).all():
                return False


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

        # increase total moves of the snake
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

        return True