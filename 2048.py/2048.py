#!/usr/bin/env/python3.9

import pygame, sys, random, math
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Get Angle Test')
screen = pygame.display.set_mode((1000, 1000), 0, 32)

'''
    tile colors (238, 228, 218), (237, 224, 200),
    (242, 177, 121), (245, 249, 99), (246, 124, 95), (246, 94, 59),
    (237, 207, 114), (237, 204, 97), (237, 200, 80), (237, 197, 63), (237, 194, 96)
'''

class tile:

    def __init__(self, x, y, width, height, type, multiplier=1):
        self.x = x * multiplier + 125
        self.y = y * multiplier + 125
        self.width = width
        self.height = height
        self.type = type
        self.multiplier = multiplier # for displaying purposes
        self.rect = pygame.Rect(self.x, self.y, width, height)

board = {1: (1,1), 2: (2,1), 3: (3,1), 4: (4,1),
        5: (1,2), 6: (2,2), 7: (3,2), 8: (4,2),
        9: (1,3), 10: (2,3), 11: (3,3), 12: (4,3),
        13: (1,4), 14: (2,4), 15: (3,4), 16: (4,4)}

available_spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

tiles = []
start = True

def generate_tile():
    if len(available_spaces) != 0:
        board_space = random.choice(available_spaces)
        x, y = board[board_space]
        t_obj = tile(x, y, 125, 125, 2, 125)
        tiles.append(t_obj)
        available_spaces.pop(available_spaces.index(board_space))


while True:

    screen.fill((249, 249, 239))

    if start:
        for t in range(2):
            generate_tile()
        start = False

    board_rect = pygame.Rect(250, 250, 500, 500)
    pygame.draw.rect(screen, (187, 173, 160), board_rect)

    for t in tiles:
        pygame.draw.rect(screen, (238, 228, 218), t.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:
                start = True
                tiles.clear()
                available_spaces.clear()
                for i in range(16):
                    available_spaces.append(i+1)


    pygame.display.update()
    clock.tick(60)
