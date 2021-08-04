import pygame
from math import sin, cos, radians
from random import random, uniform, randint

from pygame import mask

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

#PARTICLEMANAGER

class ParticleManager:
    def __init__(self):
        self.particles = []
        self.particle_types = {}

    def update(self, dt):
        for i, p in sorted(enumerate(self.particles), reverse= True):
            p.update(dt)

            if p.dead:
                self.particles.pop(i)

    def draw_particles(self, surface, scroll_x, scroll_y):
        for p in self.particles:
            p.draw(surface, scroll_x, scroll_y)

    def add_particles(self, particle, quant, **kwargs):
        for k, v in kwargs.items():
            if k in particle.__dict__:
                setattr(particle, k, v)
            else:
                raise KeyError(k)

        for _ in range(quant):
            particle.typ = particle.typ
            self.particles.append(particle.get_copy())

    def add_particle_type(self, name, radius, **kwargs):
        particle = CircleParticle(radius, **kwargs)
        self.particle_types[name] = particle

class CircleParticle:
    def __init__(self, radius, typ= None, color= (255, 255, 255), **kwargs):
        self.medium_size = uniform(0.5, 1)
        self.medium_vel = uniform(0.5, 1)
        self.radius = radius * self.medium_size
        self._typ = typ
        self.vel = 1 * self.medium_vel
        self.color = color
        self.x = 0
        self.y = 0
        self.mutation = 0
        self.mass = 1
        self.y_momentum = 0
        self.x_momentum = 0
        self.dead = False
        self.min_size = 0
        self.max_size = 1000

        self.typ = typ

        for k, v in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, v)
            else:
                raise KeyError(k)
    @property
    def typ(self):
        return self._typ
        
    @typ.setter
    def typ(self, typ):
        if typ == '360':
            self.x_momentum  =  cos(uniform(radians(0), radians(360))) * self.vel
            self.y_momentum  = sin(uniform(radians(0), radians(360))) * self.vel
        if typ == 'sides':
            if random() > 0.5:
                self.x_momentum  =  cos(uniform(radians(0), radians(-30))) * self.vel
                self.y_momentum  = sin(uniform(radians(0), radians(-30))) * self.vel
            else:
                self.x_momentum  =  cos(uniform(radians(180), radians(210))) * self.vel
                self.y_momentum  = sin(uniform(radians(180), radians(210))) * self.vel


    def draw(self, surface, scroll_x, scroll_y, flags=0):
        temp_surf = pygame.Surface((int(self.radius * 2), int(self.radius * 2)))
        temp_surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(temp_surf, self.color, (self.radius, self.radius), self.radius)
        surface.blit(temp_surf, (self.x - self.radius + scroll_x, self.y - self.radius + scroll_y), special_flags= flags)

    def update(self, dt):
        self.y += self.y_momentum * dt
        self.x += self.x_momentum * dt
        self.radius += self.mutation * dt
        self.y_momentum += GRAVITY * self.mass * dt

        if self.radius <= self.min_size or self.radius >= self.max_size:
            self.dead = True
    
    def get_copy(self):
        return copy(self)

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
        self.true_x = 0
        self.true_y = 0
        self.x = 0
        self.y = 0
        self.angle = 0
        self.zoom = 1
        self.delay_x = 1
        self.delay_y = 1
        self.shake_ticks = 0
        self.shake_x = [0, 0]
        self.shake_y = [0, 0]
        

    def update(self, dt):

        self.true_x += (self.target.x  - self.true_x  - self.display.get_width() / 2) / self.delay_x
        self.true_y += (self.target.y  - self.true_y  - self.display.get_height()/ 2) / self.delay_y
        self.x = int(copy(self.true_x))
        self.y = int(copy(self.true_y))

        self.shake_update(dt)

    def limit(self, limit_x, limit_y):
        if self.true_x * self.zoom < limit_x[0]:
           self.true_x = limit_x[0]
        if self.true_x > limit_x[1] * self.zoom:
           self.true_x = limit_x[1] * self.zoom
        
        if self.true_y * self.zoom < limit_y[0]:
           self.true_y = limit_y[0] 
        if self.true_y > limit_y[1] * self.zoom:
           self.true_y = limit_y[1] * self.zoom

    def shake(self, x_range, y_range, time):
        self.shake_ticks = time
        self.shake_x = x_range
        self.shake_y = y_range

    def shake_update(self, dt):
        if int(self.shake_ticks) > 0:
            self.shake_ticks -= 1 * dt
            self.x += randint(self.shake_x[0], self.shake_x[1])
            self.y += randint(self.shake_y[0], self.shake_y[1])

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
    def __init__(self, width, height, title = 'Game'):
        self._width  = width
        self._height = height
        self.title = title
        self.screen  = pygame.display.set_mode((width, height))
        self.display = pygame.Surface((int(width/3), int(height/3)))
        self.org_display = copy(self.display)

        pygame.display.set_caption(self.title)

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
    def __init__(self, img, **kwargs):
        self._height = img.get_height()
        self._width = img.get_width()
        self._img = img
        self.img = img
        self.org_img = img
        self.x = 0
        self.y = 0
        self.true_x = 0
        self.true_y = 0
        self.imgs_data = {}
        self.frames_data = {}
        self.frame = 0
        self._action = None
        self.flipped_x = False
        self.flipped_y = False
        self.rot_angle = 0
        self.outline = False
        self.outline_color = (255, 255, 255)

        for k, v in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, v)
            else:
                raise KeyError(k)

    def draw(self, surface, scroll_x= 0, scroll_y= 0):
        img = pygame.transform.flip(self.img, self.flipped_x, self.flipped_y)
        img = pygame.transform.rotate(img, self.rot_angle)
        pos_x = int(self.x - self.width / 2 + scroll_x)
        pos_y = int(self.y - self.height / 2 + scroll_y)

        if self.outline:
            self.draw_outline(surface, pos_x, pos_y)
            
        surface.blit(img, (pos_x , pos_y))

    def draw_outline(self, surface, pos_x, pos_y):
        mask_surf = self.mask.to_surface(setcolor= self.outline_color)
        mask_surf = pygame.transform.flip(mask_surf, self.flipped_x, self.flipped_y)
        mask_surf = pygame.transform.rotate(mask_surf, self.rot_angle)
        mask_surf.set_colorkey((0, 0, 0))
        surface.blit(mask_surf, (pos_x + 1, pos_y))
        surface.blit(mask_surf, (pos_x - 1, pos_y))
        surface.blit(mask_surf, (pos_x, pos_y + 1))
        surface.blit(mask_surf, (pos_x, pos_y - 1))

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


        


