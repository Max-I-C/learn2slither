from graphic import texture
from moovment import moov_snake
from model import create_model
from generation import generate_map 
import pygame
import time
import numpy as np
import pdb

class MyGame():
    def __init__(self):
        self.tile_sprite = 64
        self.snake_xpos = 0
        self.snake_ypos = 0
        self.snake_len = []

def display_map(grid, _game, model):
    for lines in grid:
        print("first verif", lines)
    width = len(grid[0]) * _game.tile_sprite
    height = len(grid) * _game.tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture.texture_init(_game)
    run = True
    while run:
        grid = moov_snake(_game, grid, width, height, model)
        if (grid == False):
            return False
        time.sleep(1)
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

def main():
    print("Main")
    _game = MyGame()
    model = create_model(input_size=40, output_size=4)
    while True:
        grid = generate_map(10, 10, _game)
        if (display_map(grid, _game, model) == True):
            break
    print("End of the training model.")
    

if(__name__ == "__main__"):
    main()
