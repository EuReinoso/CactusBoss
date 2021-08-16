import pygame, sys
pygame.init()

from scripts.config import OBJS, camera, particles_mng, sound_mng
from scripts.pgengine import *
from scripts.scenes.level import Level

class Level1(Level):
    def __init__(self, level_name):
        super().__init__(level_name)
        sound_mng.set_music('assets/sounds/musics/sidescroller.mp3')

        #OBJS ------------------------------------------------------------
        self.mountains1 = OBJS['mountains1'].get_copy()
        self.mountains2 = OBJS['mountains2'].get_copy()
        self.player = OBJS['player'].get_copy()
        self.cactus = OBJS['cactus1'].get_copy()

        #CONFIG
            # player
        self.player.x = 90
        self.player.y = 50
        self.player.init()
        self.lock_player = True

            #cactus
        cactus_tile = self.tiles[96]
        self.cactus.x = cactus_tile.x + 8
        self.cactus.y = cactus_tile.y - self.cactus.height/2 - cactus_tile.height/2
        self.cactus.init()

            #camera
        camera.target = self.player
        
        #cutscene stuff
        self.is_drawing_boss_name = False
        self.cutscene_ticks = 0
        self.win_ticks = 0

    def events(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()

            if not self.lock_player:
                self.player.control(event)

    def draw(self, display):
        display.fill((189, 149, 106))
        self.mountains2.draw(display, -int(camera.x * 0.3), -int(camera.y * 0.3))
        self.mountains1.draw(display, -int(camera.x * 0.6), -int(camera.y * 0.7))

        for tile in self.tiles:
            tile.draw(display, -camera.x, -camera.y)

        if not self.cactus.is_dead:
            self.cactus.draw(display, -camera.x, -camera.y)
            #ui
            self.cactus.lifebar.draw_liferects(display)
            self.cactus.lifebar.draw(display)

        #bossname
        if self.is_drawing_boss_name:
            draw_text(display, 'CACSHOTO', 160 - camera.x, 140 - camera.y, 15, 'assets/fonts/Comodore64.TTF')

        #player
        self.player.draw(display, -camera.x, -camera.y)
        for heart in self.player.hearts:
            heart.draw(display)
        
        #shots
        for shot in self.cactus.shots:
            shot.draw(display, -camera.x, -camera.y)

        #particles
        particles_mng.draw_particles(display, -camera.x, -camera.y)

    def update(self, dt):
        #CAMERA
        camera.limit([3, 97], [25, 35])
        camera.update(dt)

        #PLAYER
        self.player.update(dt)
        self.player.collision_move(self.tiles, dt)
        self.player.anim(dt)     
        if self.player.dead:
            self.change_scene('restartmenu')

        #CACTUS
        if not self.cactus.is_dead:
            self.cactus.update(self.player, dt)
            self.cactus.anim(dt)
        else:
            self.win_ticks += 1 * dt
            if int(self.win_ticks) > 200:
                self.change_scene('winmenu')
        #PARTICLES
        particles_mng.update(dt)
        
        #CUTSCENE
        if self.cutscene_ticks < 1000:
            self.update_cutscene(dt)

    def update_cutscene(self, dt):

        self.cutscene_ticks += 1 * dt
        self.cactus.idle_ticks = 0

        if int(self.cutscene_ticks) < 30:
            pass
        
        elif int(self.cutscene_ticks) == 30:
            sound_mng.sounds['level1_cutscene'].play()

        elif int(self.cutscene_ticks) >= 30 and int(self.cutscene_ticks) <= 160:
            camera.delay_x = 200
            camera.delay_y = 100
            camera.target = self.cactus

            if camera.zoom <= 2:
                camera.zoom += 0.01 * dt

            self.is_drawing_boss_name = True

        elif int(self.cutscene_ticks) >= 160 and int(self.cutscene_ticks) <= 170:
            self.is_drawing_boss_name = False

            camera.delay_x = 30
            camera.delay_y = 50 
            camera.target = self.player
            if camera.zoom > 1:
                camera.zoom -= 0.04 * dt

        else:
            sound_mng.play_music(0.15)
            self.cutscene_ticks = 1000
            self.lock_player = False
            camera.zoom = 1
            camera.delay_x = 20
            camera.delay_y = 50
