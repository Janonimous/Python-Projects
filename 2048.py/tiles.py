import pygame

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
        self.mergable = True

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def set_space(self, space):
        self.space = space

    def set_type(self, type):
        if type != self.type:
            self.set_color(type)
        self.type = type

    def set_color(self, type):
        self.color = tile.tile_colors[type]

    def set_mergable(self, bool):
        self.mergable = bool

    def get_space(self):
        return self.space

    def get_type(self):
        return self.type

    def get_color(self):
        color = tile.tile_colors[self.type]
        return color

    def get_mergable(self):
        return self.mergable

    def find_mergable_tiles(num_rows, num_cols, direction):
        tiles = []
        if direction == 'up' or direction == 'down':
            for r in range(num_rows-1):
                for c in range(num_cols):
                    if direction == 'up':
                        tiles.append((r+1)*num_cols+c+1)
                    if direction == 'down':
                        tiles.append(r*num_cols+c+1)
        if direction == 'left' or direction == 'right':
            for r in range(num_rows):
                for c in range(num_cols-1):
                    if direction == 'left':
                        tiles.append(r*num_cols+c+2)
                    if direction == 'right':
                        tiles.append(r*num_cols+c+1)
        return tiles

    def shift(direction, board, board_layout, spaces_list):
        rows, cols = len(board_layout), len(board_layout[0])
        spaces = rows * cols
        for space in range(spaces):
            space += 1
            if board[space]['obj'] != None:
                obj = board[space]['obj']
                prev_space = next_space = obj.get_space()
                num_rows = len(board_layout)
                num_cols = len(board_layout[0])
                if direction == "up":
                    for c in range(num_cols):
                        next_space -= num_rows
                        if (next_space <= 0):
                            next_space += num_rows
                            break
                        if board[next_space]["obj"] != None:
                            next_space += num_rows
                            break
                if direction == "down":
                    for c in range(num_cols):
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
                        if ((next_space % num_cols) == 0):
                            next_space += 1
                            break
                        if board[next_space]["obj"] != None:
                            next_space += 1
                            break
                if direction == "right":
                    for r in range(num_rows):
                        next_space = prev_space +1
                        if ((prev_space % num_cols) == 0):
                            next_space -= 1
                            break
                        if board[next_space]["obj"] != None:
                            next_space -= 1
                            break

                if prev_space != next_space:
                    new_coords = board[next_space]["coords"]
                    obj.set_pos(new_coords[0], new_coords[1])
                    obj.set_space(next_space)
                    board[next_space]["obj"] = obj
                    board[prev_space]["obj"] = None
                    tile.check_spaces(board, spaces_list)

    def merge(direction, board, board_layout, tiles_list):
        num_rows = len(board_layout)
        num_cols = len(board_layout[0])
        mergable_tiles = tile.find_mergable_tiles(num_rows, num_cols, direction)
        for space in mergable_tiles:
            cur_tile = board[space]['obj']
            if cur_tile != None:
                if direction == 'up':
                    next_space = space - num_rows
                if direction == 'down':
                    next_space = space + num_rows
                if direction == 'left':
                    next_space = space -1
                if direction == 'right':
                    next_space = space +1
                next_tile = board[next_space]['obj']
                if next_tile != None:
                    if cur_tile.get_type() == next_tile.get_type():
                        for t in tiles_list:
                            if t == next_tile:
                                tiles_list.remove(t)
                        del next_tile
                        cur_tile.set_type(cur_tile.get_type()*2)
                        board[next_space]['obj'] = cur_tile
                        board[space]['obj'] = None



    def check_spaces(board, spaces_list):
        spaces_list.clear()
        for key in board:
            if board[key]["obj"] == None:
                spaces_list.append(key)

    def display(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
