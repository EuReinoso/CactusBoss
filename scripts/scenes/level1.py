import pygame
pygame.init()

from scripts.pgengine import *
from scripts.objs.player import Player

class Level1:
    def __init__(self, game):
        self.game    = game
        self.display = game.window.display
        self.objs    = game.objs_mng.objs.copy() 

        #OBJS ------------------------------------------------------------
            #bg
        self.bg = self.objs['bg']
            #player
        self.player = self.objs['player']
        
        #MAP ------------------------------------------------------------
        self.map = load_map('assets/maps/map1.txt')
        self.tiles = self.load_tiles(self.map)
        
        for tile in self.tiles:
            print(tile.x, tile.y)
        print(len(self.tiles))

        self.loop = True
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

            self.player.control(event)

    def draw(self):
        self.display.fill((0, 0, 0))

        self.bg.draw(self.display)

        for tile in self.tiles:
            tile.draw(self.display)

        self.player.draw(self.display)
    
    def update(self):
        #SCROLL

        #PLAYER
        self.player.update()
        self.player.collision_move(self.tiles)
        self.player.anim()     

    def load_tiles(self, map_data):
        tiles = []
        y = 0
        for row in map_data:
            x = 0
            for tile in row:
                is_tile = False
                if tile == '1':
                    new_tile = self.objs['tile1'].get_copy()
                    is_tile = True
                    
                if tile == '2':
                    new_tile = self.objs['tile2'].get_copy()
                    is_tile = True

                if is_tile:
                    new_tile.x = x * new_tile.width
                    new_tile.y = y * new_tile.height
                    tiles.append(new_tile)

                x += 1
            y += 1
        return tiles
