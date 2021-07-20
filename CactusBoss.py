import pygame,sys
from pygame.locals import *
from assets.pgengine import *
from random import randint, uniform, choice
from math import hypot, atan2, degrees, cos, sin, radians

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load('assets/sounds/Tapes.mp3')

class Player(Platformer):
    def __init__(self, x, y, width, height, img, xvel, jump_force):
        super().__init__(x, y, width, height,img,  xvel= xvel, jump_force= jump_force)
        self.life = 50

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.right = True
                self.flipped_x = False
            if event.key == pygame.K_LEFT:
                self.left = True
                self.flipped_x = True
            if event.key == pygame.K_UP:
                if self.jumps > 0:
                    self.jump()
                    jump_sfx.play()
                    self.jumps -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.right = False
            if event.key == pygame.K_LEFT:
                self.left = False

class Cactus1(Obj):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.is_atack = False
        self.atack_ticks = 0
        self.atacks = { '1' : {'time' : 560}, 
                        '2' : {'time' : 450}, 
                        '3': {'time' : 450}}
        self.atacks_list = ['1', '2', '3']
        self.actual_atack = '1'
        self.life = 200
        self.shot_ticks = 0

    def atack1(self, player, shots, shots_vel):
        self.shot_ticks  += 1
        if self.shot_ticks > 12:
            self.shot_ticks = 0
            hyp = hypot((player.x - self.x), (player.y - self.y))
            if  hyp == 0:
                c, s = 0, 0
            else:
                c = (player.x - self.x) / hyp *  shots_vel
                s = (player.y - self.y) / hyp * shots_vel
            width = 16 
            height = 6
            rot_angle = degrees(atan2(-s, c))
            shot = Obj(self.x, self.y, width, height, thorn_img)
            shots.append({'shot' : shot, 'angle' : [c , s ], 'rot_angle' : rot_angle})
            shot_sfx.play()

    def atack2(self, shots, shots_vel):
        self.shot_ticks += 1
        if self.shot_ticks > 2:
            self.shot_ticks = 0
            
            c =  cos(radians(uniform(0, 360))) * shots_vel 
            s =  sin(radians(uniform(0, 360))) * shots_vel

            while abs(c) < shots_vel and abs(s) < shots_vel:
                c *= 1.01
                s *= 1.01

            width = 16 
            height = 6
            rot_angle = degrees(atan2(-s, c))
            shot = Obj(self.x, self.y, width, height, thorn_img)
            shots.append({'shot' : shot, 'angle' : [c , s], 'rot_angle' : rot_angle})
            shot_sfx.play()
    
    def atack3(self, shots, shots_vel):
        self.shot_ticks += 1
        if self.shot_ticks > 25:
            self.shot_ticks = 0

            angle = randint(0, 30)
            space = randint(360/20, 360/10)
            for _ in range(int(360/space)):
                c =  cos(radians(angle)) * shots_vel
                s =  sin(radians(angle)) * shots_vel
                angle -= space
                width = 16 
                height = 6
                rot_angle = degrees(atan2(-s, c))
                shot = Obj(self.x, self.y, width, height, thorn_img)
                shots.append({'shot' : shot, 'angle' : [c , s], 'rot_angle' : rot_angle})
            shot_sfx.play()

class Cactus2(Rigidbody):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.is_atack = False
        self.atack_ticks = 0
        self.atacks = { '1' : {'time' : 500}, '2': {'time' : 300}}
        self.atacks_list = ['1', '2']
        self.actual_atack = choice(self.atacks_list)
        self.life = 200
        self.shot_ticks = 0
        self.action = 'idle'
        self.jump_force = 7
        self.total_jumps = 1

        self.air_time = 0
        self.count_air_time = False

        self.base_return_timer = 0

    def jump(self):
        self.y_momentum = - self.jump_force



WINDOW_SIZE = (900, 600)
DISPLAY_SIZE = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[1]/3))
TILE_SIZE = 16

pygame.display.set_caption('CactusBoss')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)

scroll_x, scroll_y = 0, 0
shake_ticks = 0
shake_intense = 0
offset = [0, 0]

#maps
map1         = load_map('assets/maps/map1.txt')
map2         = load_map('assets/maps/map2.txt')
tutorial_map = load_map('assets/maps/tutorial_map.txt')

#Images
path = 'assets/images/'

