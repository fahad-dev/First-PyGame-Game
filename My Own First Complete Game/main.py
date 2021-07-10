import pygame, sys, time, random
import data.engine as e
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Isometric Game')
screen = pygame.display.set_mode((900,900), 0, 32)
display = pygame.Surface((300,300))

grey_block_image = pygame.image.load('grey_block.png').convert()
grey_block_image = pygame.transform.scale(grey_block_image, (20,20))
grey_block_image.set_colorkey((0,0,0))
background = pygame.image.load('space_bg.png').convert()

CHUNK_SIZE = 8

f = open('map.txt')
map_data = [[int(c) for c in row] for row in f.read().split('\n')] # check how this syntax works
f.close()

e.load_animations('data/images/entities/')
player = e.entity(23,23,23,23, 'player')

moving_right = False
moving_left = False

player_gravity = 0
air_time = 0
idle_timer = 0

while True:
    display.fill((0,0,0))
    display.blit(background, [0,0])

    tile_rects = []
    player_movement = [0,0]

    y = 0
    for row in map_data:
        x = 0
        for tile in row:
            if tile == 1:
                display.blit(grey_block_image, (x*20,y*20))
            if tile != 0:
                tile_rects.append(pygame.Rect(x*20,y*20, 20, 20))
            x += 1
        y += 1

    player.set_action('idle')

    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += player_gravity
    player_gravity += 0.2
    if player_gravity > 3:
        player_gravity = 3



    collision_types = player.move(player_movement, tile_rects)
    if collision_types['bottom']:
        player_gravity = 0
        air_time = 0
    else:
        air_time += 1


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
            if event.key == K_SPACE:
                if air_time < 12:
                    player_gravity = -8

        if event.type == KEYUP:
            if event.key == K_a:
                moving_left = False
            if event.key == K_d:
                moving_right = False

        if idle_timer != 0:
            idle_timer -= 1
        else:
            idle_timer = 5

    player.change_frame(1)  # makes the animation work by actually changing the frames of the images
    player.display(display, (0,5 + idle_timer))
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0,0))
    pygame.display.update()
    clock.tick(60)
