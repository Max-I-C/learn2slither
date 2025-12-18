import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

ENCODING = {
    "0" : 0.0,
    "1" : -1.0,
    "S" : -0.5,
    "P" : -0.5,
    "R" : -1.0,
    "G" : 1.0
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
        Dense(128, activation='relu', input_shape=(input_size,)),
        Dense(128, activation='relu'),
        Dense(output_size, activation='linear')
    ])
    model.compile(
        optimizer='adam',
        loss='mse'
    )
    return model

def neuronal_network(state, model, _game):
    state = state.reshape(1, -1)

    # Exploration (important en RL)
    if np.random.rand() < _game.epsilon:
        return np.random.randint(1, 5)

    # Exploitation
    q_values = model.predict(state, verbose=0)
    action = np.argmax(q_values[0]) + 1

    return action

def train_step(model, state, action, reward, next_state, done, gamma=0.95):
    state = state.reshape(1, -1)
    next_state = next_state.reshape(1, -1)

    q_values = model.predict(state, verbose=0)

    if done:
        q_values[0][action - 1] = reward
    else:
        next_q = model.predict(next_state, verbose=0)
        q_values[0][action - 1] = reward + gamma * np.max(next_q)

    model.fit(state, q_values, verbose=0)

def dist_to_apple(_game):
    sx, sy = _game.snake_xpos, _game.snake_ypos
    ax, ay = _game.green_x, _game.green_y
    return(abs(sx-ax) + abs(sy-ay))