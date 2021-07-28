from scripts.pgengine import Obj

class Shot(Obj):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.angle = 0
        self.vel = 1
        self.mov = [0, 0]
    
    def update(self, dt):
        self.x += self.mov[0] * self.vel * dt
        self.y += self.mov[1] * self.vel * dt
        
    
    
