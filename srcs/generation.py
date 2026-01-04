import random

# -- 4. This function create the map of 10x10 and add the elements of the map -- #
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

# -- 5. This function generate the red/green apples and the player -- #
def generate_elements(grid, widht, height, _game):
    
    #breakpoint() #Debug
    while(True):
        x_red = random.randint(1, height - 2)
        y_red = random.randint(1, widht - 2)
        if(grid[x_red][y_red] == "0"):
            grid[x_red][y_red] = "R"
            break
    _game.green_apples = []
    while(len(_game.green_apples) < 2):
        x_green = random.randint(1, height - 2)
        y_green = random.randint(1, widht - 2)
        if(grid[x_green][y_green] == "0"):
            grid[x_green][y_green] = "G"
            _game.green_apples.append((x_green, y_green)) 
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

# -- 12.1. This function is called to generate a new apple when the previous one got eated -- #
def new_apple(grid, height, widht, apple, x, y, _game):
    while(True):
        x_apple = random.randint(1, height - 2)
        y_apple = random.randint(1, widht - 2)
        if(grid[x_apple][y_apple] == "0"):
            grid[x_apple][y_apple] = apple
            if(apple == 'G'):
                if(x == _game.green_apples[0][0] and y == _game.green_apples[0][1]):
                    print("apple_1_new_generate")
                    _game.green_apples[0] = (x_apple, y_apple)
                else:
                    print("apple_2_new_generate")
                    _game.green_apples[1] = (x_apple, y_apple)

            break
    return(grid)