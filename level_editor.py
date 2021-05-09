import pygame
from pygame.math import Vector2 as vec
import os, sys, random, csv
from MapUtility import load_map_by_csv

pygame.init()

display_info = pygame.display.Info()
WW, WH = display_info.current_w//2, display_info.current_h//2
WINDOW = pygame.display.set_mode((WW, WH))

SW, SH = WW, WH
screen = pygame.Surface((SW, SH)).convert()

clock = pygame.time.Clock()

map_file_path = os.path.join("maps", "map.csv")

tiles, map_size = load_map_by_csv(map_file_path)

scroll = vec()
prev_scroll = vec()
scroll_mode = False

class TileBox:
    def __init__(self, tiles):
        self.rect = pygame.Rect(0, 0, 64, SH)
        self.tiles = tiles

    def update(self):
        pass
    
    def draw(self, screen):
        # for tile in tiles:
        #     print(x)

        pygame.draw.rect(screen, (36, 36, 36), self.rect, border_radius=8)

tilebox = TileBox(tiles)

while True:
    dt = clock.tick(60)/1000.0
    screen.fill((136, 136, 136))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                scroll_mode = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                scroll_mode = False
        
    if pygame.mouse.get_pressed(3)[0] and scroll_mode:
        scroll.x = (mx - scroll.x) * -1/2
        scroll.y = (my - scroll.y) * -1/2
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    for tile in tiles:
        tile.draw(screen, scroll)

    tilebox.draw(screen)

    WINDOW.blit(pygame.transform.scale(screen, (WINDOW.get_size())), (0, 0))
    pygame.display.update()

