import pygame
from math import sin, cos, radians
from pygame.locals import *
from os import walk
from random import random, uniform, randint

pygame.init()
pygame.font.init()
pygame.mixer.init()

#globals
GRAVITY = 0.3
AIR_FORCE = 0.05
animation_img_data = {}
animation_frame_data = {}
fps = 60
clock = pygame.time.Clock()

# Utility Stuff ---------------------------------------------------------------------------------#
def draw_fps(surface, x, y, size, font, color= (0, 0, 0)):
    draw_text_font(surface, str(int(clock.get_fps())), x, y, size, font, color)

def draw_text_font(surface, text, x, y, size, font , color= (0, 0, 0)):
    text_font = pygame.font.Font(font, size)
    render = text_font.render(text, False, color)
    surface.blit(render, (x, y))

def load_img(path, colorkey= None, type = 'png'):
    if colorkey != None:
        image = pygame.image.load(path + '.' + type).convert()
        image.set_colorkey(colorkey)
    else:
        image = pygame.image.load(path + '.' + type)
    return image

def load_imgs_from_past(past_path, colorkey= None):
    imgs = []
    for _, _, archives in walk(past_path):
        for path_archive in archives:
            imgs.append(load_img(past_path  + path_archive, type= '', colorkey= colorkey))
    
    return imgs

def load_sound(path, vol = 1, format= '.wav'):
    sound = pygame.mixer.Sound(path + format)
    sound.set_volume(vol)
    return sound

def load_map(path):
    tiles_list = []
    file = open(path)
    lines = file.readlines()
    file.close()
    for line in lines:
        valors = []
        for val in line:
            valors.append(val)
        tiles_list.append(valors)
    return tiles_list

def get_hit_list(rect, objs):
    hit_list = []
    for obj in objs:
        if rect.colliderect(obj.rect):
            hit_list.append(obj)
    return hit_list

def shake_screen(ticks, intense):
    if ticks > 0:
        offset = [randint(-intense, intense), randint(-intense, intense)]
        ticks -= 1
    else:
        intense = 0
        offset = [0, 0]
    return offset, ticks, intense

def scroll_limit(scroll, limit):
    if scroll < limit[0]:
        scroll = limit[0]
    elif scroll > limit[1]:
        scroll = limit[1]
    return scroll


class Obj:
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self._img = img
        self.org_img = img
        self.img = pygame.transform.scale(self.img, (width, height))
        self.imgs_data = {}
        self.frames_data = {}
        self.frame = 0
        self._action = None
        self.flipped_x = False
        self.flipped_y = False

    def draw(self, surface, scroll_x= 0, scroll_y= 0, rot_angle =0):
        img = pygame.transform.flip(self.img, self.flipped_x, self.flipped_y)
        img = pygame.transform.rotate(img, rot_angle)
        surface.blit(img, ( self.x - self.width/2 + scroll_x, self.y - self.height/2 + scroll_y))

    def draw_rect(self, surface, color= (255, 255, 255)):
        pygame.draw.rect(surface, color, self.rect)
    
    def set_colorkey(self, colorkey= (255, 255, 255)):
        self.img.set_colorkey(colorkey)
        self.org_img.set_colorkey(colorkey)

    def add_imgs_data(self, imgs, name, frames_sequence):
        n = 0
        imgs_sequence = {}
        frames_list = []
        for sequence in frames_sequence:
            img_id = name + '_' + str(n)
            imgs_sequence[img_id] = imgs[n].copy()
            n += 1
            for i in range(sequence):
                frames_list.append(img_id)

        self.imgs_data[name] = imgs_sequence
        self.frames_data[name] = frames_list

    def frame_update(self, frames):
        self.frame += 1
        if self.frame >= frames:
            self.frame = 0

    def anim(self):
        self.frame_update(len(self.frames_data[self.action]))
        self.img = self.imgs_data[self.action][self.frames_data[self.action][self.frame]]
    
    def perfect_collide(self, obj) -> bool:
        return self.mask.overlap(obj.mask, (obj.rect.topleft[0] - self.rect.topleft[0], obj.rect.topleft[1] - self.rect.topleft[1]))

    @property
    def mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(self.img.convert_alpha())

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, new_action):
        if self.action != new_action:
            self._action = new_action
            self.frame = 0

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, img):
        self._img = pygame.transform.scale(img, (self.width, self.height))
        self.org_img = img

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value : int):
        self._width = value
        self.img = pygame.transform.scale(self.org_img, (value, self.height))
    
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        pygame.transform.scale(self.org_img, (self.width, value))

