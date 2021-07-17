import pygame,sys
from pygame.locals import *
from assets.pgengine import *
from random import randint
from math import hypot, atan2, degrees, cos, sin

pygame.init()

class Player(Platformer):
    def __init__(self, x, y, width, height, img, xvel, jump_force):
        super().__init__(x, y, width, height,img,  xvel= xvel, jump_force= jump_force)
        self.life = 50

class Cactus(Obj):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.atack = False
        self.atacks = {'1' : {'time' : 450}}
        self.actual_atack = '1'

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
thorn_img = load_img(path + 'thorn')
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
cactus_idle_time_range = [0, 0]
cactus_idle_time = randint(cactus_idle_time_range[0], cactus_idle_time_range[1])
cactus_idle_ticks = 0


shots = []
shots_vel = 2
shot_ticks = 0

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

        #look ar Player
    if player.x < DISPLAY_SIZE[0]/2 + 50:
        cactus.flipped_x = True
    else:
        cactus.flipped_x = False

        #atack
    if not cactus.atack:
        cactus_idle_ticks += 1
        if cactus_idle_ticks >= cactus_idle_time:
            cactus_idle_ticks = 0
            cactus_idle_time = randint(cactus_idle_time_range[0], cactus_idle_time_range[1])
            cactus.atack = True
            cactus.action = 'atack'
    else:
        if cactus.actual_atack == '1':
            shot_ticks += 1
            if shot_ticks > 17:
                shot_ticks = 0
                hyp = hypot((player.x - cactus.x), (player.y - cactus.y))
                if  hyp == 0:
                    c, s = 0, 0
                else:
                    c = (player.x - cactus.x) / hyp
                    s = (player.y - cactus.y) / hyp

                width = 16 
                height = 6
                rot_angle = degrees(atan2(-s, c))
                shot = Obj(cactus.x, cactus.y, width, height, thorn_img)
                shots.append({'shot' : shot, 'angle' : [c * shots_vel, s * shots_vel], 'rot_angle' : rot_angle})

    #player
    player.draw(display, -scroll_x, -scroll_y)
    player.collision_move(tiles)
    player.update()
    player.anim()

    if player.x_momentum != 0:
        player.action = 'run'
    else:
        player.action = 'idle'

    #shots
    for i, key in sorted(enumerate(shots), reverse= True):
        shot = key['shot']
        angle = key['angle']
        rot_angle = key['rot_angle']

        shot.draw(display, -scroll_x, -scroll_y, rot_angle)
        shot.x += angle[0]
        shot.y += angle[1]

        #outing window
        if shot.x >= DISPLAY_SIZE[0] + scroll_x + shot.width or shot.x < 0 - scroll_x - shot.width:
            shots.pop(i)

        if shot.y >= DISPLAY_SIZE[1] + scroll_y + shot.height or shot.y < 0 - scroll_y - shot.height:
            shots.pop(i)
        
        if shot.rect.colliderect(player.rect):
            shots.pop(i)
            player.life -= 5

    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(fps)