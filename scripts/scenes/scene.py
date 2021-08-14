from scripts.config import OBJS, reset


class Scene:
    def __init__(self):
        self.loop = True

    def events():
        pass
    def draw():
        pass
    def update():
        pass

    def restart(self):
        self.__init__()
        reset()
        