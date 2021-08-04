import pygame, sys
pygame.init()

from scripts.config import *
from scripts.scenes.level1 import Level1
from scripts.scenes.restartmenu import RestartMenu
from scripts.scenes.winmenu import WinMenu

class Game:
    def __init__(self):
        #SCENES
        self.actual_scene = self.change_scene('restartmenu')
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
                    self.actual_scene = self.change_scene(new_scene)

        pygame.quit()
        sys.exit() 

    def change_scene(self, new_scene):
        if new_scene == 'restartmenu':
            return RestartMenu()

        if new_scene == 'level1':
            return Level1()

        if new_scene == 'winmenu':
            return WinMenu()



if __name__ == '__main__':
    Game().update()


