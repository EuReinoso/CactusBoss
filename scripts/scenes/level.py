from scripts.scenes.scene import Scene
from scripts.config import OBJS, MAPS_PATH, reset
from scripts.pgengine import load_map

class Level(Scene):
    def __init__(self, level_name):
        super().__init__()
        self.level_name = level_name
        self.map = load_map(MAPS_PATH[level_name])
        self.tiles = self.load_tiles(self.map)

    def load_tiles(self, map_data):
        tiles = []
        y = 0
        for row in map_data:
            x = 0
            for tile in row:
                is_tile = False
                if tile == '1':
                    new_tile = OBJS['tile_center'].get_copy()
                    is_tile = True
                    
                if tile == '2':
                    new_tile = OBJS['tile_ground'].get_copy()
                    is_tile = True

                if tile == '3':
                    new_tile = OBJS['tile_left'].get_copy()
                    is_tile = True

                if tile == '4':
                    new_tile = OBJS['tile_right'].get_copy()
                    is_tile = True

                if tile == '5':
                    new_tile = OBJS['tile_f_center'].get_copy()
                    is_tile = True

                if tile == '6':
                    new_tile = OBJS['tile_f_left'].get_copy()
                    is_tile = True
                
                if tile == '7':
                    new_tile = OBJS['tile_f_right'].get_copy()
                    is_tile = True

                if is_tile:
                    new_tile.x = x * new_tile.width
                    new_tile.y = y * new_tile.height
                    tiles.append(new_tile)

                x += 1
            y += 1
        return tiles

    def restart(self):
        reset()
        self.__init__(self.level_name)