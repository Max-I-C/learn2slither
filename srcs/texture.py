import pygame 

def texture_init(_game):
    dico_texture = []
    # -- Snake head -- #
    snake_sprite = pygame.image.load("../texture/snake.png").convert()
    snake_sprite = pygame.transform.scale((snake_sprite), (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(snake_sprite)
    # -- Snake body -- #
    snake_body_sprite = pygame.image.load("../texture/body.png").convert()
    snake_body_sprite = pygame.transform.scale((snake_body_sprite), (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(snake_body_sprite)
    # -- Wall -- # 
    wall_sprite = pygame.image.load("../texture/wall2.jpg").convert()
    wall_sprite = pygame.transform.scale(wall_sprite, (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(wall_sprite)
    # -- Floor -- #
    floor_sprite = pygame.image.load("../texture/floor.jpg").convert()
    floor_sprite = pygame.transform.scale(floor_sprite, (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(floor_sprite)
    # -- R_apple -- #
    r_apple_sprite = pygame.image.load("../texture/r_apple.jpeg").convert()
    r_apple_sprite = pygame.transform.scale(r_apple_sprite, (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(r_apple_sprite)
    # -- G_apple -- #
    g_apple_sprite = pygame.image.load("../texture/green_.png").convert()
    g_apple_sprite = pygame.transform.scale(g_apple_sprite, (_game.tile_sprite, _game.tile_sprite))
    dico_texture.append(g_apple_sprite)
    return (dico_texture)