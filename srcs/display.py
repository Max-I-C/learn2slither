from moovment import moov_snake
from texture import texture_init
import pygame
import time

# -- 7.
def display_map_not_graphical(_game, grid, model, _data):
    while True:
        grid = moov_snake(_game, grid, model, _data)
        if (grid == False):
            return False
        for lines in grid :
            print(lines)
        print('\n')

# -- 7.
def display_map_graphical(_game, grid, model, _data):
    width = len(grid[0]) * _game.tile_sprite
    height = len(grid) * _game.tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture_init(_game)
    run = True
    while run:
        grid = moov_snake(_game, grid, model, _data)
        if (grid == False):
            return False
        time.sleep(0.1)
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char == "1":
                    screen.blit(dico_texture[2], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "P":
                    screen.blit(dico_texture[0], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "S":
                    screen.blit(dico_texture[1], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "0":
                    screen.blit(dico_texture[3], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "R":
                    screen.blit(dico_texture[4], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "G":
                    screen.blit(dico_texture[5], (j * _game.tile_sprite, i * _game.tile_sprite))
        pygame.display.flip()
    pygame.quit()

# -- 6.
def display_map(grid, _game, model, flag, _data):
    if (flag == False):
        return(display_map_not_graphical(_game, grid, model, _data))
    return(display_map_graphical(_game, grid, model, _data))