class Rigidbody(Obj):
    def __init__(self, x, y, width, height, img, mass = 1, gravity= True):
        super().__init__(x, y, width, height, img)
        self.mass = mass
        self.y_momentum = 0
        self.x_momentum = 0
        self.gravity = gravity
        self.collide = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}
    
    def update(self):
        if self.gravity:
            self.y_momentum += GRAVITY * self.mass


class Platformer(Rigidbody):
    def __init__(self, x, y, width, height, img, jump_force= 5, xvel= 1.5, total_jumps= 2):
        super().__init__(x, y, width, height, img)
        self.right = False
        self.left = False
        self.xvel = xvel
        self.jump_force = jump_force
        self.total_jumps = total_jumps
        self.jumps = 1

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
    
    def update(self):
        if self.right:
            self.x_momentum = int(self.xvel)
        elif self.left:
            self.x_momentum = - int(self.xvel)
        else:
            self.x_momentum = 0
        
        if self.gravity:
            self.y_momentum += GRAVITY * self.mass

    def collision_move(self, tiles):
        self.collide = {'top':False,'bottom':False,'right':False,'left':False}
        self.x += self.x_momentum
        hit_list = get_hit_list(self.rect, tiles)
        for tile in hit_list:
            if self.x_momentum > 0:
                self.collide['right'] = True
                self.x = tile.rect.left - self.width/2
            elif self.x_momentum < 0:
                self.collide['left'] = True
                self.x = tile.rect.right + self.width/2
        self.y += self.y_momentum
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

class CircleParticle:
    def __init__(self, x, y, radius, x_momentum= 0, y_momentum = 0, mass = 1, mutation= -0.5, air = True, gravity= True, type= None,  color= (255, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.mutation = mutation
        self.mass = mass
        self.color = color
        self.air= air
        self.gravity = gravity
        self.y_momentum = y_momentum
        self.x_momentum = x_momentum

        if type != None:
            if type == 'tinysmoke':
                self.mutation = 0.2
                self.mass = 0
                self.air = False
                self.gravity = False
                self.radius =  random() * radius
                self.x_momentum = cos(uniform(radians(-80), radians(-100)))
                self.y_momentum = sin(uniform(radians(-80), radians(-100)))
            if type == 'bigsmoke':
                self.mutation = 0.2
                self.mass = 0.0001
                self.radius =  random() * radius
                self.x_momentum = cos(uniform(radians(0), radians(180)))
            if type == 'explosion':
                self.mutation = 0.3
                self.mass = 0.1
                self.radius = random() *  radius
                self.air = False
                self.x_momentum  =  cos(uniform(radians(0), radians(360))) 
                self.y_momentum = sin(uniform(radians(0), radians(360)))
            if type == 'dexplosion':
                self.mutation = -0.3
                self.mass = 0.1
                self.radius = random() *  radius
                self.air = False
                self.x_momentum  =  cos(uniform(radians(0), radians(360))) 
                self.y_momentum = sin(uniform(radians(0), radians(360)))
            if type == 'fire':
                self.mutation = - 0.3
                self.mass = 1
                self.gravity = False
                self.radius = random() * radius
                self.x_momentum = cos(uniform(radians(-80), radians(-100))) * 10
                self.y_momentum = sin(uniform(radians(-80), radians(-100))) * 5
            if type == 'tinyup':
                self.mutation = - 0.2
                self.mass = 1
                self.radius = random() * radius
                self.x_momentum = cos(uniform(radians(-80), radians(-100))) * 10
                self.y_momentum = sin(uniform(radians(-80), radians(-100))) * 5
            if type == 'bigup':
                self.mutation = - 0.2
                self.mass = 1
                self.radius = random() * radius
                self.x_momentum = cos(uniform(radians(-60), radians(-120))) * 5
                self.y_momentum = sin(uniform(radians(-60), radians(-120))) * 5


    def draw(self, surface, scroll_x, scroll_y, flags=0):
        temp_surf = pygame.Surface((self.radius * 2, self.radius * 2))
        temp_surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(temp_surf, self.color, (self.radius, self.radius), self.radius)
        surface.blit(temp_surf, (self.x - self.radius + scroll_x, self.y - self.radius + scroll_y), special_flags= flags)

    def update(self):
        self.y += self.y_momentum
        self.x += self.x_momentum
        self.radius += self.mutation
        
        if self.gravity:
            self.y_momentum += (GRAVITY * self.mass) - AIR_FORCE      

        if self.air and self.x_momentum != 0:
            if self.x_momentum > 0:
                self.x_momentum -= AIR_FORCE 
            if self.x_momentum < 0:
                self.x_momentum += AIR_FORCE
        


