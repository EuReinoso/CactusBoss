import pygame
from scripts.pgengine import Platformer

pygame.init()


class Player(Platformer):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.xvel = 3
        self.jump_force = 3
        self.mass = 0.7