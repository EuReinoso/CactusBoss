import pygame
from math import sin, cos, radians
from random import random, uniform, randint
from typing import Type

pygame.init()
pygame.font.init()
pygame.mixer.init()

#globals
GRAVITY = 0.3
AIR_FORCE = 0.05
main_font = None

# Utility Stuff ---------------------------------------------------------------------------------#
def set_main_font(font_path):
    global main_font
    main_font = font_path

def draw_text(surface, text, x, y, size, font = None, color= (0, 0, 0)):
    if font == None:
        font = main_font
    text_font = pygame.font.Font(font, size)
    render = text_font.render(text, False, color)
    surface.blit(render, (x, y))

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
    return offset, ticks

def scroll_limit(scroll, limit):
    if scroll < limit[0]:
        scroll = limit[0] 
    elif scroll > limit[1]: 
        scroll = limit[1]

#CLOCK
from time import time

class Clock:
    def __init__(self):
        self.fps = 144
        self.clock = pygame.time.Clock()
        self.last_time = time()
        self.dt = time() - self.last_time

    def tick(self):
        self.clock.tick(self.fps)

    def dt_update(self):
        self.dt = time() - self.last_time
        self.dt *= 60
        self.last_time = time()

    def draw_fps(self, surface, x, y, size, font_path, color= (0, 0, 0)):
        font = pygame.font.Font(font_path, size)
        render = font.render(str(int(self.clock.get_fps())), False, color)
        surface.blit(render, (x, y))

#CAMERA

class Camera:
    def __init__(self, window):
        self.window = window
        self.display = window.display
        self._target = None
        self.x = 0
        self.y = 0
        self.angle = 0
        self.zoom = 1
        self.delay_x = 1
        self.delay_y = 1

    def update(self, dt):
        self.x += int((self.target.x  - self.x   - self.display.get_width() / 2) / self.delay_x * dt)
        self.y += int((self.target.y  - self.y   - self.display.get_height()/ 2) / self.delay_y * dt)

    def limit(self, limit_x, limit_y):
        if self.x < limit_x[0]:
            self.x = limit_x[0]
        if self.x > limit_x[1]:
            self.x = limit_x[1]

        if self.y < limit_y[0]:
            self.y = limit_y[0]
        if self.y > limit_y[1]:
            self.y = limit_y[1]


    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, target):
        self._target = target

#OBJSMANAGER
class ObjsManager:
    def __init__(self):
        self.objs = {}

    def add_obj(self, name, obj):
        self.objs[name] = obj


#IMAGESMANAGER
from os import walk

def load_img(path, a_type = 'png', colorkey= None):
    if colorkey == None:
        image = pygame.image.load(path + '.' + a_type).convert_alpha()
    else:
        image = pygame.image.load(path + '.' + a_type).convert()
        image.set_colorkey(colorkey)
    return image

def load_imgs_from_past(past_path, colorkey= None):
    imgs = []
    for _, _, files in walk(past_path):
        for file in files:
            imgs.append(load_img(past_path  + file, a_type= '', colorkey= colorkey))
    
    return imgs

class ImgsManager:
    def __init__(self):
        self.imgs = {}
        self.animations = {}

    def add_img(self, path : str, name : str, a_type : str = 'png', colorkey= None):
        if colorkey == None:
            image = pygame.image.load(path + '.' + a_type).convert_alpha()
        else:
            image = pygame.image.load(path + '.' + a_type).convert()
            image.set_colorkey(colorkey)

        self.imgs[name] = image

    def add_imgs_from_past(self, past_path : str, a_type= 'png' , colorkey= None):
        for _, _, files in walk(past_path):
            for file in files:
                file = file.removesuffix('.' + a_type)
                img = load_img(past_path  + file, a_type= a_type, colorkey= colorkey)
                self.imgs[file] = img
            break

    def add_animations_from_past(self, past_path : str, a_type= 'png', colorkey= None):
        """
        Given the path to an "animations" folder, 
        it navigates through all the folders inside it.
        And it adds a key to the self.animations attribute,
        that contains a list of all the images in the folder.
        The key for each images list is accessed by folder name.

        Issue:
            Split this method into two.
        """
        for root, dirs, _ in walk(past_path):
            for dir_name in dirs:
                imgs = []
                for _, _, files in walk(root + dir_name + '/'):
                    for file in files:
                        file = file.removesuffix('.' + a_type)
                        path = past_path + dir_name + '/' + file
                        img = load_img(path, a_type= a_type, colorkey= colorkey)
                        imgs.append(img)
                    break
                self.animations[dir_name] = imgs

