from tensorflow.keras.models import load_model
from model import create_model
import argparse
import json


# -- 1. This function manage the flags placed in the execution -- #
def args_manager():
    parser = argparse.ArgumentParser(description="Learn2Slither")
    parser.add_argument(
        "-g", "--graphical",
        action="store_true",
        help="Enable graphical mode (pygame)"
    )
    parser.add_argument(
        "-r", "--real",
        action="store_true",
        help="Enable training mode"
    )
    parser.add_argument(
        "-n", "--number-of-games",
        type=int,
        default=10000,
        help="Number of game to run"
    )
    parser.add_argument(
        "-s", "--step",
        action="store_true",
        help="Enable the step by step"
    )
    parser.add_argument(
        "-q", "--quick",
        type=float,
        default=0.0,
        help="Define the speed of the graphical environement"
    )
    parser.add_argument(
        "-t", "--training",
        type=int,
        default=0,
        help="Define wich model will be load"
    )
    parser.add_argument(
        "-c", "--clear",
        action="store_true",
        help="Use that flag if you don't want output data"
    )
    args = parser.parse_args()
    return (args)


# -- 2. This function open a data files that contain the number of #
# episode that the model got trained and the epsilon value -- #
def collecting_data(_game, _model, args):
    try:
        with open(".prog_data.json") as f:
            data = json.load(f)
            _game.epsilon = data["epsilone"]
            _model.episode = data["episode"]
        print("Data found from the .json files")
    except Exception:
        _game.epsilon = 1
        _model.episode = 0
        print("No epsilon data found")
    if (args.training):
        _model.episode = args.training
    try:
        _model.model = load_model(
            f"models/snake_model_v2_{_model.episode}.keras"
        )
        print("Model loaded, continuing training....")
    except Exception:
        _model.model = create_model(input_size=40, output_size=4)
        print("New model created")


# -- 3. This function define the value associated to the flags -- #
def store_args_data(args, _game):
    if (args.real):
        _game.epsilon = 0
    if (args.number_of_games is not None):
        _game.max_game = args.number_of_games
    if (args.graphical):
        _game.graph = True
    if (args.step):
        _game.step = True
    if (args.quick):
        _game.quick = args.quick
    if (args.clear):
        _game.clear = True


# -- 14. This function is updating the for the game info -- #
def save_and_display(_model, _data, _game):
    _model.episode += 1
    _data.all_game += 1
    if (_game.max_length < len(_game.snake_len)):
        _game.max_length = len(_game.snake_len)
    print("nb of episode ", _model.episode)
    print("Best score : ", _game.max_length)
    print(_data)
    if (_game.epsilon):
        _game.epsilon = max(0.02, _game.epsilon * 0.995)
