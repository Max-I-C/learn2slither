from generation import new_apple
from model import build_vision, neuronal_network, encode_vision

def update_len(grid, _apple, _game):
    if(_apple == 'R'):
        grid[_game.snake_len[len(_game.snake_len) - 1][0]][_game.snake_len[len(_game.snake_len) - 1][1]] = '0'
        _game.snake_len.pop()
        print("Snake -1 of len")
        if(len(_game.snake_len) == 1):
            print("GAME OVER, SNAKE TOO LITLE")
            exit()
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
    grid[_game.snake_len[len(_game.snake_len) - 1][0]][_game.snake_len[len(_game.snake_len) - 1][1]] = '0'
    for i in range(len(_game.snake_len) - 1, 0, -1):
        _game.snake_len[i] = _game.snake_len[i - 1]
        grid[_game.snake_len[i][0]][_game.snake_len[i][1]] = 'S'
    _game.snake_len[0] = (new_x, new_y)
    return(grid)

def change_direction(x, y, grid, widht, height, _game):
    if(_game.snake_xpos + x > widht - 2 or _game.snake_xpos + x < 1 or _game.snake_ypos + y > height - 2 or _game.snake_ypos + y < 1):
        print("GAME OVER, SNAKE HIT A WALL")
        exit()
    if(grid[_game.snake_xpos + x][_game.snake_ypos + y] == 'G'):
        grid = new_apple(grid, height, widht, 'G')
        grid = update_len(grid, 'G', _game)
    elif(grid[_game.snake_xpos + x][_game.snake_ypos + y] == 'R'):
        grid = new_apple(grid, height, widht, 'R')
        grid = update_len(grid, 'R', _game)
    grid[_game.snake_xpos][_game.snake_ypos] = '0'
    if(grid[_game.snake_xpos + x][_game.snake_ypos + y] == 'P' or grid[_game.snake_xpos + x][_game.snake_ypos + y] == 'S'):
        print("GAME OVER, SNAKE CROSSING ITSELF")
        exit()
    grid[_game.snake_xpos + x][_game.snake_ypos + y] = 'P'
    _game.snake_xpos = _game.snake_xpos + x
    _game.snake_ypos = _game.snake_ypos + y
    grid = snake_moov(_game.snake_xpos, _game.snake_ypos, grid, _game)
    return(grid)


    
def moov_snake(_game, grid, width, height, model):
    print(encode_vision(build_vision(_game, grid)))
    snake_vision = build_vision(_game, grid)
    decision = neuronal_network(snake_vision, model)
    if(decision == 1):
        grid = change_direction(-1, 0, grid, len(grid[0]), len(grid), _game)
    elif(decision == 2):
        grid = change_direction(+1, 0, grid, len(grid[0]), len(grid), _game)
    elif(decision == 3):
        grid = change_direction(0, -1, grid, len(grid[0]), len(grid), _game)
    elif(decision == 4):
        grid = change_direction(0, +1, grid, len(grid[0]), len(grid), _game)
    else:
        print("HAAAAAAAAAAAAAAAAAAAA, j'suis stuck la le sang")
    print(snake_vision)