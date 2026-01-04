from data import collecting_data, args_manager, save_and_display, store_args_data
from model import save_model
from generation import generate_map
from display import display_map

# -- Definition of classes -- # 
class Model():
    def __init___(self):
        self.model = ""
        self.episode = 0

class Dataset():
    def __init__(self):
        self.all_game = 0
        self.max_game = 0
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
        self.max_length = 0
        self.max_duration = 0
        self.graph = False
# -- Definition of classes -- # 

# -- 0 -- #
def main():
    args = args_manager()
    _game = MyGame()
    _data = Dataset()
    _model = Model()
    collecting_data(_game, _model)
    store_args_data(args, _game, _data)
    print(" -> ", _model.episode, " -> ", _game.max_game)
    while True and _data.all_game < _game.max_game:
        grid = generate_map(10, 10, _game)
        if (display_map(grid, _game, _model.model, _data.graph, _data) == True):
            break
        if(_model.episode % 100 == 0 and _model.episode != 0):
            save_model(_model, _game)
        save_and_display(_model, _data, _game)
    print("End of the training model.")

if(__name__ == "__main__"):
    main()
