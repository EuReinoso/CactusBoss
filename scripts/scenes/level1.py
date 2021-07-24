import pygame
pygame.init()

from scripts.pgengine import *
from scripts.objs.player import Player

class Level1:
    def __init__(self, game):
        self.game       = game
        self.surface    = game.window.display
        self.imgs       = game.imgs_mng.imgs
        self.animations = game.imgs_mng.animations

        #OBJS ------------------------------------------------------------
        #bg
        self.bg = Obj(self.surface.get_width()/2, self.surface.get_height()/2, int(self.surface.get_width() * 1.1), int(self.surface.get_height() * 1.1), self.imgs['background']) 
        #player
        self.player = Player(50, 50, 11, 15, self.animations['player_idle'][0])
        self.player.add_imgs_data(self.animations['player_idle'], 'idle', [10, 10])
        self.player.action = 'idle'

        #MAP ------------------------------------------------------------
        self.map = load_map('assets/maps/map1.txt')
        self.tile_size = 16
        self.tiles = self.load_tiles(self.map)

        self.loop = True
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

            self.player.control(event)

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.bg.draw(self.surface)
        for tile in self.tiles:
            tile.draw(self.surface)

        self.player.draw(self.surface)
    
    def update(self):
        #SCROLL
        pass
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
                if tile == '1':
                    tiles.append(Obj(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, self.imgs['tile1']))
                if tile == '2':
                    tiles.append(Obj(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size, self.imgs['tile2']))
                x += 1
            y += 1
        
        return tiles


