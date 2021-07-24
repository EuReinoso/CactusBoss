import pygame, sys, os
pygame.init()

from scripts.scenes.level1 import Level1
from scripts.pgengine import clock, Window, ImgsManager


class Game:
    def __init__(self):
        self.window  = Window(900, 600)

        #IMAGES
        imgs_path = 'assets/images/'
        self.imgs_mng = ImgsManager()
        self.imgs_mng.add_imgs_from_past(imgs_path)
        self.imgs_mng.add_animations_from_past(imgs_path + 'animations/')

        self.scenes = {'level1' : Level1(self)}
        self.actual_scene = self.scenes['level1']

    def update(self):
        while self.actual_scene.loop:
            self.actual_scene.events()
            self.actual_scene.draw()
            self.actual_scene.update()

            self.window.blit_display()
            pygame.display.update()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().update()


