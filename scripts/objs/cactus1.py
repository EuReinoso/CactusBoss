from scripts import config
from scripts.pgengine import Obj, CircleParticle
from math import hypot, degrees, atan2, radians, cos, sin
from random import randint, uniform, choice

class Cactus1(Obj):
    def __init__(self, img):
        super().__init__(img)
        self.lifes = {'1' : 100, '2': 100}
        self.actual_life = '1'
        self.life = self.lifes[self.actual_life]
        self.is_dead = False

        self.shots = []
        self.atack_ticks = 0
        self.atack_time = {'1' : 350, '2' : 200, '3' : 300, 'a1' : 350}
        self.atacks_list = ['1', '2', '3']
        self.a_atacks_list = ['a1']
        self.actual_atack = '3'
        self.is_atack = False
        self.is_angry = False

        self.idle_time_range = [200, 350]
        self.idle_time = 120
        self.idle_ticks = 0
        self.shot_ticks = 0

        self.damage_ticks = 0

        self.angle_shot = 0

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
            self.action = 'atack'
            if not self.is_angry:
                self.actual_atack = choice(self.atacks_list)
            else:
                self.actual_atack = choice(self.a_atacks_list)
            self.outline = False
        else:
            if self.damage_ticks <= 0:
                if self.rect.colliderect(player.rect):
                    if player.x > self.x - 13 and player.x < self.x + 13:
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
                    if self.shot_ticks > 15:
                        self.shot_ticks = 0
                        self.atacka1(player.x, player.y)


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
        c = cos(radians(uniform(0, 360)))
        s = sin(radians(uniform(0, 360)))

        while abs(c) < 2 and abs(s) < 2:
            c *= 1.01
            s *= 1.01

        rot_angle  = degrees(atan2(-s, c))
        shot = self.shot([c, s], rot_angle, 1, config.OBJS['thorn'])
        self.shots.append(shot)

    def atack3(self):
        angle = randint(0, 360)
        space = randint(360//7, 360/5)
        for _ in range(int(360/space)):
            c = cos(radians(angle))
            s = sin(radians(angle))

            angle -= space
            rot_angle = degrees(atan2(-s, c))
            shot = self.shot([c, s], rot_angle, 2, config.OBJS['thorn'])
            self.shots.append(shot)

    def atacka1(self, player_x, player_y):
        hyp = hypot((player_x - self.mouth_pos[0]), (player_y - self.mouth_pos[1]))
        mov = [0, 0]
        if hyp != 0:
            mov[0] = (player_x - self.mouth_pos[0]) / hyp
            mov[1] = (player_y - self.mouth_pos[1]) / hyp
        
        rot_angle = degrees(atan2(-mov[1], mov[0]))
        shot = self.shot(mov, rot_angle, 2, config.OBJS['thorn'], (200, 0, 0), 2)
        self.shots.append(shot)

    def shot(self, mov, angle, vel, obj, outline_color= (1, 1, 1), size = 1):
        shot = obj.get_copy()
        shot.width *= size
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
            self.action = 'idle'

    def damage(self):
        self.life -= 3
        self.action = 'damage'
        self.damage_ticks = 10
        config.camera.shake([-3, 3], [-3, 3], 10)

        
