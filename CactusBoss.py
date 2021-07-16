import pygame,sys
from pygame.locals import *
from assets.pgengine import *

pygame.init()

WINDOW_SIZE = (900, 600)
DISPLAY_SIZE = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[1]/3))

pygame.display.set_caption('CactusBoss')
window = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(DISPLAY_SIZE)

#Images
path = 'assets/images/'

bg_img = load_img(path + 'background')


bg = Obj(DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]/2, DISPLAY_SIZE[0], DISPLAY_SIZE[1], img= bg_img)

loop = True
while loop:

    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #BG
    bg.draw(display)

    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()