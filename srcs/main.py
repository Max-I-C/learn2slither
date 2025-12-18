from graphic import texture
from moovment import moov_snake
from model import create_model
from generation import generate_map 
from tensorflow.keras.models import load_model
import pygame
import time
import numpy as np
import argparse
import pdb

class Dataset():
    def __init__(self):
        self.death_by_wall = 0
        self.death_by_snake = 0
        self.death_by_lenght = 0
        self.green_apple_eated = 0
        self.red_apple_eated = 0
    def __str__(self):
        return f"death_wall: {self.death_by_wall}, death_snake: {self.death_by_snake}, death_lenght: {self.death_by_lenght}, green_apple: {self.green_apple_eated}, red_apple: {self.red_apple_eated}"

class MyGame():
    def __init__(self):
        self.direction = 1
        self.epsilon = 1.0
        self.tile_sprite = 64
        self.snake_xpos = 0
        self.snake_ypos = 0
        self.green_x = 0
        self.green_y = 0
        self.snake_len = []

def display_map_not_graphical(_game, grid, model, _data):
    while True:
        grid = moov_snake(_game, grid, model, _data)
        if (grid == False):
            return False
        for lines in grid :
            print(lines)
        print('\n')

def display_map_graphical(_game, grid, model, _data):
    width = len(grid[0]) * _game.tile_sprite
    height = len(grid) * _game.tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture.texture_init(_game)
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

def display_map(grid, _game, model, flag, _data):
    if (flag == "no_graphical"):
        return(display_map_not_graphical(_game, grid, model, _data))
    else:
        return(display_map_graphical(_game, grid, model, _data))

def main():
    print("Main")
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_flag", default="graphical")
    args = parser.parse_args()
    _game = MyGame()
    _data = Dataset()
    try:
        model = load_model("snake_model.keras")
        print("Model loaded, continuing training....")
    except:
        model = create_model(input_size=40, output_size=4)
        print("New model created")
    episode = 0
    while True and episode < 1000:
        grid = generate_map(10, 10, _game)
        if (display_map(grid, _game, model, args.graph_flag, _data) == True):
            break
        if(episode % 100 == 0 and episode != 0):
            try:
                model.save("snake_model.keras")
                print("Saving the model at ", episode)
            except Exception as e:
                print("Problem while saving")
        episode += 1
        print(_data)
        _game.epsilon = max(0.05, 1.0 * (0.9995 ** episode))
    print("End of the training model.")
    

if(__name__ == "__main__"):
    main()
