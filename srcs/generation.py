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
            _game.green_x = x_green
            _game.green_y = y_green 
            break
    while(True):
        x_snake = random.randint(1, height - 2)
        y_snake = random.randint(1, widht - 2)
        if(grid[x_snake][y_snake] == "0"):
            grid[x_snake][y_snake] = "P"
            _game.snake_xpos = x_snake
            _game.snake_ypos = y_snake
            _game.snake_len.append((_game.snake_xpos, _game.snake_ypos))

            while(len(_game.snake_len) < 3):
                if(y_snake + 1 < widht - 1 and grid[x_snake][y_snake + 1] == '0'):
                    _game.snake_len.append((x_snake, y_snake + 1))
                    y_snake = y_snake + 1
                elif(y_snake - 1 > 0 and grid[x_snake][y_snake - 1] == '0'):
                    _game.snake_len.append((x_snake, y_snake - 1))
                    y_snake = y_snake - 1
                elif(x_snake + 1 < height - 1 and grid[x_snake + 1][y_snake] == '0'):
                    _game.snake_len.append((x_snake + 1, y_snake))
                    x_snake = x_snake + 1
                elif(x_snake - 1 > 0 and grid[x_snake - 1][y_snake] == '0'):
                    _game.snake_len.append((x_snake - 1, y_snake))
                    x_snake = x_snake - 1
                else:
                    break
                grid[x_snake][y_snake] = "S"
            # Set initial direction based on the second segment so we forbid only the immediate reverse move
            if len(_game.snake_len) >= 2:
                hx, hy = _game.snake_len[0]
                bx, by = _game.snake_len[1]
                if bx == hx and by == hy + 1:      # body is to the right -> heading left
                    _game.direction = 3
                elif bx == hx and by == hy - 1:    # body is to the left -> heading right
                    _game.direction = 4
                elif bx == hx + 1 and by == hy:    # body is below -> heading up
                    _game.direction = 1
                elif bx == hx - 1 and by == hy:    # body is above -> heading down
                    _game.direction = 2
            else:
                _game.direction = 1
            print("Snake len at end of spawn:", len(_game.snake_len))
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

def new_apple(grid, height, widht, apple, _game):
    while(True):
        x_apple = random.randint(1, height - 2)
        y_apple = random.randint(1, widht - 2)
        if(grid[x_apple][y_apple] == "0"):
            grid[x_apple][y_apple] = apple
            if(apple == 'G'):
                _game.green_x = x_apple
                _game.green_y = y_apple
            break
    return(grid)