arrow_img         = load_img(path + 'arrows') 
thorn_img         = load_img(path + 'thorn')
tile1_img         = load_img(path + 'tile1')
tile2_img         = load_img(path + 'tile2')
lifebarb_img      = load_img(path + 'lifebar_b')
lifebarg_img      = load_img(path + 'lifebar_g')
bg_img            = load_img(path + 'background')
player_idle_imgs  = load_imgs_from_past(path + 'player_idle/')
player_run_imgs   = load_imgs_from_past(path + 'player_run/')
cactus_idle_imgs  = load_imgs_from_past(path + 'cactus_idle/')
cactus_atack_imgs = load_imgs_from_past(path + 'cactus_atack/')
cactus2_idle_imgs = load_imgs_from_past(path + 'cactus2_idle/')
cactus2_atack_imgs= load_imgs_from_past(path + 'cactus2_atack/')

#sounds
path = 'assets/sounds/'

jump_sfx      = load_sound(path + 'jump', 0.6)
shot_sfx      = load_sound(path + 'shot', vol= 0.5)
thornhit_sfx  = load_sound(path + 'thornhit')
hitcactus_sfx = load_sound(path + 'hitcactus')
lose_sfx      = load_sound(path + 'lose')
win_sfx       = load_sound(path + 'win')
tremor_sfx    = load_sound(path + 'tremor', vol= 0.5)

font_path = 'assets/fonts/Comodore64.TTF'

def load_tiles(map_data):
    tiles = []
    y = 0
    for row in map_data:
        x = 0
        for val in row:
            if val == '1':
                tiles.append(Obj(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, tile1_img))
            if val == '2':
                tiles.append(Obj(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, tile2_img))
            x += 1
        y += 1

    return tiles

