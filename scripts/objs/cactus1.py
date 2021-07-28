from scripts import config
from scripts.pgengine import Obj
from math import hypot, degrees, atan2
from random import randint

class Cactus1(Obj):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.life = 100

        self.shots = []
        self.atack_ticks = 0
        self.atack_time = {'1' : 300}
        self.atacks_list = ['1']
        self.actual_atack = '1'
        self.is_atack = False

        self.idle_time_range = [300, 450]
        self.idle_time = 120
        self.idle_ticks = 0
        self.shot_ticks = 0

    def init(self):
        #FUTURE POLISH - make shots coming out of mouth
        self.mouth_pos = (self.x , self.y )

    def look_player(self, player_x):
        if player_x < self.x:
            self.flipped_x = True
        else:
            self.flipped_x = False

    def update(self, player, dt):
        if self.is_atack:
            self.atack_update(player, dt)
        else:
            self.idle_update(player, dt)
        
        self.shots_update(player, dt)
        self.look_player(player.x)
    
    def idle_update(self, player, dt):
        self.idle_ticks += 1 * dt
        if self.idle_ticks > self.idle_time:
            self.idle_ticks = 0
            self.idle_time = self._get_idle_time()
            self.is_atack = True
            self.action = 'atack'
        else:
            if self.rect.colliderect(player.rect):
                if player.x > self.x - 13 and player.x < self.x + 13:
                    if player.rect.bottom > self.rect.top  + 16 and player.rect.top < self.rect.top + 16:
                        self.life -= 5 
                        player.jump()

    def atack_update(self, player, dt):
        self.atack_ticks += 1 * dt
        if self.atack_ticks > self.atack_time[self.actual_atack]:
            self.atack_ticks = 0
            self.is_atack = False
            self.action = 'idle'
        else:
            if self.atack_ticks > 80:
                if self.actual_atack == '1':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 15:
                        self.shot_ticks = 0
                        self.atack1(player.x, player.y)

    def atack1(self, player_x, player_y):
        hyp = hypot((player_x - self.mouth_pos[0]), (player_y - self.mouth_pos[1]))
        mov = [0, 0]
        if hyp != 0:
            mov[0] = (player_x - self.mouth_pos[0]) / hyp
            mov[1] = (player_y - self.mouth_pos[1]) / hyp
        
        rot_angle = degrees(atan2(-mov[1], mov[0]))
        shot = self.shot(mov, rot_angle, 3, config.OBJS['thorn'])
        self.shots.append(shot)
    
    def shot(self, mov, angle, vel, obj):
        shot = obj.get_copy()
        shot.x = self.mouth_pos[0]
        shot.y = self.mouth_pos[1]
        shot.mov = mov
        shot.rot_angle = angle
        shot.vel = vel
        return shot

    def shots_update(self, player, dt):
        for i, shot in sorted(enumerate(self.shots), reverse= True):
            shot.update(dt)

            #out of window
            if shot.x < 0 - shot.width or shot.x > config.display.get_width() + config.camera.x + shot.width or shot.y < - shot.height or shot.y > config.display.get_height() + config.camera.y  + shot.height:
                self.shots.pop(i)
            else:
                #collide player
                if shot.rect.colliderect(player.rect):
                    self.shots.pop(i)
                    player.life -= 1

    def _get_idle_time(self):
        return randint(self.idle_time_range[0], self.idle_time_range[1])


        
