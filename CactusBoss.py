import pygame, sys
pygame.init()

from scripts.config import *
from scripts import scenes

class Game:
    def __init__(self):
        #SCENES
        self.scene = scenes.RestartMenu()

    def update(self):
        while self.scene.loop:
            window.screen.fill((0, 0, 0))
            display.fill((0, 0, 0))

            clock.dt_update()
            clock.tick()
            clock.draw_fps(display, 5, 5, 8, 'assets/fonts/Comodore64.TTF')
            dt = clock.dt

            filtered_events, pressed_keys = self.get_events()

            self.scene.events(filtered_events, pressed_keys)
            self.scene.draw(display)
            self.scene.update(dt)

            self.scene = self.scene.next

            window.blit_display(zoom= camera.zoom)
            pygame.display.update()

    def get_events(self):
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                filtered_events.append(event)

        return filtered_events, pressed_keys

if __name__ == '__main__':
    Game().update()


