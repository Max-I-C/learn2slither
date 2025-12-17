import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

ENCODING = {
    "0" : 0.0,
    "1" : -1.0,
    "S" : -0.5,
    "P" : 0.0,
    "R" : 1.0,
    "G" : -1.0
}

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
    return(snake_vision)

def create_model(input_size, output_size):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_size,)),
        Dense(64, activation='relu'),
        Dense(output_size, activation='linear')
    ])
    model.compile(
        optimizer='adam',
        loss='mse'
    )
    return model

def neuronal_network(snake_vision, model, epsilon=0.1):
    state = encode_vision(snake_vision)
    state = state.reshape(1, -1)

    # Exploration (important en RL)
    if np.random.rand() < epsilon:
        return np.random.randint(1, 5)

    # Exploitation
    q_values = model.predict(state, verbose=0)
    action = np.argmax(q_values[0]) + 1

    return action