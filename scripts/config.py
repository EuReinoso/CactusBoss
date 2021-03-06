from scripts.pgengine import ImgsManager, ObjsManager, Obj, Window, Camera, Clock, ParticleManager, SoundManager, load_map
from scripts.objs.player import Player
from scripts.objs.cactus1 import Cactus1
from scripts.objs.shot import Shot
from scripts.objs.lifebar import LifeBar

def reset():
    sound_mng.stop_music()
    particles_mng.particles = []
    camera.shake_ticks = 0

#WINDOW
window  = Window(900, 600, 'CactusBoss')
display = window.display

#CAMERA
camera = Camera(window)
camera.delay_x = 20
camera.delay_y = 20

#CLOCK
clock = Clock()
clock.fps = 144

#TILE
TILE_SIZE = 16

#SOUNDS
sound_mng = SoundManager()
sound_mng.add_sounds_from_past('assets/sounds/sfx/')
sound_mng.add_sounds_from_past('assets/sounds/musics/', 'mp3')
sound_mng.sounds['jump'].set_volume(0.5)
sound_mng.sounds['shot'].set_volume(0.5)
sound_mng.sounds['shot2'].set_volume(0.5)
sound_mng.sounds['cactus_powerup'].set_volume(0.3)
sound_mng.sounds['explosion'].set_volume(0.4)

#IMAGES
imgs_path = 'assets/images/'
imgs_mng = ImgsManager()
imgs_mng.add_imgs_from_past(imgs_path)
imgs_mng.add_animations_from_past(imgs_path + 'animations/')
IMGS = imgs_mng.imgs
ANIMATIONS = imgs_mng.animations

#OBJS
objs_mng = ObjsManager()
objs_mng.add_obj('mountains1', Obj(IMGS['background1']))
objs_mng.add_obj('mountains2', Obj(IMGS['background2']))
objs_mng.add_obj('tile_center', Obj(IMGS['tile1']))
objs_mng.add_obj('tile_ground', Obj(IMGS['tile2']))
objs_mng.add_obj('tile_left', Obj(IMGS['tile3']))
objs_mng.add_obj('tile_right', Obj(IMGS['tile4']))
objs_mng.add_obj('tile_f_center', Obj(IMGS['tile5']))
objs_mng.add_obj('tile_f_left', Obj(IMGS['tile6']))
objs_mng.add_obj('tile_f_right', Obj(IMGS['tile7']))
objs_mng.add_obj('player', Player(ANIMATIONS['player_idle'][0]))
objs_mng.add_obj('cactus1', Cactus1(ANIMATIONS['cactus_idle'][0]))
objs_mng.add_obj('thorn', Shot(IMGS['thorn']))
objs_mng.add_obj('lifebar', LifeBar(IMGS['lifebar_b']))
objs_mng.add_obj('liferect_r', Obj(IMGS['liferect_r']))
objs_mng.add_obj('liferect_g', Obj(IMGS['liferect_g']))
objs_mng.add_obj('player_life', Obj(IMGS['player_life']))

#OBJS CONFIG
OBJS = objs_mng.objs.copy()
    #bg
OBJS['mountains1'].y = 140
OBJS['mountains1'].x = display.get_width() / 2
OBJS['mountains1'].height = 150
OBJS['mountains1'].width = int(display.get_width() * 1.5)
OBJS['mountains2'].y = 90
OBJS['mountains2'].x = display.get_width() / 2
OBJS['mountains2'].height = 140
OBJS['mountains2'].width = int(display.get_width() * 1.5)

    #player
OBJS['player'].add_imgs_data(ANIMATIONS['player_idle'], 'idle', [15, 15])
OBJS['player'].add_imgs_data(ANIMATIONS['player_run'], 'run', [7, 7])
OBJS['player'].add_imgs_data(ANIMATIONS['player_damage'], 'damage', [2, 10])

    #cactuslifebar
OBJS['lifebar'].y = 10
OBJS['lifebar'].x = display.get_width() / 2
OBJS['lifebar'].height = 5
OBJS['lifebar'].width  = 200
OBJS['lifebar'].add_liferect(OBJS['liferect_r'])
OBJS['lifebar'].add_liferect(OBJS['liferect_g'])
    #cactus1
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_idle'], 'idle', [10, 10, 10, 10])
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_atack'], 'atack', [10, 10, 10, 10])
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_damage'], 'damage', [3, 3, 3, 3])
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_a_idle'], 'a_idle', [10, 10, 10, 10])
OBJS['cactus1'].add_imgs_data(ANIMATIONS['cactus_a_atack'], 'a_atack', [10, 10, 10, 10])

#PARTICLES
particles_mng = ParticleManager()

MAPS_PATH = {
    'tutorial' : 'assets/maps/tutorial_map.txt',
    'level1' :   'assets/maps/map1.txt',
    'level2' :   'assets/maps/map2.txt'
}
