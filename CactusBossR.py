import pygame, sys
pygame.init()

from scripts.scenes.level1 import Level1

WINDOW_SIZE = (900, 600)
DISPLAY_SIZE = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[1]/3))

class Game:
    def __init__(self):
        print('window')
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE)

        self.scenes = {'level1' : Level1(self.display)}
        self.actual_scene = self.scenes['level1']

    def update(self):
        while self.actual_scene.loop:
            self.actual_scene.events()
            self.actual_scene.draw()
            self.actual_scene.update()

            self.window.blit(pygame.transform.scale(self.display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().update()


