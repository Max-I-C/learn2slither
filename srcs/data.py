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
    args = parser.parse_args()
    return (args)


# -- 2. This function open a data files that contain the number of #
# episode that the model got trained and the epsilon value -- #
def collecting_data(_game, _model):
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
    try:
        _model.model = load_model(
            f"models/snake_model_v2_{_model.episode}.keras"
        )
        print("Model loaded, continuing training....")
    except Exception:
        _model.model = create_model(input_size=40, output_size=4)
        print("New model created")


# -- 3. This function define the value associated to the flags -- #
def store_args_data(args, _game, _data):
    if (args.real):
        _game.epsilon = 0
    if (args.number_of_games is not None):
        _game.max_game = args.number_of_games
    _data.graph = False
    if (args.graphical):
        _data.graph = True


# -- 14. This function is updating the for the game info -- #
def save_and_display(_model, _data, _game):
    _model.episode += 1
    _data.all_game += 1
    if (_game.max_length < len(_game.snake_len)):
        _game.max_length = len(_game.snake_len)
    print("nb of episode ", _model.episode)
    print("Best score : ", _game.max_length)
    print(_data)
    _game.epsilon = max(0.02, _game.epsilon * 0.995)
