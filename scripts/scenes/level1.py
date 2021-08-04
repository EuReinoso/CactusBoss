import pygame, sys
pygame.init()

from scripts.config import OBJS, clock, display, camera, particles_mng
from scripts.pgengine import *
from scripts.scenes.scene import Scene

class Level1(Scene):
    def __init__(self):
        #MAP ------------------------------------------------------------
        self.map = load_map('assets/maps/map1.txt')
        self.tiles = self.load_tiles(self.map)

        #OBJS ------------------------------------------------------------
        self.mountains1 = OBJS['mountains1'].get_copy()
        self.mountains2 = OBJS['mountains2'].get_copy()
        self.player = OBJS['player'].get_copy()
        self.cactus = OBJS['cactus1'].get_copy()

        #CONFIG
            # player
        self.player.x = 90
        self.player.y = 50
        self.player.build_hearts()
        self.lock_player = True

            #cactus
        cactus_tile = self.tiles[96]
        self.cactus.x = cactus_tile.x + 8
        self.cactus.y = cactus_tile.y - self.cactus.height/2 - cactus_tile.height/2
        self.cactus.add_lifebar(OBJS['lifebar'].get_copy())
        self.cactus.init()

        #CAMERA
        camera.target = self.player

        self.cutscene_ticks = 0
        self.start = False
        
        self.win_ticks = 0

        self.loop = True
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    self.loop = False

            if not self.lock_player:
                self.player.control(event)

    def draw(self):
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

        #player
        self.player.draw(display, -camera.x, -camera.y)
        for heart in self.player.hearts:
            heart.draw(display)
        
        #shots
        for shot in self.cactus.shots:
            shot.draw(display, -camera.x, -camera.y)

        #particles
        particles_mng.draw_particles(display, -camera.x, -camera.y)

    def update(self):
        dt = clock.dt

        #CAMERA
        camera.limit([3, 97], [25, 35])
        camera.update(dt)

        #PLAYER
        self.player.update(dt)
        self.player.collision_move(self.tiles, dt)
        self.player.anim(dt)     
        if self.player.dead:
            self.restart()
            self.cactus.shots = []
            return 'restartmenu'

        #CACTUS
        if not self.cactus.is_dead:
            self.cactus.update(self.player, dt)
            self.cactus.anim(dt)
        else:
            self.win_ticks += 1 * dt
            if int(self.win_ticks) > 200:
                self.restart()
                self.cactus.shots = []
                return 'restartmenu'
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

        elif int(self.cutscene_ticks) >= 30 and int(self.cutscene_ticks) <= 160:
            camera.delay_x = 200
            camera.delay_y = 100
            camera.target = self.cactus

            if camera.zoom <= 2:
                camera.zoom += 0.01 * dt

            draw_text(display, 'CACSHOT', 160 - camera.x, 140 - camera.y, 15, 'assets/fonts/Comodore64.TTF')

        elif int(self.cutscene_ticks) >= 160 and int(self.cutscene_ticks) <= 170:
            camera.delay_x = 30
            camera.delay_y = 50 
            camera.target = self.player
            if camera.zoom > 1:
                camera.zoom -= 0.04 * dt

        else:
            self.cutscene_ticks = 1000
            self.lock_player = False
            camera.zoom = 1
            camera.delay_x = 20
            camera.delay_y = 50
    
