from generation import new_apple
from model import build_vision, neuronal_network, encode_vision, train_step, dist_to_apple

def update_len(grid, _apple, _game):
    if(_apple == 'R'):
        grid[_game.snake_len[len(_game.snake_len) - 1][0]][_game.snake_len[len(_game.snake_len) - 1][1]] = '0'
        _game.snake_len.pop()
        print("Snake -1 of len")
        return(grid)
    x_last = _game.snake_len[len(_game.snake_len) - 1][0] 
    y_last = _game.snake_len[len(_game.snake_len) - 1][1]
    if(grid[x_last][y_last + 1] == '0'):
        _game.snake_len.append((x_last, y_last + 1))
    elif(grid[x_last][y_last - 1] == '0'):
        _game.snake_len.append((x_last, y_last - 1))
    elif(grid[x_last + 1][y_last] == '0'):
        _game.snake_len.append((x_last + 1, y_last))
    elif(grid[x_last - 1][y_last] == '0'):
        _game.snake_len.append((x_last - 1, y_last))
    else:
        print("Error to had snake_len")
    print("Snake +1 of len")
    return(grid)

def snake_moov(new_x, new_y, grid, _game):
    if not _game.snake_len:
        print("CA A PAS CRASHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        return grid 
    tail_x, tail_y = _game.snake_len[-1]
    grid[tail_x][tail_y] = '0'
    for i in range(len(_game.snake_len) - 1, 0, -1):
        _game.snake_len[i] = _game.snake_len[i - 1]
        grid[_game.snake_len[i][0]][_game.snake_len[i][1]] = 'S'
    _game.snake_len[0] = (new_x, new_y)
    return(grid)

def change_direction(x, y, grid, widht, height, _game):
    nx = _game.snake_xpos + x
    ny = _game.snake_ypos + y 
    
    if(nx > widht - 2 or nx < 1 or ny > height - 2 or ny < 1):
        print("GAME OVER, SNAKE HIT A WALL")
        return grid, "WALL"
    cell = grid[nx][ny]
    if(cell == 'P' or cell == 'S'):
        print("GAME OVER, SNAKE CROSSING ITSELF")
        return grid, "SELF"
    if(cell == 'G'):
        event = "GREEN_APPLE"
        grid = new_apple(grid, height, widht, 'G', _game)
        grid = update_len(grid, 'G', _game)
    elif(cell == 'R'):
        if(len(_game.snake_len) == 1):
            print("GAME OVER, SNAKE TOO LITLE")
            return grid, "SNAKE_LEN"
        event = "RED_APPLE"
        grid = new_apple(grid, height, widht, 'R', _game)
        grid = update_len(grid, 'R', _game)
    else:
        event = "MOOVE"
    grid[_game.snake_xpos][_game.snake_ypos] = '0'
    grid[nx][ny] = 'P'
    _game.snake_xpos = nx
    _game.snake_ypos = ny
    grid = snake_moov(nx, ny, grid, _game)
    return(grid, event)

def moov_snake(_game, grid, model):
    #print(encode_vision(build_vision(_game, grid)))
    old_dist = dist_to_apple(_game)
    state = encode_vision(build_vision(_game, grid))
    decision = neuronal_network(state, model, _game)
    if(decision == 1):
        grid, event = change_direction(-1, 0, grid, len(grid[0]), len(grid), _game)
    elif(decision == 2):
        grid, event = change_direction(+1, 0, grid, len(grid[0]), len(grid), _game)
    elif(decision == 3):
        grid, event = change_direction(0, -1, grid, len(grid[0]), len(grid), _game)
    elif(decision == 4):
        grid, event = change_direction(0, +1, grid, len(grid[0]), len(grid), _game)
    else:
        print("HAAAAAAAAAAAAAAAAAAAA, j'suis stuck la le sang")

    reward = 0.0
    done = False
    if (event in ["WALL", "SELF", "SNAKE_LEN"]):
        done = True
        reward = -100
    elif (event == "GREEN_APPLE"):
        reward = +50
    elif (event == "RED_APPLE"):
        reward = -30
    else:
        new_dist = dist_to_apple(_game)
        if(new_dist < old_dist):
            reward += 10.0
        elif(new_dist > old_dist):
            reward -= 10.0
        else:
            reward -= 0.05
    if(done):
        next_state = state
    else:
        next_state = encode_vision(build_vision(_game, grid))
    train_step(model, state, decision, reward, next_state, done)
    if(done):
        return(False)
    return(grid)
    #for lines in grid:
    #    print("->", lines)
    #print(grid)
    #print(snake_vision)