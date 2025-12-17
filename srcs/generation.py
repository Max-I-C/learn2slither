import random

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
    _game.snake_len = []
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