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
        reset()
        self.__init__()
        
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