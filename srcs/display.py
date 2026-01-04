from moovment import moov_snake
from texture import texture_init
import pygame
import time


# -- 6. The function that will luch with or without the pygame module, depending of the flag -- #
def display_map(grid, _game, model, flag, _data):
    if not flag:
        return (display_map_not_graphical(_game, grid, model, _data))
    return (display_map_graphical(_game, grid, model, _data))


# -- 7. This function the program without pygame, this is mostly use to train faster the model -- #
def display_map_not_graphical(_game, grid, model, _data):
    while True:
        grid = moov_snake(_game, grid, model, _data)
        if not grid:
            return False
        for lines in grid:
            print(lines)
        print('\n')


# -- 7. This one is to run with pygame, this is better to be able to see how is playing the snake -- #
def display_map_graphical(_game, grid, model, _data):
    width = len(grid[0]) * _game.tile_sprite
    height = len(grid) * _game.tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture_init(_game)
    run = True
    while run:
        grid = moov_snake(_game, grid, model, _data)
        if not grid:
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
