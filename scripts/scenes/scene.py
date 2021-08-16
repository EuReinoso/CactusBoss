from scripts.config import OBJS, reset
from scripts import scenes

class Scene:
    def __init__(self):
        self.next = self
        self.loop = True

    def events(self, events, pressed_keys):
        pass
    def draw(self, display):
        pass
    def update(self, dt):
        pass

    def change_scene(self, new_scene):
        if new_scene == 'restartmenu':
            self.next = scenes.RestartMenu()

        if new_scene == 'level1':
            self.next = scenes.Level1(new_scene)

        if new_scene == 'winmenu':
            self.next = scenes.WinMenu()

    def restart(self):
        self.__init__()
        reset()
        