#WINDOW MODULE
FULLSCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)

class Window:
    def __init__(self, width, height):
        self._width  = width
        self._height = height
        self.screen  = pygame.display.set_mode((width, height))
        self.display = pygame.Surface((int(width/3), int(height/3)))
        self.org_display = copy(self.display)

    def resize(self, width, height):
        self._width = width
        self._height = height
        self.screen = pygame.display.set_mode((width, height))
    
    def blit_display(self, zoom= 1):
        width  = int(self.width * zoom)
        height = int(self.height * zoom)
        pos_x = int(self.width/2 - width/2)
        pos_y = int(self.height/2 - height/2)
        self.screen.blit(pygame.transform.scale(self.display, (width, height)), (pos_x, pos_y))

    def get_size(self):
        return (self.width, self.height)

    def get_center(self):
        return (self.width/2, self.height/2)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

#OBJ
from copy import copy

class Obj:
    def __init__(self, img):
        self._height = img.get_height()
        self._width = img.get_width()
        self._img = img
        self.org_img = img
        self.x = 0
        self.y = 0
        self.imgs_data = {}
        self.frames_data = {}
        self.frame = 0
        self._action = None
        self.flipped_x = False
        self.flipped_y = False
        self.rot_angle = 0

    def draw(self, surface, scroll_x= 0, scroll_y= 0):
        img = pygame.transform.flip(self.img, self.flipped_x, self.flipped_y)
        img = pygame.transform.rotate(img, self.rot_angle)
        pos_x = int(self.x - self.width / 2 + scroll_x)
        pos_y = int(self.y - self.height / 2 + scroll_y)
        surface.blit(img, (pos_x , pos_y))

    def draw_rect(self, surface, scroll_x= 0, scroll_y = 0, color= (255, 255, 255)):
        pygame.draw.rect(surface, color, (self.rect.x + scroll_x, self.rect.y + scroll_y, self.rect.width, self.rect.height))
    
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

    def frame_update(self, frames, dt):
        self.frame += 1 * dt
        if self.frame >= frames:
            self.frame = 0

    def anim(self, dt):
        self.frame_update(len(self.frames_data[self.action]), dt)
        self.img = self.imgs_data[self.action][self.frames_data[self.action][int(self.frame)]]
    
    def perfect_collide(self, obj) -> bool:
        return self.mask.overlap(obj.mask, (obj.rect.topleft[0] - self.rect.topleft[0], obj.rect.topleft[1] - self.rect.topleft[1]))

    def get_copy(self):
        return copy(self)

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
    def __init__(self, img, mass = 1, gravity= True):
        super().__init__(img)
        self.mass = mass
        self.gravity = gravity
        self.y_momentum = 0
        self.x_momentum = 0
        self.collide = {'top' : False, 'bottom' : False, 'right' : False, 'left' : False}
    
    def update(self):
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
                self.y_momentum = 0
            elif self.y_momentum < 0:
                self.collide['top'] = True
                self.y = tile.rect.bottom + self.height/2  
                self.y_momentum = 0  

class Platformer(Rigidbody):
    def __init__(self, img):
        super().__init__(img)
        self.right = False
        self.left = False
        self.xvel = 1
        self.total_jumps = 1
        self.jump_force = 5
        self.jumps = 0

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
    def __init__(self, radius, type= None, color= (255, 255, 255)):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.mutation = 0
        self.mass = 1
        self.color = color
        self.air= False
        self.gravity = True
        self.y_momentum = 0
        self.x_momentum = 0

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
        


