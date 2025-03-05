import pygame
import random
from elements import tile_empty, tile_mine, tile_exploded, tile_flag, tile_unknown, tile_numbers

class Tile:
    def __init__(self, x, y, image, type, tile_size, revealed=False, flagged=False):
        self.x = x * tile_size
        self.y = y * tile_size
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
        self.tile_size = tile_size

    def draw(self, board_surface):
        if self.revealed:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.flagged:
            board_surface.blit(tile_flag, (self.x, self.y))
        else:
            board_surface.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        return self.type

class Board:
    def __init__(self, rows, cols, amount_mines, tile_size):
        self.rows = rows
        self.cols = cols
        self.amount_mines = amount_mines
        self.tile_size = tile_size
        self.board_surface = pygame.Surface((tile_size * cols, tile_size * rows))
        self.board_list = [
            [Tile(col, row, tile_empty, ".", tile_size) for row in range(rows)]
            for col in range(cols)
        ]
        self.place_mines()
        self.place_clues()
        self.dug = []

    def place_mines(self):
        for _ in range(self.amount_mines):
            while True:
                x = random.randint(0, self.cols - 1)
                y = random.randint(0, self.rows - 1)
                if self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break

    def place_clues(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board_list[x][y].type != "X":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines - 1]
                        self.board_list[x][y].type = "C"

    @staticmethod
    def is_inside(x, y, rows, cols):
        return 0 <= x < cols and 0 <= y < rows

    def check_neighbours(self, x, y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if self.is_inside(nx, ny, self.rows, self.cols):
                    if self.board_list[nx][ny].type == "X":
                        count += 1
        return count

    def draw(self, screen):
        for col in self.board_list:
            for tile in col:
                tile.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))

    def dig(self, x, y):
        self.dug.append((x, y))
        if self.board_list[x][y].type == "X":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded
            return False
        self.board_list[x][y].revealed = True
        if self.board_list[x][y].type == "C":
            return True
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (nx, ny) not in self.dug and self.is_inside(nx, ny, self.rows, self.cols):
                    self.dig(nx, ny)
        return True
