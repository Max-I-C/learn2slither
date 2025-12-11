from graphic import texture 
import random
import pygame
import pdb

tile_sprite = 64
snake_xpos = 0
snake_ypos = 0
snake_len = []

def generate_elements(grid, widht, height):
    global snake_xpos
    global snake_ypos
    global snake_len
    
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
            snake_xpos = x_snake
            snake_ypos = y_snake
            snake_len.append((snake_xpos, snake_ypos))
            i = 0
            while(i < 2):
                if(grid[x_snake][y_snake + 1] == '0'):
                    snake_len.append((x_snake, y_snake + 1))
                    y_snake = y_snake + 1
                elif(grid[x_snake][y_snake - 1] == '0'):
                    snake_len.append((x_snake, y_snake - 1))
                    y_snake = y_snake - 1
                elif(grid[x_snake + 1][y_snake] == '0'):
                    snake_len.append((x_snake + 1, y_snake))
                    x_snake = x_snake + 1
                elif(grid[x_snake - 1][y_snake] == '0'):
                    snake_len.append((x_snake - 1, y_snake))
                    x_snake = x_snake - 1
                else:
                    print("Error to had snake_len")
                i = i + 1
                grid[x_snake][y_snake] = "S"
        break
    return(grid)

def generate_map(widht, height):
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
    return(generate_elements(grid, widht, height))


def new_apple(grid, height, widht, apple):
    while(True):
        x_apple = random.randint(1, height - 2)
        y_apple = random.randint(1, widht - 2)
        if(grid[x_apple][y_apple] == "0"):
            grid[x_apple][y_apple] = apple
            break
    return(grid)

def update_len(grid, _apple):
    global snake_len

    if(_apple == 'R'):
        grid[snake_len[len(snake_len) - 1][0]][snake_len[len(snake_len) - 1][1]] = '0'
        snake_len.pop()
        print("Snake -1 of len")
        if(len(snake_len) == 1):
            print("GAME OVER, SNAKE TOO LITLE")
            exit()
        return(grid)
    x_last = snake_len[len(snake_len) - 1][0] 
    y_last = snake_len[len(snake_len) - 1][1]
    if(grid[x_last][y_last + 1] == '0'):
        snake_len.append((x_last, y_last + 1))
    elif(grid[x_last][y_last - 1] == '0'):
        snake_len.append((x_last, y_last - 1))
    elif(grid[x_last + 1][y_last] == '0'):
        snake_len.append((x_last + 1, y_last))
    elif(grid[x_last - 1][y_last] == '0'):
        snake_len.append((x_last - 1, y_last))
    else:
        print("Error to had snake_len")
    print("Snake +1 of len")
    return(grid)

def snake_moov(new_x, new_y, grid):
    grid[snake_len[len(snake_len) - 1][0]][snake_len[len(snake_len) - 1][1]] = '0'
    for i in range(len(snake_len) - 1, 0, -1):
        snake_len[i] = snake_len[i - 1]
        grid[snake_len[i][0]][snake_len[i][1]] = 'S'
    snake_len[0] = (new_x, new_y)
    return(grid)

def change_direction(x, y, grid, widht, height):
    global snake_ypos
    global snake_xpos
    if(snake_xpos + x > widht - 2 or snake_xpos + x < 1 or snake_ypos + y > height - 2 or snake_ypos + y < 1):
        return(grid)
    if(grid[snake_xpos + x][snake_ypos + y] == 'G'):
        grid = new_apple(grid, height, widht, 'G')
        grid = update_len(grid, 'G')
    elif(grid[snake_xpos + x][snake_ypos + y] == 'R'):
        grid = new_apple(grid, height, widht, 'R')
        grid = update_len(grid, 'R')
    grid[snake_xpos][snake_ypos] = '0'
    if(grid[snake_xpos + x][snake_ypos + y] == 'P' or grid[snake_xpos + x][snake_ypos + y] == 'S'):
        print("GAME OVER, SNAKE CROSSING ITSELF")
        exit()
    grid[snake_xpos + x][snake_ypos + y] = 'P'
    snake_xpos = snake_xpos + x
    snake_ypos = snake_ypos + y
    grid = snake_moov(snake_xpos, snake_ypos, grid)
    return(grid)

def display_map(grid):
    width = len(grid[0]) * tile_sprite
    height = len(grid) * tile_sprite

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    dico_texture = texture.texture_init()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    grid = change_direction(-1, 0, grid, len(grid[0]), len(grid))
                elif event.key == pygame.K_s:
                    grid = change_direction(+1, 0, grid, len(grid[0]), len(grid))
                elif event.key == pygame.K_d:
                    grid = change_direction(0, +1, grid, len(grid[0]), len(grid))
                elif event.key == pygame.K_a:
                    grid = change_direction(0, -1, grid, len(grid[0]), len(grid))
                    
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char == "1":
                    screen.blit(dico_texture[2], (j * tile_sprite, i * tile_sprite))
                elif char == "P":
                    screen.blit(dico_texture[0], (j * tile_sprite, i * tile_sprite))
                elif char == "S":
                    screen.blit(dico_texture[1], (j * tile_sprite, i * tile_sprite))
                elif char == "0":
                    screen.blit(dico_texture[3], (j * tile_sprite, i * tile_sprite))
                elif char == "R":
                    screen.blit(dico_texture[4], (j * tile_sprite, i * tile_sprite))
                elif char == "G":
                    screen.blit(dico_texture[5], (j * tile_sprite, i * tile_sprite))
        pygame.display.flip()
    pygame.quit()

def main():
    print("Main")
    grid = generate_map(10, 10)
    display_map(grid)
    

if(__name__ == "__main__"):
    main()