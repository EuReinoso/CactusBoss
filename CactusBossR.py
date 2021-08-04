import pygame, sys
pygame.init()

from scripts.config import *
from scripts.scenes.level1 import Level1
from scripts.scenes.restartmenu import RestartMenu

class Game:
    def __init__(self):
        #SCENES
        self.scenes = {'level1' : Level1(), 'restartmenu' : RestartMenu()}
        self.actual_scene = self.scenes['restartmenu']
        self.loop = True

    def update(self):
        while self.loop:
            while self.actual_scene.loop:
                window.screen.fill((0, 0, 0))
                display.fill((0, 0, 0))

                self.actual_scene.events()
                self.actual_scene.draw()
                new_scene = self.actual_scene.update()
 
                clock.tick()
                clock.dt_update()
                clock.draw_fps(display, 5, 5, 8, 'assets/fonts/Comodore64.TTF')

                window.blit_display(zoom= camera.zoom)
                pygame.display.update()

                if new_scene != None:
                    self.actual_scene = self.scenes[new_scene]

        pygame.quit()
        sys.exit() 

if __name__ == '__main__':
    Game().update()


