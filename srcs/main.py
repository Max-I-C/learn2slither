from graphic import texture
from moovment import moov_snake
from model import create_model
from generation import generate_map
from tensorflow.keras.models import load_model
import pygame
import time
import argparse
import json


class Model():
    def __init___(self):
        self.model = ""
        self.episode = 0

class Dataset():
    def __init__(self):
        self.all_game = 0
        self.death_by_wall = 0
        self.death_by_snake = 0
        self.death_by_lenght = 0
        self.green_apple_eated = 0
        self.red_apple_eated = 0

    def __str__(self):
        return (
            f"total_game: {self.all_game}, death_wall: {self.death_by_wall}, death_snake: {self.death_by_snake}, death_lenght: {self.death_by_lenght}, green_apple: {self.green_apple_eated}, red_apple: {self.red_apple_eated}"
            f"\n% of game loose by the wall: {(self.death_by_wall / self.all_game * 100) if self.all_game > 0 else 0:.2f}%"            
        )

class MyGame():
    def __init__(self):
        self.direction = 1
        self.epsilon = 0
        self.tile_sprite = 64
        self.snake_xpos = 0
        self.snake_ypos = 0
        self.green_apples = []
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

def collecting_data(_game, _model):
    try:
        with open(".prog_data.json") as f:
            data = json.load(f)
            _game.epsilon = data["epsilone"]
            _model.episode = data["episode"]
        print("Data found from the .json files")
    except:
        _game.epsilon = 1
        _episode = 0
        print("No epsilon data found")
    try:
        _model.model = load_model(f"models/snake_model_v2_{_model.episode}.keras")
        print("Model loaded, continuing training....")
    except:
        _model.model = create_model(input_size=40, output_size=4)
        print("New model created")

def main():
    print("Main")
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_flag", default="graphical")
    args = parser.parse_args()
    _game = MyGame()
    _data = Dataset()
    _model = Model()
    try:
        collecting_data(_game, _model)
    except:
        print("Error while collecting data")

    while True and _model.episode < 10000:
        grid = generate_map(10, 10, _game)
        if (display_map(grid, _game, _model.model, args.graph_flag, _data) == True):
            break
        if(_model.episode % 100 == 0 and _model.episode != 0):
            try:
                _model.model.save(f"models/snake_model_v2_{_model.episode}.keras")
                print("Saving the model at ", _model.episode)
                data = {"epsilone": _game.epsilon, "episode": _model.episode}
                with open(".prog_data.json", "w") as f:
                    json.dump(data, f)
            except Exception as e:
                print("Problem while saving")
        _model.episode += 1
        _data.all_game += 1
        print("nb of episode ", _model.episode)
        print(_data)
        _game.epsilon = max(0.02, _game.epsilon * 0.995)
    print("End of the training model.")


if(__name__ == "__main__"):
    main()
