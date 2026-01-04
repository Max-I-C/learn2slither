import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import json


OPPOSITE = {
    1:2, # UP and DOWN
    2:1,
    3:4, # LEFT AND RIGHT
    4:3
}

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

# -- 11.
def neuronal_network(state, model, _game):
    state = state.reshape(1, -1)
    valid_actions = get_valid_action(_game.direction)

    # Exploration (important en RL)
    if np.random.rand() < _game.epsilon:
        return np.random.choice(valid_actions)

    # Exploitation
    q_values = model.predict(state, verbose=0)[0]
    valid_q_values = [q_values[a - 1] for a in valid_actions]
    best_action = valid_actions[np.argmax(valid_q_values)]
    return best_action

def train_step(model, state, action, reward, next_state, done, _game, gamma=0.95):
    state = state.reshape(1, -1)
    next_state = next_state.reshape(1, -1)

    q_values = model.predict(state, verbose=0)

    if done:
        q_values[0][action - 1] = reward
    else:
        next_q = model.predict(next_state, verbose=0)[0]
        valid_actions = get_valid_action(_game.direction)
        max_next_q = max(next_q[a - 1] for a in valid_actions)
        q_values[0][action - 1] = reward + gamma * max_next_q
    model.fit(state, q_values, verbose=0)

# -- 9.
def dist_to_apple(_game):
    sx, sy = _game.snake_xpos, _game.snake_ypos
    return min(
        abs(sx-x) + abs(sy-y)
        for (x, y) in _game.green_apples
    )

def get_valid_action(current_direction):
    return [a for a in [1,2,3,4] if a != OPPOSITE[current_direction]]

# -- 13.
def save_model(_model, _game):
    try:
        _model.model.save(f"models/snake_model_v2_{_model.episode}.keras")
        print("Saving the model at ", _model.episode)
        data = {"epsilone": _game.epsilon, "episode": _model.episode}
        with open(".prog_data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("ERROR WHILE SAVING")