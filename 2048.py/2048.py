#!/usr/bin/env/python3.9

import pygame
import random
import sys
from tiles import tile
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('2048')
screen = pygame.display.set_mode((1000, 1000), 0, 32)
def short():
    pygame.quit()
    sys.exit()

space_length = 125

rows = 4 # length of columns
columns = 4 # length of rows
spaces = rows * columns
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
move = False

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

tile.check_spaces(board, available_spaces)

while True:

    screen.fill((249, 249, 239))

    tile.check_spaces(board, available_spaces)

    if start:
        for t in range(2):
            generate_tile()
        start = False

    if move:
        for direction in move_directions:
            if move_directions[direction]:
                for s in range(1, spaces+1):
                    tile.shift(direction, board, board_layout, available_spaces)
                    tile.merge(direction, board, board_layout, tiles)
                #generate_tile()


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
                move_directions["up"] = move = True
            if event.key == K_DOWN or event.key == K_s:
                move_directions["down"] = move = True
            if event.key == K_RIGHT or event.key == K_d:
                move_directions["right"] = move = True
            if event.key == K_LEFT or event.key == K_a:
                move_directions["left"] = move = True

            if event.key == K_1:
                start = True
                refresh()
            if event.key == K_2:
                generate_tile()

        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                move_directions["up"] = move = False
            if event.key == K_DOWN or event.key == K_s:
                move_directions["down"] = move = False
            if event.key == K_RIGHT or event.key == K_d:
                move_directions["right"] = move = False
            if event.key == K_LEFT or event.key == K_a:
                move_directions["left"] = move = False


    pygame.display.update()
    clock.tick(60)
