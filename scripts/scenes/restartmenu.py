import pygame, sys
from scripts.scenes.scene import Scene
from scripts.config import OBJS, camera, sound_mng
from math import sin
from scripts.pgengine import *

class RestartMenu(Scene):
    def __init__(self):
        super().__init__()
        sound_mng.set_music('assets/sounds/musics/desert.mp3')
        sound_mng.play_music(0.3)

        self.camera_ticks = 0

        self.mountains1 = OBJS['mountains1'].get_copy()
        self.mountains2 = OBJS['mountains2'].get_copy()

    def events(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.change_scene('level1')
    
    def draw(self, display):
        display.fill((189, 149, 106))
        self.mountains2.draw(display, -int(camera.x * 0.3), -int(camera.y * 0.3))
        self.mountains1.draw(display, -int(camera.x * 0.6), -int(camera.y * 0.7))

        draw_text(display, 'SPACE TO PLAY', 53, 45, 18, 'assets/fonts/Comodore64.TTF')

    def update(self, dt):

        #anim camera
        self.camera_ticks += 1 * dt
        if sin(self.camera_ticks/10) > 0:
            camera.x += 0.5
        else:
            camera.x -= 0.5
