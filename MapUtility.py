from imports import *
import csv

## COLOR KEYS 
map_colorkeys = {
    "GRASS": {
        "TOP": [(0, 252, 0, 255), 1],
        "TOPRIGHT": [(0, 224, 0, 255), 2],
        "RIGHT": [(0, 196, 0, 255), 3],
        "BOTTOMRIGHT": [(0, 168, 0, 255), 4],
        "BOTTOM": [(0, 140, 0, 255), 5],
        "BOTTOMLEFT": [(0, 112, 0, 255), 6],
        "LEFT": [(0, 84, 0, 255), 7],
        "TOPLEFT": [(0, 56, 0, 255), 8],
        "MID": [(0, 28, 0, 255), 9]
    }
}

"""
list = [
    [img, pos], 
    [img, pos],
    [img, pos],
    [img, pos],
    [img, pos]
]
"""
tile_names = []
for i in map_colorkeys.keys():
    inner_dict = map_colorkeys[i]
    for j in inner_dict.keys():
        tile_names.append(i + " " + j)

def load_tile(name):
    return pygame.image.load(os.path.join("images", "tiles", name+".png")).convert_alpha()

## QUIET PROUD OF THIS SYSTEM ACTUALLY ;)
def load_map_by_img(path: str, tile_size=32):
    map_img = pygame.image.load(path).convert_alpha()
    tiles = []
    for x in range(map_img.get_width()):
        for y in range(map_img.get_height()):
            for tile_name in tile_names:
                if map_img.get_at((x, y)) == map_colorkeys[tile_name.split(" ")[0]][tile_name.split(" ")[1]][0]:
                    tiles.append(Tile(load_tile(tile_name), (x*tile_size, y*tile_size)))
    return tiles

def load_map_by_csv(path: str, tile_size=32):
    tiles = []
    # if os.path.exists(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        x, y = 0, 0
        for row in reader:
            x = 0
            y += 1
            for cell in row:
                x += 1
                for tile_name in tile_names:
                    if int(cell) == map_colorkeys[tile_name.split(" ")[0]][tile_name.split(" ")[1]][1]:
                        tiles.append(Tile(load_tile(tile_name), (x*tile_size, y*tile_size)))

    return tiles, vec(x, y)



## SMALL TILE CLASS
class Tile:
    def __init__(self, img, pos):
        self.image = img
        self.pos = vec(pos)
        self.rect = self.image.get_rect(topleft=self.pos)
        # self.image.set_alpha(150)

    def draw(self, screen: pygame.Surface, scroll: vec):
        screen.blit(self.image, (self.rect.x - scroll.x, self.rect.y - scroll.y))
        # pygame.draw.rect(screen, (0, 0, 0), [self.rect.topleft-scroll, self.rect.size], border_radius=16)
