import pygame
pygame.init()

from scripts.pgengine import *

class Level1:
    def __init__(self, surface):
        self.surface = surface

        #IMAGES
        imgs_path = 'assets/images/'
        self.bg_img = load_img(imgs_path + 'background')

        #OBJS
        self.bg = Obj(self.surface.get_width()/2, self.surface.get_height()/2, int(self.surface.get_width() * 1.1), int(self.surface.get_height() * 1.1), self.bg_img) 

        self.loop = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

    def draw(self):
        self.bg.draw(self.surface)
    
    def update(self):
        pass        

