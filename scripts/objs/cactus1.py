from scripts import config
from scripts.pgengine import Obj, CircleParticle
from math import hypot, degrees, atan2, radians, cos, sin, pi
from random import randint, choice, random

class Cactus1(Obj):
    def __init__(self, img):
        super().__init__(img)
        self.lifes = {'1' : 100, '2': 100}
        self.actual_life = '1'
        self.life = self.lifes[self.actual_life]
        self.is_dead = False

        self.shots = []
        self.atack_ticks = 0
        self.atack_time = {'1' : 350, '2' : 200, '3' : 300, 'a1' : 350, 'a2' : 400, 'a3' : 430, 'a4' : 400}
        self.atacks_list = ['1', '2', '3']
        self.a_atacks_list = ['a1', 'a2', 'a3', 'a4']
        self.actual_atack = '1'
        self.is_atack = False
        self.is_angry = True

        self.idle_time_range = [200, 350]
        self.idle_time = 120
        self.idle_ticks = 0
        self.shot_ticks = 0

        self.damage_ticks = 0

        self.angle_shot = 0
        self.rot_increase = 0.05
        self.shot_count = 0
        self.surprise_atack_ticks = 0

    def init(self):
        #FUTURE POLISH - make shots coming out of mouth
        self.mouth_pos = (self.x , self.y )

    def look_player(self, player_x):
        if player_x < self.x:
            self.flipped_x = True
        else:
            self.flipped_x = False

    def update(self, player, dt):
        if self.damage_ticks > 0:
            self.damage_update(dt)

        if self.is_atack:
            self.atack_update(player, dt)
        else:
            self.idle_update(player, dt)
        
        self.shots_update(player, dt)
        self.look_player(player.x)
        self.lifebar_update()

        if self.is_angry:
            self.surprise_atack_ticks += 1
            if self.surprise_atack_ticks > 350:
                self.surprise_atack_ticks = 0
                self.atacka4(player.x, player.y)

    def idle_update(self, player, dt):
        #outlineupdate
        if sin(self.idle_ticks/10) > 0:
            self.outline = True
        else:
            self.outline = False

        self.idle_ticks += 1 * dt
        if self.idle_ticks > self.idle_time:
            self.idle_ticks = 0
            self.idle_time = self._get_idle_time()
            self.is_atack = True

            if not self.is_angry:
                self.actual_atack = choice(self.atacks_list)
                self.action = 'atack'
            else:
                self.actual_atack = choice(self.a_atacks_list)
                self.action = 'a_atack'

                if self.actual_atack == 'a2':
                    if random() > 0.5:
                        self.rot_increase *= -1
                if self.actual_atack == 'a3':
                    if random() > 0.5:
                        self.angle_shot = radians(90)
                    else:
                        self.angle_shot = radians(270)
            self.outline = False
        else:
            if self.damage_ticks <= 0:
                if self.rect.colliderect(player.rect):
                    if player.x > self.x - 11 and player.x < self.x + 11:
                        if player.rect.bottom > self.rect.top  + 17 and player.rect.top < self.rect.top + 17:
                            self.damage()
                            player.jump()
                            player.jumps = 1
                            
                            #vfx
                            p1 = CircleParticle(10, typ= '360', x= player.x, y= player.y + 10, mass= 0.5, mutation= -0.2,vel= 3, color= (148, 138, 131))
                            p2 = CircleParticle(8, typ= '360', x= player.x, y= player.y + 10, mass= 1, mutation= -0.5, vel= 5, color= (148, 180, 131))
                            p3 = CircleParticle(5, typ= '360', x= player.x, y= player.y + 10, mass= 5, mutation= -0.2, vel= 10, color= (148, 180, 131))
                            config.particles_mng.add_particles(p1, 10)
                            config.particles_mng.add_particles(p2, 20)
                            config.particles_mng.add_particles(p3, 30)
                            

    def atack_update(self, player, dt):
        self.atack_ticks += 1 * dt
        if self.atack_ticks > self.atack_time[self.actual_atack]:
            self.atack_ticks = 0
            self.is_atack = False

            if self.is_angry:
                self.action = 'a_idle'
            else:
                self.action = 'idle'
        else:
            if self.atack_ticks > 80:
                if self.actual_atack == '1':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 8:
                        self.shot_ticks = 0
                        self.atack1(player.x, player.y)
                if self.actual_atack == '2':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 2:
                        self.shot_ticks = 0
                        self.atack2()
                if self.actual_atack == '3':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 15:
                        self.shot_ticks = 0
                        self.atack3()
                if self.actual_atack == 'a1':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 30:
                        self.shot_ticks = 0
                        self.atacka1(player.x, player.y)
                if self.actual_atack == 'a2':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 5:
                        self.angle_shot += self.rot_increase
                        self.shot_ticks = 0
                        self.atacka2()
                if self.actual_atack == 'a3':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 25:
                        self.shot_ticks = 0
                        self.atacka3()
                        self.angle_shot += radians(13)
                if self.actual_atack == 'a4':
                    self.shot_ticks += 1 * dt
                    if self.shot_ticks > 5:
                        self.shot_ticks = 0
                        self.atacka4(player.x, player.y)

    def atack1(self, player_x, player_y):
        hyp = hypot((player_x - self.mouth_pos[0]), (player_y - self.mouth_pos[1]))
        mov = [0, 0]
        if hyp != 0:
            mov[0] = (player_x - self.mouth_pos[0]) / hyp
            mov[1] = (player_y - self.mouth_pos[1]) / hyp
        
        rot_angle = degrees(atan2(-mov[1], mov[0]))
        shot = self.shot(mov, rot_angle, 2, config.OBJS['thorn'])
        self.shots.append(shot)

    def atack2(self):
        angle = radians(randint(0, 360))

        c = cos(angle)
        s = sin(angle)

        rot_angle  = degrees(atan2(-s, c))
        shot = self.shot([c, s], rot_angle, 1, config.OBJS['thorn'])
        self.shots.append(shot)

    def atack3(self):
        angle = radians(randint(0, 360))
        space = radians(360//5)
        for _ in range(int(2*pi/space)):
            c = cos(angle)
            s = sin(angle)

            rot_angle = degrees(atan2(-s, c))
            shot = self.shot([c, s], rot_angle, 2, config.OBJS['thorn'])
            self.shots.append(shot)
            angle += space

    def atacka1(self, player_x, player_y):

        hyp  = hypot((player_x - self.mouth_pos[0]), (player_y - self.mouth_pos[1]))
        mov  = [0, 0]
        if hyp != 0:
            mov[0]  = (player_x  - self.mouth_pos[0]) / hyp
            mov[1]  = (player_y  - self.mouth_pos[1]) / hyp

        rot_angle = degrees(atan2(-mov[1] , mov[0] ))
        
        sep = 50
        angle1 = radians(sep) + radians(rot_angle)
        angle2 = -radians(sep) + radians(rot_angle)
        mov1 = [cos(angle1), - sin(angle1)]
        mov2 = [cos(angle2), - sin(angle2)]

        rot_angle1 = degrees(atan2(-mov1[1], mov1[0]))
        rot_angle2 = degrees(atan2(-mov2[1], mov2[0]))
        
        shot  = self.shot(mov , rot_angle , 2, config.OBJS['thorn'], (200, 0, 0), 1.5)
        shot1 = self.shot(mov1, rot_angle1, 2, config.OBJS['thorn'], (200, 0, 0), 1.5)
        shot2 = self.shot(mov2, rot_angle2, 2, config.OBJS['thorn'], (200, 0, 0), 1.5)

        self.shots.append(shot )
        self.shots.append(shot1)
        self.shots.append(shot2)

    def atacka2(self):
        angle = self.angle_shot
        space = radians(360//5)
        for _ in range(int(2*pi/space)):
            c = cos(angle)
            s = sin(angle)

            rot_angle = degrees(atan2(-s, c))
            shot = self.shot([c, s], rot_angle, 2, config.OBJS['thorn'], (200, 0, 0), 0.5)
            self.shots.append(shot)
            angle += space

    def atacka3(self):
        angle  = self.angle_shot
        angle1 = -self.angle_shot  + radians(180)

        c = cos(angle)
        s = sin(angle)

        c1 = cos(angle1)
        s1 = sin(angle1)

        rot_angle  = degrees(atan2(-s, c))
        rot_angle1 = degrees(atan2(-s1, c1))
        shot = self.shot([c, s], rot_angle, 3, config.OBJS['thorn'], (200, 0, 0), 3)
        shot1 = self.shot([c1, s1], rot_angle1, 3, config.OBJS['thorn'], (200, 0, 0), 3)
        self.shots.append(shot)
        self.shots.append(shot1)

    def atacka4(self, player_x, player_y):
        x_pos = randint(0, config.camera.display.get_width()) + config.camera.x
        y_pos = -10 + config.camera.y
        hyp = hypot((player_x - x_pos), (player_y - y_pos))
        mov = [0, 0]
        if hyp != 0:
            mov[0] = (player_x - x_pos) / hyp
            mov[1] = (player_y - y_pos) / hyp
        
        rot_angle = degrees(atan2(-mov[1], mov[0]))
        shot = self.shot(mov, rot_angle, 2, config.OBJS['thorn'], (200, 0, 0), 0.5)
        shot.x = x_pos 
        shot.y = y_pos
        self.shots.append(shot)

    def shot(self, mov, angle, vel, obj, outline_color= (1, 1, 1), size = 1):
        shot = obj.get_copy()
        shot.width = int(shot.width * size)
        shot.x = self.mouth_pos[0]
        shot.y = self.mouth_pos[1] 
        shot.mov = mov
        shot.rot_angle = angle
        shot.vel = vel
        shot.outline_color = outline_color
        return shot

    def shots_update(self, player, dt):
        for i, shot in sorted(enumerate(self.shots), reverse= True):
            shot.update(dt)

            #out of window
            if shot.x < 0 - shot.width or shot.x > config.display.get_width() + config.camera.x + shot.width or shot.y < - shot.height or shot.y > config.display.get_height() + config.camera.y  + shot.height:
                self.shots.pop(i)
            else:
                #collide player
                if player.imuniti_ticks <= 0:
                    if shot.perfect_collide(player):
                        self.shots.pop(i)
                        player.damage()

    def add_lifebar(self, obj):
        self.lifebar = obj

    def get_life_percent(self):
        return self.life / self.lifes[self.actual_life]

    def _get_idle_time(self):
        return randint(self.idle_time_range[0], self.idle_time_range[1])

    def lifebar_update(self):
        self.lifebar.update_liferect(self.get_life_percent())
        if self.get_life_percent() <= 0 and self.actual_life == '1':
            self.actual_life = '2'
            self.life = self.lifes['2']
            self.lifebar.del_liferect()
            self.is_angry = True
        if self.get_life_percent() <= 0 and self.actual_life == '2':
            self.is_dead = True

    def damage_update(self, dt):
        self.damage_ticks -= 1 * dt
        if int(self.damage_ticks) == 0:
            if self.is_angry:
                self.action = 'a_idle'
            else:
                self.action = 'idle'

    def damage(self):
        self.life -= 4
        self.action = 'damage'
        self.damage_ticks = 10
        config.camera.shake([-3, 3], [-3, 3], 10)

        
