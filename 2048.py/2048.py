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

    def move(self, direction, board, board_layout):
        space = self.space
        num_rows = len(board_layout)
        num_columns = len(board_layout[0])
        if direction == "up":
            while True:
                next_space = space - num_rows
                if next_space <= 0:
                    break
                if board[next_space]["open"]:
                    space = next_space
        if direction == "down":
            while True:
                next_space = space + num_rows
                if next_space > len(board):
                    break
                if board[next_space]["open"]:
                    space = next_space
        row_num = (space-1) // num_columns
        relative_space = ((space-1) % num_columns) +1
        if direction == "left":
            while True:
                next_space = relative_space -1
                if next_space <= 0:
                    break
                if board[next_space]["open"]:
                    space = next_space
        if direction == "right":
            while True:
                next_space = relative_space +1
                if next_space > num_columns:
                    break
                if board[next_space]["open"]:
                    space = next_space

        new_coords = board[space]["coords"]
        self.set_pos(new_coords[0], new_coords[1])
        self.set_space(space)
        board[space]["open"] = False

        # move tile and at the tile's new space set the board at that space to closed (open: False)


    def display(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

space_length = 125

rows = 4 # length of columns
columns = 4 # length of rows
board_layout = [[y+(x*4)+1 for y in range(columns)] for x in range(rows)]
print(board_layout)
board = {}
for i in range(rows*columns):
    x = ((i % rows) * space_length) + 250
    y = (((i - (i % columns)) // 4) * space_length) + 250
    board[i+1] = {}
    board[i+1]["coords"], board[i+1]["open"] = (x, y), True
print(board)

tiles = []
available_spaces = []
move_directions = {"up": False, "down": False, "left": False, "right": False}
start = True

def check_spaces():
    #available_spaces = [key for key in board if board[key]["open"] == True]
    for key in board:
        if board[key]["open"] == True:
            available_spaces.append(key)

def generate_tile():
    if len(available_spaces) != 0:
        board_space = random.choice(available_spaces)
        x, y = board[board_space]["coords"]
        t_obj = tile(x, y, space_length, space_length, board_space, 2)
        tiles.append(t_obj)
        available_spaces.pop(available_spaces.index(board_space))

check_spaces()


while True:

    screen.fill((249, 249, 239))

    if start:
        for t in range(2):
            generate_tile()
        start = False

    for direction in move_directions:
        if direction:
            

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

            if event.key == K_UP:
                move_directions["up"] = True
            if event.key == K_DOWN:
                move_directions["down"] = True
            if event.key == K_RIGHT:
                move_directions["right"] = True
            if event.key == K_LEFT:
                move_directions["left"] = True

            if event.key == K_1:
                start = True
                tiles.clear()
                available_spaces.clear()
                for i in range(16):
                    available_spaces.append(i+1)
            if event.key == K_2:
                generate_tile()

        if event.type == KEYUP:
            if event.key == K_UP:
                move_directions["up"] = True
            if event.key == K_DOWN:
                move_directions["down"] = True
            if event.key == K_RIGHT:
                move_directions["right"] = True
            if event.key == K_LEFT:
                move_directions["left"] = True


    pygame.display.update()
    clock.tick(60)
