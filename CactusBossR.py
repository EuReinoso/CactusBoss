import pygame, sys
pygame.init()

from scripts.config import *
from scripts.scenes.level1 import Level1

class Game:
    def __init__(self):
        #SCENES
        self.scenes = {'level1' : Level1()}
        self.actual_scene = self.scenes['level1']
        self.loop = True

    def update(self):
        while self.loop:
            while self.actual_scene.loop:
                window.screen.fill((0, 0, 0))
                display.fill((0, 0, 0))

                self.actual_scene.events()
                self.actual_scene.draw()
                self.actual_scene.update()

                clock.tick()
                clock.dt_update()
                clock.draw_fps(display, 5, 5, 8, 'assets/fonts/Comodore64.TTF')

                window.blit_display(zoom= camera.zoom)
                pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().update()


