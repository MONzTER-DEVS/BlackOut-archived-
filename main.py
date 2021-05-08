from imports import *
from Objects import Player, Triangle

pygame.init()

WW, WH = 640, 480
window = pygame.display.set_mode((WW, WH))

SW, SH = 320, 240
display = pygame.Surface((SW, SH))
# display = pygame.image.load(os.path.join("images", "back.png")).convert()
clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption("NONAME_PLATFORMER")
from MapUtility import load_map_by_img

## SCENES
def main():
    # initializing main game
    back = pygame.image.load(os.path.join("images", "back.png")).convert()

    player = Player(vec(SW//2, SH//2), vec(0, 0))
    tri = Triangle(vec(100, SH//2), vec(5, 0))

    level = load_map_by_img(os.path.join("maps", "testmap.png"))

    scroll = vec()

    last_time = time.time()

    while True:
        clock.tick(fps)
        dt = time.time() - last_time
        dt *= fps
        last_time = time.time()
        display.fill((255, 255, 255))
        
        scroll.x += (player.body.centerx - scroll.x - SW / 2) // 10
        scroll.y += (player.body.centery - scroll.y - SH/2) // 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        ## UPDATING STUF
        player.update(dt, level)
        player.move(keys)

        tri.update(dt, level)

        ## DRAWING
        display.blit(back, (0, 0))
        tri.draw(display, scroll)
        player.draw(display, scroll)
        for tile in level:
            tile.draw(display, scroll)
        window.blit(pygame.transform.scale(display, (window.get_width(), window.get_height())), (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
