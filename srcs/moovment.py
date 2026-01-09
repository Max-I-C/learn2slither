from generation import new_apple
from model import neuronal_network, train_step, dist_to_apple
from vision import build_vision, encode_vision


# -- 8. Here the moovment that the model decide to choice is #
# redirected to the function that will moove the snake -- #
def moov_snake(_game, grid, model, _data):
    # print(encode_vision(build_vision(_game, grid)))
    _data.moov_count += 1
    old_dist = dist_to_apple(_game)
    state = encode_vision(build_vision(_game, grid))
    decision = neuronal_network(state, model, _game)
    if (decision == 1):
        _game.direction = 1
        print("UP")
        grid, event = change_direction(
            -1, 0, grid, len(grid[0]), len(grid), _game
        )
    elif (decision == 2):
        _game.direction = 2
        print("DOWN")
        grid, event = change_direction(
            +1, 0, grid, len(grid[0]), len(grid), _game
        )
    elif (decision == 3):
        _game.direction = 3
        print("LEFT")
        grid, event = change_direction(
            0, -1, grid, len(grid[0]), len(grid), _game
        )
    elif (decision == 4):
        _game.direction = 4
        print("RIGHT")
        grid, event = change_direction(
            0, +1, grid, len(grid[0]), len(grid), _game
        )
    else:
        print("The snake is stuck")

    reward = 0.0
    done = False
    if (event in ["WALL", "SELF", "SNAKE_LEN"]):
        done = True
        adding_to_dataset(event, _data)
        reward = -100
    elif (event == "GREEN_APPLE"):
        reward = +50
        _data.green_apple_eated += 1
    elif (event == "RED_APPLE"):
        reward = -60
        _data.red_apple_eated += 1
    else:
        new_dist = dist_to_apple(_game)
        delta = old_dist - new_dist
        if abs(delta) < 0.05:
            reward -= 0.3
        reward -= 0.02
    if (done):
        next_state = state
    else:
        next_state = encode_vision(build_vision(_game, grid))
    if (_game.epsilon):
        train_step(model, state, decision, reward, next_state, done, _game)
    if (done):
        return (False)
    return (grid)


# -- 12. This function treat the action and execute it with the game rules -- #
def change_direction(x, y, grid, widht, height, _game):
    nx = _game.snake_xpos + x
    ny = _game.snake_ypos + y

    if (nx > widht - 2 or nx < 1 or ny > height - 2 or ny < 1):
        print("GAME OVER, SNAKE HIT A WALL")
        return grid, "WALL"
    cell = grid[nx][ny]
    if (cell == 'P' or cell == 'S'):
        print("GAME OVER, SNAKE CROSSING ITSELF")
        return grid, "SELF"
    if (cell == 'G'):
        event = "GREEN_APPLE"
        grid = new_apple(grid, height, widht, 'G', nx, ny, _game)
        grid = update_len(grid, 'G', _game)
    elif (cell == 'R'):
        if (len(_game.snake_len) == 1):
            print("GAME OVER, SNAKE TOO LITLE")
            return grid, "SNAKE_LEN"
        event = "RED_APPLE"
        grid = new_apple(grid, height, widht, 'R', nx, ny, _game)
        grid = update_len(grid, 'R', _game)
    else:
        event = "MOOVE"
    grid[_game.snake_xpos][_game.snake_ypos] = '0'
    grid[nx][ny] = 'P'
    _game.snake_xpos = nx
    _game.snake_ypos = ny
    grid = snake_moov(nx, ny, grid, _game)
    return (grid, event)


# -- 12.2. Uptade the len of the snake, so it #
# can be removing a part of the snake body or adding one -- #
def update_len(grid, _apple, _game):
    if (_apple == 'R'):
        x, y = _game.snake_len[-1]
        grid[x][y] = '0'
        _game.snake_len.pop()
        print("Snake -1 of len")
        return (grid)
    x_last = _game.snake_len[len(_game.snake_len) - 1][0]
    y_last = _game.snake_len[len(_game.snake_len) - 1][1]
    if (grid[x_last][y_last + 1] == '0'):
        _game.snake_len.append((x_last, y_last + 1))
    elif (grid[x_last][y_last - 1] == '0'):
        _game.snake_len.append((x_last, y_last - 1))
    elif (grid[x_last + 1][y_last] == '0'):
        _game.snake_len.append((x_last + 1, y_last))
    elif (grid[x_last - 1][y_last] == '0'):
        _game.snake_len.append((x_last - 1, y_last))
    else:
        print("Error to had snake_len")
    print("Snake +1 of len")
    return (grid)


# -- 13. This moove each part of the body of the snake -- #
def snake_moov(new_x, new_y, grid, _game):
    if not _game.snake_len:
        print("No crash but take care is not normal")
        return grid
    tail_x, tail_y = _game.snake_len[-1]
    grid[tail_x][tail_y] = '0'
    for i in range(len(_game.snake_len) - 1, 0, -1):
        _game.snake_len[i] = _game.snake_len[i - 1]
        grid[_game.snake_len[i][0]][_game.snake_len[i][1]] = 'S'
    _game.snake_len[0] = (new_x, new_y)
    return (grid)


# -- Add the resaon of death in the dataset -- #
def adding_to_dataset(event, _data):
    if (event == "WALL"):
        _data.death_by_wall += 1
    elif (event == "SELF"):
        _data.death_by_snake += 1
    else:
        _data.death_by_lenght += 1
    return
