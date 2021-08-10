#!/usr/bin/env/python3.9

import pygame, sys, random, math
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('2048')
screen = pygame.display.set_mode((1000, 1000), 0, 32)

'''
    tile colors (238, 228, 218), (237, 224, 200),
    (242, 177, 121), (245, 249, 99), (246, 124, 95), (246, 94, 59),
    (237, 207, 114), (237, 204, 97), (237, 200, 80), (237, 197, 63), (237, 194, 96)
'''

class tile:

    tile_colors = {2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 249, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
    256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 96)}

    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.offset = [0, 0]
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.color = self.get_color()

    def get_color(self):
        color = tile.tile_colors[self.type]
        return color

    def display(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

rows = 4 # length of columns
columns = 4 # length of rows
board_layout = [[y+(x*4)+1 for y in range(columns)] for x in range(rows)]
board = {}
for i in range(rows*columns):
    x = ((i % rows) * 125) + 250
    y = (((i - (i % columns)) // 4) * 125) + 250
    board[i+1] = {}
    board[i+1]["coords"], board[i+1]["open"] = (x, y), True

tiles = []
available_spaces = []
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
        t_obj = tile(x, y, 125, 125, 2)
        tiles.append(t_obj)
        available_spaces.pop(available_spaces.index(board_space))

check_spaces()


while True:

    screen.fill((249, 249, 239))

    if start:
        for t in range(2):
            generate_tile()
        start = False

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

            if event.key == K_1:
                start = True
                tiles.clear()
                available_spaces.clear()
                for i in range(16):
                    available_spaces.append(i+1)
            if event.key == K_2:
                start = True


    pygame.display.update()
    clock.tick(60)
