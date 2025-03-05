import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BGCOLOUR = DARKGREY

TILESIZE = 32
FPS = 60
TITLE = "Minesweeper Clone"

DIFFICULTY_LEVELS = {
    'easy': {'rows': 8, 'cols': 8, 'mines': 10, 'time': 300},  
    'medium': {'rows': 12, 'cols': 12, 'mines': 20, 'time': 500}, 
    'hard': {'rows': 15, 'cols': 15, 'mines': 40, 'time': 800}, 
}

current_difficulty = 'medium'
ROWS = DIFFICULTY_LEVELS[current_difficulty]['rows']
COLS = DIFFICULTY_LEVELS[current_difficulty]['cols']
AMOUNT_MINES = DIFFICULTY_LEVELS[current_difficulty]['mines']
TIME_LIMIT = DIFFICULTY_LEVELS[current_difficulty]['time']

WIDTH = TILESIZE * COLS
HEIGHT = TILESIZE * ROWS

tile_numbers = [pygame.transform.scale(
    pygame.image.load(os.path.join("assets", f"Tile{i}.png")), (TILESIZE, TILESIZE))
    for i in range(1, 9)]
tile_empty = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileUnknown.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TileNotMine.png")), (TILESIZE, TILESIZE))
