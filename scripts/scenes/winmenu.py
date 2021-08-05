import pygame, sys
from scripts.scenes.scene import Scene
from scripts.config import OBJS, display, camera, clock, sound_mng
from math import sin
from scripts.pgengine import *

class WinMenu(Scene):
    def __init__(self):
        super().__init__()
        sound_mng.set_music('assets/sounds/musics/desert.mp3')
        sound_mng.play_music(0.3)
        sound_mng.sounds['win'].play()

        self.end = False

        self.camera_ticks = 0

        self.mountains1 = OBJS['mountains1'].get_copy()
        self.mountains2 = OBJS['mountains2'].get_copy()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.end = True
    
    def draw(self):
        display.fill((189, 149, 106))
        self.mountains2.draw(display, -int(camera.x * 0.3), -int(camera.y * 0.3))
        self.mountains1.draw(display, -int(camera.x * 0.6), -int(camera.y * 0.7))

        draw_text(display, 'YOU WIN!', 80, 45, 18, 'assets/fonts/Comodore64.TTF')

    def update(self):
        clock.dt_update()
        dt = clock.dt

        if self.end:
            self.restart()
            return 'level1'

        #anim camera
        self.camera_ticks += 1 * dt
        if sin(self.camera_ticks/10) > 0:
            camera.x += 0.5
        else:
            camera.x -= 0.5