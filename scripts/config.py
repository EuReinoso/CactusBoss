from scripts.pgengine import ImgsManager, ObjsManager, Obj, Window, Camera, Clock
from scripts.objs.player import Player
from scripts.objs.cactus1 import Cactus1
from scripts.objs.shot import Shot

#WINDOW
window  = Window(900, 600)
display = window.display

#CAMERA
camera = Camera(window)
camera.delay_x = 15
camera.delay_y = 5

#CLOCK
clock = Clock()
clock.fps = 144

#TILE
TILE_SIZE = 16

#IMAGES
imgs_path = 'assets/images/'
imgs_mng = ImgsManager()
imgs_mng.add_imgs_from_past(imgs_path)
imgs_mng.add_animations_from_past(imgs_path + 'animations/')
IMGS = imgs_mng.imgs
ANIMATIONS = imgs_mng.animations

#OBJS
objs_mng = ObjsManager()
objs_mng.add_obj('bg', Obj(display.get_width()/2, display.get_height()/2, int(display.get_width() * 2), int(display.get_height() * 2), IMGS['background']))
objs_mng.add_obj('tile1', Obj(0, 0, TILE_SIZE, TILE_SIZE, IMGS['tile1']))
objs_mng.add_obj('tile2', Obj(0, 0, TILE_SIZE, TILE_SIZE, IMGS['tile2']))
objs_mng.add_obj('player', Player(50, 50, 11, 15, ANIMATIONS['player_idle'][0]))
objs_mng.add_obj('cactus1', Cactus1(1, 1, 80, 80, ANIMATIONS['cactus_idle'][0]))
objs_mng.add_obj('thorn', Shot(0, 0, IMGS['thorn'].get_width(), IMGS['thorn'].get_height(), IMGS['thorn']))

#OBJS CONFIG
OBJS = objs_mng.objs.copy()
    #player
OBJS['player'].add_imgs_data(ANIMATIONS['player_idle'], 'idle', [15, 15])
OBJS['player'].add_imgs_data(ANIMATIONS['player_run'], 'run', [10, 10])
OBJS['player'].action = 'idle'
    #cactus1
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_idle'], 'idle', [10, 10, 10, 10])
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_atack'], 'atack', [10, 10, 10, 10])
OBJS['cactus1'].action = 'idle'