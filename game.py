# import pygame
import random
import enum

class Move(enum.Enum):
    Up = 1
    Down = 2
    Right = 3
    Left = 4
class SnakeGame:
    
    def __init__(self, scale) -> None:
        self.scale = scale
        # self.board = [[0] * scale] * scale
        self.board = [[0 for i in range(scale)] for j in range(scale)]
        self.body = []
        center = int(scale / 2)
        self.head = [center, center]
        self.board[self.head[0]][self.head[1]] = 1
        self.len = 0
        
    
    def spawn_apple(self):
        spawned = False
        while not spawned:
            apple = [random.randint(0, self.scale-1), random.randint(0, self.scale-1)]
            if self.board[apple[0]][apple[1]] == 0:
                self.apple = apple
                self.board[apple[0]][apple[1]] = 2
                spawned = True
                
    def move(self, move: Move):
        # storing head for later
        new_head = self.head.copy()

        # change head position
        if move == Move.Up:
            new_head[1] -= 1
        if move == Move.Down:
            new_head[1] += 1
        if move == Move.Right:
            new_head[0] += 1
        if move == Move.Left:
            new_head[0] -= 1
        
        # check for Border Collision
        if new_head[0] >= self.scale or new_head[0] < 0 or new_head[1] >= self.scale or new_head[1] < 0:
            return False
        
        # check for Body Collision
        if self.board[new_head[0]][new_head[1]] == 1:
            return False

        # check for Apple Eating
        grow = False
        if self.board[new_head[0]][new_head[1]] == 2:
            if self.len != 0:
                self.body.append(
                    self.body.append(self.body[self.len-1].copy())
                )
            else:
                self.body.append(
                    self.head.copy()
                )
            self.len += 1
            grow = True
        
        prev = self.head
        self.head = new_head
        
        # moving body forward
        if self.len > 0:
            if grow:
                r = self.len - 1
            else:
                r = self.len
            
            for i in range(0, r):
                new_pos = prev
                prev = self.body[i].copy()
                self.body[i] = new_pos
        
        # cleaning tail cell in board
        if not grow:
            tail = prev
            self.board[tail[0]][tail[1]] = 0
        
        # mark new head possition on board
        self.board[self.head[0]][self.head[1]] = 1

        return True

    def print_board(self):
        for y in range(self.scale):
            for x in range(self.scale):
                print(self.board[x][y], " ", end='')
            print()
        print()
