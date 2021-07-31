import pygame
from scripts.pgengine import Platformer, get_hit_list, GRAVITY, CircleParticle
from scripts import config
from random import uniform

pygame.init()


class Player(Platformer):
    def __init__(self, img):
        super().__init__(img)
        self.life = 5
        self.hearts = []
        self.dead = False
        self.imuniti_ticks = 0

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
        self.move()
        self.y_momentum += GRAVITY * self.mass * dt


        if self.imuniti_ticks <= 0:
            if self.right or self.left:
                self.action = 'run'
            else:
                self.action = 'idle'
            
        self.imuniti_update(dt)
        
        self.hearts_update(dt)

    def move(self):
        if self.right:
            self.x_momentum = int(self.xvel) 
        elif self.left:
            self.x_momentum = - int(self.xvel)
        else:
            self.x_momentum = 0

    def build_hearts(self):
        x = 10
        y = 190
        for _ in range(self.life):
            heart = config.OBJS['player_life'].get_copy()
            heart.x = x
            heart.y = y
            heart.true_x = x
            heart.true_y = y
            x += 6
            self.hearts.append(heart)

    def del_heart(self):
        self.hearts.pop()

    def hearts_update(self, dt):
        if len(self.hearts) > 0:
            self.hearts[-1].x = self.hearts[-1].true_x
            self.hearts[-1].y = self.hearts[-1].true_y
            self.hearts[-1].x += uniform(-1, 1) * dt
            self.hearts[-1].y += uniform(-3, -2) * dt

    def damage(self):
        self.life -= 1
        self.imuniti_ticks = 15
        self.action = 'damage'
        if self.life == 0:
            self.dead = True
        if self.life >= 0:
            self.imuniti_ticks = 60
            self.del_heart()

        #vfx
        config.camera.shake([-2, 2], [-2, 2], 10)
        p1 = CircleParticle(5, typ= '360', x= self.x, y= self.y, mass= 0.6, mutation= -0.1,vel= 1, color= (200, 100, 100))
        p2 = CircleParticle(6, typ= '360', x= self.x, y= self.y, mass= 1, mutation= -0.2,vel= 3, color= (100, 50, 50))
        p3 = CircleParticle(4, typ= '360', x= self.x, y= self.y, mass= 0.2, mutation= -0.1,vel= 7, color= (100, 100, 100))
        config.particles_mng.add_particles(p1, 10)
        config.particles_mng.add_particles(p2, 20)
        config.particles_mng.add_particles(p3, 5)
        

    def imuniti_update(self, dt):
        if self.imuniti_ticks > 0:
            self.imuniti_ticks -= 1 * dt
            if int(self.imuniti_ticks) == 0:
                self.action = 'idle'


    