def level1():
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1) 

    #load_map
    tiles = load_tiles(map1)

    #Objs
    bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0] * 2, DISPLAY_SIZE[1] * 2, img= bg_img)

    player = Player(100, 100, 11, 15, player_idle_imgs[0], xvel= 3, jump_force= 3)
    player.mass = 0.7
    player.action = 'idle'
    player.add_imgs_data(player_idle_imgs, 'idle', [15, 15])
    player.add_imgs_data(player_run_imgs, 'run', [10, 10])

    cactus_tile = tiles[96]
    cactus = Cactus1(cactus_tile.x, cactus_tile.y - cactus_tile.height/2 - 40, 80, 80, img= cactus_idle_imgs[0])
    cactus.action = 'idle'
    cactus.actual_atack = choice(cactus.atacks_list)
    cactus.add_imgs_data(cactus_idle_imgs, 'idle', [10, 10, 10, 10])
    cactus.add_imgs_data(cactus_atack_imgs, 'atack', [10, 10, 10, 10])
    cactus_idle_time_range = [150, 400]
    cactus_idle_time = 60
    cactus_idle_ticks = 0


    lifebar_player = Obj(int(DISPLAY_SIZE[0] * 0.1), int(DISPLAY_SIZE[1] * 0.95), player.life, 10, img= lifebarb_img)
    player_life_rect = [lifebar_player.x - lifebar_player.width/2 + 3, lifebar_player.y -lifebar_player.height/2, player.life - 5, 8] 

    lifebar_cactus = Obj(display.get_rect().centerx, int(DISPLAY_SIZE[1] * 0.05), cactus.life, 6, img= lifebarg_img)
    cactus_life_rect = [lifebar_cactus.x - lifebar_cactus.width/2 + 10, lifebar_cactus.y - lifebar_cactus.height/2 + 2, cactus.life - 15, 4]

    shots = []
    shots_vel = 2

    particles = []

    #scroll
    scroll_x, scroll_y = 0, 0
    shake_ticks = 0
    shake_intense = 0
    offset = [0, 0]

    status = ''

    loop = True
    while loop:

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
        
            #life
        if cactus.life <= 2:
            loop = False
            status = 'You Win!'
            win_sfx.play()

            #look at Player
        if player.x < DISPLAY_SIZE[0]/2 + 50:
            cactus.flipped_x = True
        else:
            cactus.flipped_x = False

            #atack
        if not cactus.is_atack:
            cactus_idle_ticks += 1
            if cactus_idle_ticks >= cactus_idle_time:
                cactus_idle_ticks = 0
                cactus_idle_time = randint(cactus_idle_time_range[0], cactus_idle_time_range[1])
                cactus.is_atack = True
                cactus.action = 'atack'
            else:
                draw_text_font(display, 'ATACK!', cactus.x - scroll_x - 20, cactus.y - 80 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                draw_text_font(display, '|', cactus.x - scroll_x, cactus.y - 60 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                draw_text_font(display, 'v', cactus.x - scroll_x, cactus.y - 50 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                if player.rect.right > cactus.rect.left + 22 and player.rect.left < cactus.rect.right - 17:
                    if player.rect.bottom > cactus.rect.top  + 15 and player.rect.top < cactus.rect.top + 15 and player.y_momentum > 0:
                        player.jump()
                        cactus.life -= 5
                        shake_ticks, shake_intense = 10, 10
                        hitcactus_sfx.play()
                        for _ in range(20):
                            particles.append(CircleParticle(player.x, player.y + 15, 10, type= 'dexplosion'))
        else:
            cactus.atack_ticks += 1
            if cactus.atack_ticks < cactus.atacks[cactus.actual_atack]['time'] and cactus.atack_ticks > 60:
                if cactus.actual_atack == '1':
                    cactus.atack1(player, shots, shots_vel)

                if cactus.actual_atack == '2':
                    cactus.atack2(shots, shots_vel)

                if cactus.actual_atack == '3':
                    cactus.atack3(shots, shots_vel)

            if cactus.atack_ticks > cactus.atacks[cactus.actual_atack]['time']:   
                cactus.atack_ticks = 0
                cactus.is_atack = False
                cactus.action = 'idle'
                cactus.actual_atack = choice(cactus.atacks_list)

        #player
        player.draw(display, -scroll_x, -scroll_y)
        player.collision_move(tiles)
        player.update()
        player.anim()

        if player.x_momentum != 0:
            player.action = 'run'
        else:
            player.action = 'idle'

        if player.life <= 0:
            loop = False
            status = 'You Lose!'
            lose_sfx.play()

        #shots
        for i, key in sorted(enumerate(shots), reverse= True):
            shot = key['shot']
            angle = key['angle']
            rot_angle = key['rot_angle']

            shot.draw(display, -scroll_x, -scroll_y, rot_angle)
            shot.x += angle[0]
            shot.y += angle[1]

            #outing window
            if shot.x >= DISPLAY_SIZE[0] + scroll_x + shot.width or shot.x < 0 - scroll_x - shot.width  or shot.y >= DISPLAY_SIZE[1] + scroll_y + shot.height or shot.y < 0 - scroll_y - shot.height:
                shots.pop(i)
            else:
                #shot player
                if shot.rect.colliderect(player.rect):
                    shots.pop(i)
                    player.life -= 2
                    shake_ticks, shake_intense = 5, 5
                    thornhit_sfx.play()
                    for _ in range(10):
                        particles.append(CircleParticle(shot.x, shot.y, 5, type= 'dexplosion'))

        #particles
        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.draw(display, -scroll_x, -scroll_y)
            particle.update()

            if particle.radius <= 0:
                particles.pop(i)

        #UI
        pygame.draw.rect(display,(0, 200, 0), player_life_rect)
        lifebar_player.draw(display)
        player_life_rect = [lifebar_player.x - lifebar_player.width/2 + 3, lifebar_player.y -lifebar_player.height/2, player.life - 5, 8] 

        pygame.draw.rect(display, (200, 0, 0), cactus_life_rect)
        lifebar_cactus.draw(display)
        cactus_life_rect = [lifebar_cactus.x - lifebar_cactus.width/2 + 10, lifebar_cactus.y - lifebar_cactus.height/2 + 2, cactus.life - 15, 4]

        draw_fps(display, 3, 3, 7, font_path)

        #window
        scroll_x += int((player.x - scroll_x - DISPLAY_SIZE[0]/2)/10)
        scroll_y += int((player.y - scroll_y - DISPLAY_SIZE[1]/2)/30)
        
        scroll_x = scroll_limit(scroll_x, (-8, int(DISPLAY_SIZE[0]/2.8)))
        scroll_y = scroll_limit(scroll_y, (30, int(DISPLAY_SIZE[1]/5)))

        offset, shake_ticks,shake_intense = shake_screen(shake_ticks, shake_intense)

        window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0 + offset[0], 0 + offset[1]))
        pygame.display.update()
        clock.tick(fps)
    
    return status

def menu(text):
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1) 

    bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0] + 50, DISPLAY_SIZE[1] + 50, img= bg_img)

    shake = True
    offset = [0, 0]
    loop = True
    while loop:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = False

        #bg 
        bg.draw(display, offset[0], offset[1])

        #UI
        draw_text_font(display, text, display.get_rect().center[0] - 100, display.get_rect().center[1], 30, font= font_path)
        draw_text_font(display, 'SPACE TO PLAY AGAIN', display.get_rect().center[0] - 110, display.get_rect().center[1] + 40, 15, font= font_path)
        if shake:
            offset = [randint(-1, 1), randint(-1, 1)]
        else:
            offset = [0, 0]

        window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(fps)

