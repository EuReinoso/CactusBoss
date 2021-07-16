import pygame,sys
from pygame.locals import *
from assets.pgengine import *

pygame.init()

class Player(Platformer):
    def __init__(self, x, y, width, height, img, xvel, jump_force):
        super().__init__(x, y, width, height,img,  xvel= xvel, jump_force= jump_force)

class Cactus(Obj):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)

WINDOW_SIZE = (900, 600)
DISPLAY_SIZE = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[1]/3))
TILE_SIZE = 16

pygame.display.set_caption('CactusBoss')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)

map1 = load_map('assets/map.txt')

#Images
path = 'assets/images/'

bg_img = load_img(path + 'background')
tile1_img = load_img(path + 'tile1')
tile2_img = load_img(path + 'tile2')
player_idle_imgs = load_imgs_from_past(path + 'player_idle/')
player_run_imgs = load_imgs_from_past(path + 'player_run/')
cactus_idle_imgs = load_imgs_from_past(path + 'cactus_idle/')
cactus_atack_imgs = load_imgs_from_past(path + 'cactus_atack/')

#load_map
tiles = []
y = 0
for row in map1:
    x = 0
    for val in row:
        if val == '1':
            tiles.append(Obj(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, tile1_img))
        if val == '2':
            tiles.append(Obj(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, tile2_img))

        x += 1
    y += 1

#Objs
bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0] * 2, DISPLAY_SIZE[1] * 2, img= bg_img)

player = Player(100, 100, 11, 15, player_idle_imgs[0], xvel= 3, jump_force= 3)
player.mass = 0.7
player.action = 'idle'
player.add_imgs_data(player_idle_imgs, 'idle', [15, 15])
player.add_imgs_data(player_run_imgs, 'run', [10, 10])

cactus_tile = tiles[96]
cactus = Cactus(cactus_tile.x, cactus_tile.y - cactus_tile.height/2 - 40, 80, 80, img= cactus_idle_imgs[0])
cactus.action = 'idle'
cactus.add_imgs_data(cactus_idle_imgs, 'idle', [10, 10, 10, 10])
cactus.add_imgs_data(cactus_atack_imgs, 'atack', [10, 10, 10, 10])
               
#scroll
scroll_x, scroll_y = 0, 0

loop = True
while loop:

    scroll_x += int((player.x - scroll_x - DISPLAY_SIZE[0]/2)/10)
    scroll_y += int((player.y - scroll_y - DISPLAY_SIZE[1]/2)/30)
    
    if scroll_x >= DISPLAY_SIZE[0]/2.8:
        scroll_x = DISPLAY_SIZE[0]/2.8
    
    if scroll_x <= -8:
        scroll_x = -8

    if scroll_y >= DISPLAY_SIZE[1]/5:
        scroll_y = int(DISPLAY_SIZE[1]/5)
    
    if scroll_y <= 30:
        scroll_y = 30


    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        player.control(event)

    #BG
    bg.draw(display, -scroll_x * 0.5, -scroll_y * 0.5)

    #Blit map
    for tile in tiles:
        tile.draw(display, -scroll_x, -scroll_y)

    #cactus
    cactus.draw(display, -scroll_x, -scroll_y)
    cactus.anim()

    #player
    player.draw(display, -scroll_x, -scroll_y)
    player.collision_move(tiles)
    player.update()
    player.anim()

    if player.x_momentum != 0:
        player.action = 'run'
    else:
        player.action = 'idle'


    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(fps)