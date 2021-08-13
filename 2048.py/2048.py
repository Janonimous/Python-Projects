#!/usr/bin/env/python3.9

import pygame, sys, random, math
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('2048')
screen = pygame.display.set_mode((1000, 1000), 0, 32)

''' May want to change tile nums to go from (0-15) instead of (1-16) '''

'''
    tile colors (238, 228, 218), (237, 224, 200),
    (242, 177, 121), (245, 249, 99), (246, 124, 95), (246, 94, 59),
    (237, 207, 114), (237, 204, 97), (237, 200, 80), (237, 197, 63), (237, 194, 96)
'''

class tile:

    tile_colors = {2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 249, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
    256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 96)}

    def __init__(self, x, y, width, height, space, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.space = space
        self.type = type
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.color = self.get_color()

    def get_color(self):
        color = tile.tile_colors[self.type]
        return color

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def set_space(self, space):
        self.space = space

    def set_type(self, type):
        self.type = type

    def merge(self):
        pass

    def move(self, direction, board, board_layout, obj):
        prev_space = self.space
        next_space = self.space
        num_rows = len(board_layout)
        num_columns = len(board_layout[0])
        if direction == "up":
            for c in range(num_columns):
                next_space -= num_rows
                if (next_space <= 0):
                    next_space += num_rows
                    break
                if board[next_space]["obj"] != None:
                    next_space += num_rows
                    break
        if direction == "down":
            for c in range(num_columns):
                next_space += num_rows
                if (next_space > len(board)):
                    next_space -= num_rows
                    break
                if board[next_space]["obj"] != None:
                    next_space -= num_rows
                    break
        if direction == "left":
            for r in range(num_rows):
                next_space = prev_space -1
                if ((next_space % num_columns) == 0):
                    next_space += 1
                    break
                if board[next_space]["obj"] != None:
                    next_space += 1
                    break
        if direction == "right":
            for r in range(num_rows):
                next_space = prev_space +1
                if ((prev_space % num_columns) == 0):
                    next_space -= 1
                    break
                if board[next_space]["obj"] != None:
                    next_space -= 1
                    break

        if prev_space != next_space:
            new_coords = board[next_space]["coords"]
            self.set_pos(new_coords[0], new_coords[1])
            self.set_space(next_space)
            board[next_space]["obj"] = obj
            board[prev_space]["obj"] = None
            check_spaces()

    def display(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

space_length = 125

rows = 4 # length of columns
columns = 4 # length of rows
board_layout = [[y+(x*4)+1 for y in range(columns)] for x in range(rows)]
board = {}
for i in range(rows*columns):
    x = ((i % rows) * space_length) + 250
    y = (((i - (i % columns)) // 4) * space_length) + 250
    board[i+1] = {}
    board[i+1]["coords"], board[i+1]["obj"] = (x, y), None
print(board)
print(board_layout)

tiles = []
available_spaces = []
move_directions = {"up": False, "down": False, "left": False, "right": False}
start = True

def check_spaces():
    #available_spaces = [key for key in board if board[key]["open"] == True]
    available_spaces.clear()
    for key in board:
        if board[key]["obj"] == None:
            available_spaces.append(key)

def generate_tile():
    if len(available_spaces) != 0:
        board_space = random.choice(available_spaces)
        x, y = board[board_space]["coords"]
        t_obj = tile(x, y, space_length, space_length, board_space, 2)
        tiles.append(t_obj)
        board[board_space]["obj"] = t_obj
        available_spaces.pop(available_spaces.index(board_space))

def refresh():
    tiles.clear()
    available_spaces.clear()
    for i in range(len(board)):
        available_spaces.append(i+1)
        board[i+1]["obj"] = None

check_spaces()


while True:

    screen.fill((249, 249, 239))

    check_spaces()

    if start:
        for t in range(2):
            generate_tile()
        start = False

    for direction in move_directions:
        if move_directions[direction]:
            for t in tiles:
                t.move(direction, board, board_layout, t)

    board_rect = pygame.Rect(250, 250, 500, 500)
    pygame.draw.rect(screen, (187, 173, 160), board_rect)

    for t in tiles:
        t.display(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_UP or event.key == K_w:
                move_directions["up"] = True
            if event.key == K_DOWN or event.key == K_s:
                move_directions["down"] = True
            if event.key == K_RIGHT or event.key == K_d:
                move_directions["right"] = True
            if event.key == K_LEFT or event.key == K_a:
                move_directions["left"] = True

            if event.key == K_1:
                start = True
                refresh()
            if event.key == K_2:
                generate_tile()

        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                move_directions["up"] = False
            if event.key == K_DOWN or event.key == K_s:
                move_directions["down"] = False
            if event.key == K_RIGHT or event.key == K_d:
                move_directions["right"] = False
            if event.key == K_LEFT or event.key == K_a:
                move_directions["left"] = False


    pygame.display.update()
    clock.tick(60)