def level2():
    global shake_ticks, shake_intense, offset

    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


    #objs
    bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0] * 2, DISPLAY_SIZE[1] * 2, img= bg_img)

    player = Player(100, 100, 11, 15, player_idle_imgs[0], xvel= 3, jump_force= 3)
    player.mass = 0.7
    player.action = 'idle'
    player.add_imgs_data(player_idle_imgs, 'idle', [15, 15])
    player.add_imgs_data(player_run_imgs, 'run', [10, 10])

    #cactus
    cactus = Cactus2(100, 100, 37 * 2, 26 * 2, cactus2_idle_imgs[0])
    cactus.add_imgs_data(cactus2_idle_imgs, 'idle', [10, 10, 10, 10])
    cactus.add_imgs_data(cactus2_atack_imgs, 'atack', [10, 10, 10, 10])
    cactus_idle_time_range = [120, 240]
    cactus_idle_time = 60
    cactus_idle_ticks = 0

    #ui
    lifebar_player = Obj(int(DISPLAY_SIZE[0] * 0.1), int(DISPLAY_SIZE[1] * 0.95), player.life, 10, img= lifebarb_img)
    player_life_rect = [lifebar_player.x - lifebar_player.width/2 + 3, lifebar_player.y -lifebar_player.height/2, player.life - 5, 8] 

    lifebar_cactus = Obj(display.get_rect().centerx, int(DISPLAY_SIZE[1] * 0.05), cactus.life, 6, img= lifebarg_img)
    cactus_life_rect = [lifebar_cactus.x - lifebar_cactus.width/2 + 10, lifebar_cactus.y - lifebar_cactus.height/2 + 2, cactus.life - 15, 4]


    #map
    tiles = load_tiles(map2) 

    #scroll
    scroll_x, scroll_y = 0, 0
    
    particles = []

    status = ''

    loop = True
    while loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            player.control(event)

        display.fill((0, 0, 0))

        #bg
        bg.draw(display, int(-scroll_x * 0.3), int(-scroll_y * 0.3))

        #cactus
        cactus.draw(display, -scroll_x, -scroll_y)
        cactus.update()
        cactus.collision_move(tiles)
        cactus.anim()

        if not cactus.is_atack:
            cactus_idle_ticks += 1
            if cactus_idle_ticks >= cactus_idle_time:
                cactus_idle_ticks = 0
                cactus_idle_time = randint(cactus_idle_time_range[0], cactus_idle_time_range[1])
                cactus.is_atack = True
                cactus.action = 'atack'
                
            else:
                draw_text_font(display, 'ATACK!', cactus.x - scroll_x - 20, cactus.y - 80 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                draw_text_font(display, '|', cactus.x - scroll_x, cactus.y - 60 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                draw_text_font(display, 'v', cactus.x - scroll_x, cactus.y - 50 - scroll_y, 15, font= font_path, color= (0, 0, 0))
                if player.rect.right > cactus.rect.left + 22 and player.rect.left < cactus.rect.right - 17:
                    if player.rect.bottom > cactus.rect.top  + 15 and player.rect.top < cactus.rect.top + 15 and player.y_momentum > 0:
                        player.jump()
                        cactus.life -= 5
                        shake_ticks = 5
                        shake_intense = 5
                        hitcactus_sfx.play()
                        for _ in range(10):
                            particles.append(CircleParticle(player.x, player.y + player.height/2, 10, type= 'dexplosion'))
        else:
            cactus.atack_ticks += 1
            if cactus.atack_ticks < cactus.atacks[cactus.actual_atack]['time'] and cactus.atack_ticks > 20:
                if cactus.actual_atack == '1':
                    if cactus.collide['bottom']:
                        cactus.jump()
                        shake_ticks = 10
                        shake_intense = 10
                        tremor_sfx.play()
                        for _ in range(15):
                            particles.append(CircleParticle(cactus.x, cactus.y + cactus.height/2, 13, type= 'dexplosion'))
                        if player.x > cactus.x:
                            cactus.flipped_x = False
                            cactus.x_momentum = 2
                        else:
                            cactus.flipped_x = True
                            cactus.x_momentum = - 2

                    if (cactus.collide['right'] and cactus.x_momentum > 8) or (cactus.collide['left'] and cactus.x_momentum < 8):
                        cactus.atack_ticks = cactus.atacks['1']['time']
                        cactus.x_momentum = 0
                        hitcactus_sfx.play()
                        if cactus.collide['right']:
                            for _ in range(15):  
                                particles.append(CircleParticle(cactus.x + cactus.width/2, cactus.y, 13, type= 'dexplosion'))
                        if cactus.collide['left']:
                            for _ in range(15):  
                                particles.append(CircleParticle(cactus.x - cactus.width/2, cactus.y, 13, type= 'dexplosion'))


                if cactus.actual_atack == '2':
                    if cactus.collide['bottom']:
                        cactus.jump()
                        cactus.air_time = 0
                        shake_ticks = 10
                        shake_intense = 10
                        tremor_sfx.play()
                        for _ in range(15):
                            particles.append(CircleParticle(cactus.x, cactus.y + cactus.height/2, 13, type= 'dexplosion'))
                        if player.x > cactus.x:
                            cactus.flipped_x = False
                            cactus.x_momentum = 5
                        else:
                            cactus.flipped_x = True
                            cactus.x_momentum = -5
                    else: 
                        if (cactus.x > player.x and cactus.x_momentum > 0) or (cactus.x < player.x and cactus.x_momentum < 0):
                            cactus.x_momentum = 0
                            cactus.gravity = False
                            cactus.y_momentum = 0
                            cactus.count_air_time = True
                        if cactus.count_air_time:
                            cactus.air_time += 1
                        if cactus.air_time > 10:
                            cactus.count_air_time = False
                            cactus.gravity = True
                            cactus.y_momentum += 3

            if cactus.atack_ticks > cactus.atacks[cactus.actual_atack]['time']:
                cactus.atack_ticks = 0
                cactus.is_atack = False
                cactus.action = 'idle'
                cactus.gravity = True

                if cactus.actual_atack == '1':
                    cactus.actual_atack = choice(['2'])
                else:
                    cactus.actual_atack = choice(['1','2'])

                
        
        #player
        player.draw(display, - scroll_x, - scroll_y)
        player.collision_move(tiles)
        player.update()
        player.anim()

        if player.x_momentum != 0:
            player.action = 'run'
        else:
            player.action = 'idle'

        #tiles
        for tile in tiles:
            tile.draw(display, -scroll_x, -scroll_y)

        #particles
        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.draw(display, -scroll_x, -scroll_y)
            particle.update()

            if particle.radius <= 0:
                particles.pop(i)

        #ui
        pygame.draw.rect(display,(0, 200, 0), player_life_rect)
        lifebar_player.draw(display)
        player_life_rect = [lifebar_player.x - lifebar_player.width/2 + 3, lifebar_player.y -lifebar_player.height/2, player.life - 5, 8] 

        pygame.draw.rect(display, (200, 0, 0), cactus_life_rect)
        lifebar_cactus.draw(display)
        cactus_life_rect = [lifebar_cactus.x - lifebar_cactus.width/2 + 10, lifebar_cactus.y - lifebar_cactus.height/2 + 2, cactus.life - 15, 4]


        #window
        scroll_x += int((player.x - scroll_x - DISPLAY_SIZE[0]/2)/10)
        scroll_y += int((player.y - scroll_y - DISPLAY_SIZE[1]/2)/30)
        
        scroll_x = scroll_limit(scroll_x, (-8, int(DISPLAY_SIZE[0]/2.8)))
        scroll_y = scroll_limit(scroll_y, (-1000, -35))

        offset, shake_ticks,shake_intense = shake_screen(shake_ticks, shake_intense)

        window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0 + offset[0], 0 + offset[1]))
        pygame.display.update()
        clock.tick(fps)

