from graphic import texture 
import random
import pygame
import time
import pdb

class MyGame():
    def __init__(self):
        self.tile_sprite = 64
        self.snake_xpos = 0
        self.snake_ypos = 0
        self.snake_len = []

def generate_elements(grid, widht, height, _game):
    
    #breakpoint() #Debug
    while(True):
        x_red = random.randint(1, height - 2)
        y_red = random.randint(1, widht - 2)
        if(grid[x_red][y_red] == "0"):
            grid[x_red][y_red] = "R"
            break
    while(True):
        x_green = random.randint(1, height - 2)
        y_green = random.randint(1, widht - 2)
        if(grid[x_green][y_green] == "0"):
            grid[x_green][y_green] = "G"
            break
    while(True):
        x_snake = random.randint(1, height - 2)
        y_snake = random.randint(1, widht - 2)
        if(grid[x_snake][y_snake] == "0"):
            grid[x_snake][y_snake] = "P"
            _game.snake_xpos = x_snake
            _game.snake_ypos = y_snake
            _game.snake_len.append((_game.snake_xpos, _game.snake_ypos))
            i = 0
            while(i < 2):
                if(grid[x_snake][y_snake + 1] == '0'):
                    _game.snake_len.append((x_snake, y_snake + 1))
                    y_snake = y_snake + 1
                elif(grid[x_snake][y_snake - 1] == '0'):
                    _game.snake_len.append((x_snake, y_snake - 1))
                    y_snake = y_snake - 1
                elif(grid[x_snake + 1][y_snake] == '0'):
                    _game.snake_len.append((x_snake + 1, y_snake))
                    x_snake = x_snake + 1
                elif(grid[x_snake - 1][y_snake] == '0'):
                    _game.snake_len.append((x_snake - 1, y_snake))
                    x_snake = x_snake - 1
                else:
                    print("Error to had snake_len")
                i = i + 1
                grid[x_snake][y_snake] = "S"
        break
    return(grid)

def generate_map(widht, height, _game):
    #breakpoint() #Debug
    grid = []
    for i in range(height):
        row = []
        for j in range(widht):
            if(i == 0 or i == height - 1 or j == 0 or j == widht - 1):
                row.append("1")
            else:
                row.append("0")
        grid.append(row)
    return(generate_elements(grid, widht, height, _game))


def new_apple(grid, height, widht, apple):
    while(True):
        x_apple = random.randint(1, height - 2)
        y_apple = random.randint(1, widht - 2)
        if(grid[x_apple][y_apple] == "0"):
            grid[x_apple][y_apple] = apple
            break
    return(grid)

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
    
def moov_snake(_game, grid, width, height):
    snake_vision = build_vision(_game, grid)
    if(snake_vision["UP"][0] == '0' or snake_vision["UP"][0] == 'G'):
        grid = change_direction(-1, 0, grid, len(grid[0]), len(grid), _game)
    elif(snake_vision["DOWN"][0] == '0' or snake_vision["DOWN"][0] == 'G'):
        grid = change_direction(+1, 0, grid, len(grid[0]), len(grid), _game)
    elif(snake_vision["LEFT"][0] == '0' or snake_vision["LEFT"][0] == 'G'):
        grid = change_direction(0, -1, grid, len(grid[0]), len(grid), _game)
    elif(snake_vision["RIGHT"][0] == '0' or snake_vision["RIGHT"][0] == 'G'):
        grid = change_direction(0, +1, grid, len(grid[0]), len(grid), _game)
    else:
        print("HAAAAAAAAAAAAAAAAAAAA, j'suis stuck la le sang")
    print(snake_vision)

def display_map(grid, _game):
    width = len(grid[0]) * _game.tile_sprite
    height = len(grid) * _game.tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture.texture_init(_game)
    run = True
    while run:
        moov_snake(_game, grid, width, height)
        time.sleep(0.1)
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                run = False
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_w:
#                    grid = change_direction(-1, 0, grid, len(grid[0]), len(grid), _game)
#                elif event.key == pygame.K_s:
#                    grid = change_direction(+1, 0, grid, len(grid[0]), len(grid), _game)
#                elif event.key == pygame.K_d:
#                    grid = change_direction(0, +1, grid, len(grid[0]), len(grid), _game)
#                elif event.key == pygame.K_a:
#                    grid = change_direction(0, -1, grid, len(grid[0]), len(grid), _game)
#                    
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char == "1":
                    screen.blit(dico_texture[2], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "P":
                    screen.blit(dico_texture[0], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "S":
                    screen.blit(dico_texture[1], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "0":
                    screen.blit(dico_texture[3], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "R":
                    screen.blit(dico_texture[4], (j * _game.tile_sprite, i * _game.tile_sprite))
                elif char == "G":
                    screen.blit(dico_texture[5], (j * _game.tile_sprite, i * _game.tile_sprite))
        pygame.display.flip()
    pygame.quit()

def main():
    print("Main")
    _game = MyGame()
    grid = generate_map(10, 10, _game)
    display_map(grid, _game)
    

if(__name__ == "__main__"):
    main()
