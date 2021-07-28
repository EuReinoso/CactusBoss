import pygame, sys
pygame.init()

from scripts.config import OBJS, clock, display, camera
from scripts.pgengine import *

class Level1:
    def __init__(self):
        #MAP ------------------------------------------------------------
        self.map = load_map('assets/maps/map1.txt')
        self.tiles = self.load_tiles(self.map)

        #OBJS ------------------------------------------------------------
        self.bg     = OBJS['bg'].get_copy()
        self.player = OBJS['player'].get_copy()
        self.cactus = OBJS['cactus1'].get_copy()

        #CONFIG
            #cactus
        cactus_tile = self.tiles[96]
        self.cactus.x = cactus_tile.x + 8
        self.cactus.y = cactus_tile.y - self.cactus.height/2 - cactus_tile.height/2
        self.cactus.init()

        #CAMERA
        camera.target = self.player
        
        self.loop = True
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    self.loop = False

            self.player.control(event)

    def draw(self):
        self.bg.draw(display, -int(camera.x * 0.5), -int(camera.y* 0.5))

        for tile in self.tiles:
            tile.draw(display, -camera.x, -camera.y)

        self.cactus.draw(display, -camera.x, -camera.y)
        for shot in self.cactus.shots:
            shot.draw(display, -camera.x, -camera.y)
            
        self.player.draw(display, -camera.x, -camera.y)

    
    def update(self):
        dt = clock.dt

        #CAMERA
        camera.update(dt)
        camera.limit([-8, 108], [25, 45])

        #PLAYER
        self.player.update(dt)
        self.player.collision_move(self.tiles, dt)
        self.player.anim(dt)     

        #CACTUS
        self.cactus.update(self.player, dt)
        self.cactus.anim(dt)

        #debug

    def load_tiles(self, map_data):
        tiles = []
        y = 0
        for row in map_data:
            x = 0
            for tile in row:
                is_tile = False
                if tile == '1':
                    new_tile = OBJS['tile1'].get_copy()
                    is_tile = True
                    
                if tile == '2':
                    new_tile = OBJS['tile2'].get_copy()
                    is_tile = True

                if is_tile:
                    new_tile.x = x * new_tile.width
                    new_tile.y = y * new_tile.height
                    tiles.append(new_tile)

                x += 1
            y += 1
        return tiles