def tutorial():
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1) 

    #load_map
    tiles = load_tiles(tutorial_map)

    #Objs
    arrow = Obj(160, 40, 100, 60, arrow_img)

    bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0] * 2, DISPLAY_SIZE[1] * 2, img= bg_img)

    player = Player(50, 100, 11, 15, player_idle_imgs[0], xvel= 3, jump_force= 3)
    player.mass = 0.7
    player.action = 'idle'
    player.add_imgs_data(player_idle_imgs, 'idle', [15, 15])
    player.add_imgs_data(player_run_imgs, 'run', [10, 10])

    cactus_tile = tiles[68]
    cactus = Cactus1(cactus_tile.x, cactus_tile.y - cactus_tile.height/2 - 40, 80, 80, img= cactus_idle_imgs[0])
    cactus.action = 'idle'
    cactus.add_imgs_data(cactus_idle_imgs, 'idle', [10, 10, 10, 10])

    #particles
    particles = []

    #scroll
    scroll_x, scroll_y = 0, 0
    shake_ticks = 0
    shake_intense = 0
    offset = [0, 0]
    loop = True
    while loop:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = False
            player.control(event)
        #bg 
        bg.draw(display, offset[0], offset[1])

        #tiles
        for tile in tiles:
            tile.draw(display, -scroll_x, -scroll_y)

        #UI
        draw_text_font(display, 'DOUBLE JUMP!', 250 - scroll_x, 50 - scroll_y, 10, font= font_path, color= (0, 0, 0))
        draw_text_font(display, '------------>', 240 - scroll_x, 60 - scroll_y, 10, font= font_path, color= (0, 0, 0)) 

        # cactus
        cactus.draw(display, -scroll_x, -scroll_y)
        cactus.anim()
        
        draw_text_font(display, 'JUMP', cactus.x - scroll_x - 20, cactus.y - 100 - scroll_y, 15, font= font_path, color= (0, 0, 0))
        draw_text_font(display, 'ATACK!', cactus.x - scroll_x - 20, cactus.y - 80 - scroll_y, 15, font= font_path, color= (0, 0, 0))
        draw_text_font(display, '|', cactus.x - scroll_x, cactus.y - 60 - scroll_y, 15, font= font_path, color= (0, 0, 0))
        draw_text_font(display, 'v', cactus.x - scroll_x, cactus.y - 50 - scroll_y, 15, font= font_path, color= (0, 0, 0))
        if player.rect.right > cactus.rect.left + 15 and player.rect.left < cactus.rect.right - 15:
            if player.rect.bottom > cactus.rect.top  + 15 and player.rect.top < cactus.rect.top + 15 and player.y_momentum > 0:
                player.jump()
                shake_ticks = 5
                hitcactus_sfx.play()
                for _ in range(20):
                    particles.append(CircleParticle(player.x, player.y + 15, 10, type= 'dexplosion'))
                loop = False

        #player
        player.draw(display, -scroll_x, -scroll_y)
        player.update()
        player.collision_move(tiles)
        player.anim()

        if player.x_momentum != 0:
            player.action = 'run'
        else:
            player.action = 'idle'

        #particles
        for i, particle in sorted(enumerate(particles), reverse=True):
            particle.draw(display, -scroll_x, -scroll_y)
            particle.update()

            if particle.radius <= 0:
                particles.pop(i)

        #UI
        arrow.draw(display, -scroll_x, -scroll_y)

        
        #window
        scroll_x += int((player.x - scroll_x - DISPLAY_SIZE[0]/2)/10)
        scroll_y += int((player.y - scroll_y - DISPLAY_SIZE[1]/2)/30)
        
        scroll_x = scroll_limit(scroll_x, (-8, DISPLAY_SIZE[0]))
        scroll_y = scroll_limit(scroll_y, (-30, -30))

        offset, shake_ticks, shake_intense = shake_screen(shake_ticks, shake_intense)

        window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0 + offset[0], 0 + offset[1]))
        pygame.display.update()
        clock.tick(fps)

def main():

    is_tutorial = False
    while True:
        # if not is_tutorial:
        #     tutorial()
        #     is_tutorial = True

        # status = level1()
        # menu(status)

        status = level2()
        menu(status)

main()