import pygame, sys
pygame.init()

from scripts.scenes.level1 import Level1
from scripts.pgengine import clock, Window, ImgsManager, ObjsManager, Obj, Camera
from scripts.objs.player import Player

TILE_SIZE = 16

class Game:
    def __init__(self):
        self.window  = Window(900, 600)
        self.display = self.window.display
        self.camera = Camera(self.window)

        #IMAGES
        imgs_path = 'assets/images/'
        self.imgs_mng = ImgsManager()
        self.imgs_mng.add_imgs_from_past(imgs_path)
        self.imgs_mng.add_animations_from_past(imgs_path + 'animations/')
        self.imgs = self.imgs_mng.imgs
        self.animations = self.imgs_mng.animations

        #OBJS
        self.objs_mng = ObjsManager()
        self.objs_mng.add_obj('bg', Obj(self.display.get_width()/2, self.display.get_height()/2, int(self.display.get_width() * 2), int(self.display.get_height() * 2), self.imgs['background']))
        self.objs_mng.add_obj('tile1', Obj(0, 0, TILE_SIZE, TILE_SIZE, self.imgs['tile1']))
        self.objs_mng.add_obj('tile2', Obj(0, 0, TILE_SIZE, TILE_SIZE, self.imgs['tile2']))
        self.objs_mng.add_obj('player', Player(50, 50, 11, 15, self.animations['player_idle'][0]))

        #OBJSCONFIG
        self.objs = self.objs_mng.objs
        self.objs['player'].add_imgs_data(self.animations['player_idle'], 'idle', [10, 10])
        self.objs['player'].add_imgs_data(self.animations['player_run'], 'run', [10, 10])
        self.objs['player'].action = 'idle'

        #SCENES
        self.scenes = {'level1' : Level1(self)}
        self.actual_scene = self.scenes['level1']

    def update(self):
        while self.actual_scene.loop:
            self.window.screen.fill((0, 0, 0))
            self.display.fill((0, 0, 0))

            self.actual_scene.events()
            self.actual_scene.draw()
            self.actual_scene.update()

            self.window.blit_display(zoom= self.camera.zoom)
            pygame.display.update()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().update()


