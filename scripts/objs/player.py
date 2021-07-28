import pygame
from pygame import display
from scripts.pgengine import Platformer, get_hit_list, GRAVITY
from scripts import config

pygame.init()


class Player(Platformer):
    def __init__(self, img):
        super().__init__(img)
        self.life = 10
        self.hearts = []

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.right = True
                self.flipped_x = False
            if event.key == pygame.K_LEFT:
                self.left = True
                self.flipped_x = True
            if event.key == pygame.K_UP:
                if self.jumps > 0:
                    self.jump()
                    self.jumps -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.right = False
            if event.key == pygame.K_LEFT:
                self.left = False

    def collision_move(self, tiles, dt):
        self.collide = {'top':False,'bottom':False,'right':False,'left':False}
        self.x += self.x_momentum * dt
        hit_list = get_hit_list(self.rect, tiles)
        for tile in hit_list:
            if self.x_momentum > 0:
                self.collide['right'] = True
                self.x = tile.rect.left - self.width/2
            elif self.x_momentum < 0:
                self.collide['left'] = True
                self.x = tile.rect.right + self.width/2
        self.y += self.y_momentum * dt
        hit_list = get_hit_list(self.rect, tiles)
        for tile in hit_list:
            if self.y_momentum > 0:
                self.collide['bottom'] = True
                self.y = tile.rect.top - self.height/2
                self.jumps = self.total_jumps
                self.y_momentum = 0
            elif self.y_momentum < 0:
                self.collide['top'] = True
                self.y = tile.rect.bottom + self.height/2  
                self.y_momentum = 0 

    def jump(self):
        self.y_momentum = - self.jump_force 

    def update(self, dt):
        if self.right:
            self.x_momentum = int(self.xvel) 
            self.action = 'run'
        elif self.left:
            self.x_momentum = - int(self.xvel)
            self.action = 'run'
        else:
            self.x_momentum = 0
            self.action = 'idle'
        
        if self.gravity:
            self.y_momentum += GRAVITY * self.mass * dt

    def build_hearts(self):
        x = 10
        y = 190
        for _ in range(self.life):
            heart = config.OBJS['player_life'].get_copy()
            heart.x = x
            heart.y = y
            x += 6
            self.hearts.append(heart)

    def del_heart(self):
        self.hearts.pop()


    