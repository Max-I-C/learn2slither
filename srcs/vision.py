import numpy as np

# -- Information that provides the model a number associate at each part of the map -- #
ENCODING = {
    "0" : 0.0,
    "1" : -1.0,
    "S" : -0.5,
    "P" : -0.5,
    "R" : -1.0,
    "G" : 1.0
}

# -- Build the snake vision to be able to use it in the model -- # 
def build_vision(_game, grid):
    snake_vision = {
        "UP": [],
        "CENTER" : ["P"],
        "DOWN": [],
        "LEFT": [],
        "RIGHT": [] 
    }
    max_x = len(grid)
    max_y = len(grid[0])
    x = _game.snake_xpos + 1
    y = _game.snake_ypos + 1
    while(x < max_x):
        snake_vision["DOWN"].append(grid[x][_game.snake_ypos])
        x += 1
    while(y < max_y):
        snake_vision["RIGHT"].append(grid[_game.snake_xpos][y])
        y = y + 1
    x = _game.snake_xpos - 1 
    y = _game.snake_ypos - 1
    while(x >= 0):
        snake_vision["UP"].append(grid[x][_game.snake_ypos])
        x -= 1
    while(y >= 0):
        snake_vision["LEFT"].append(grid[_game.snake_xpos][y])
        y -= 1
    display_vision(grid, _game, snake_vision)
    return(snake_vision)

# -- 10. Transform the vision of the snake with the [INT] associate at each case of the map from the vision -- #
def encode_vision(snake_vison, max_dist=10):
    state = []
    for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
        cells = snake_vison[direction][:max_dist]
        for cell in cells:
            state.append(ENCODING.get(cell, 0.0))
        while len(cells) < max_dist:
            state.append(-1.0)
            cells.append("1")
    return np.array(state, dtype=np.float32)

# -- Display the vision in the terminal to make sure that the snake is seing the information he should -- #
def display_vision(grid, _game, snake_vision):
    height = len(grid)
    width = len(grid[0])
    x = _game.snake_xpos
    y = _game.snake_ypos
    vision_map = [[" " for _ in range(width)] for _ in range(height)]
    vision_map[x][y] = 'P'
     
    for i, cell in enumerate(snake_vision["LEFT"], start=1):
        n_y = y - i
        if (n_y >= 0):
            vision_map[x][n_y] = cell
    for i, cell in enumerate(snake_vision["RIGHT"], start=1):
        n_y = y + i
        if (n_y < width):
            vision_map[x][n_y] = cell
    for i, cell in enumerate(snake_vision["UP"], start=1):
        n_x = x - i
        if (n_x >= 0):
            vision_map[n_x][y] = cell
    for i, cell in enumerate(snake_vision["DOWN"], start=1):
        n_x = x + i
        if (n_x < height):
            vision_map[n_x][y] = cell
    
    print('\n')
    for line in vision_map:
        print("".join(line))