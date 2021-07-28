from scripts.pgengine import Obj

class LifeBar(Obj):
    def __init__(self, img):
        super().__init__(img)
        self.liferects = []

    def update_liferect(self, life_percent):
        if len(self.liferects) > 0:
            if int(life_percent * self.width) > 0:
                self.liferects[-1].width = int(life_percent * self.width)

    def add_liferect(self, obj):
        obj.x = self.x
        obj.y = self.y
        obj.height = self.height
        obj.width = self.width
        self.liferects.append(obj)

    def del_liferect(self):
        self.liferects.pop()

    def draw_liferects(self, display):
        for liferect in self.liferects:
            liferect.draw(display)
