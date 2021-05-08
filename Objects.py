from imports import *
from TransitionPoint import TransitionPoint

class Player:
    def __init__(self, pos: vec, vel: vec):
        self.vel = vel
        self.body = pygame.Rect(0, 0, 32, 32)
        self.body.center = pos

        self.left_leg = Leg(self.body)
        self.right_leg = Leg(self.body, side="right")
        self.eyes = Eyes(self.body)

        self.is_on_ground = False

    def update(self, dt, tiles):
        # self.body.topleft += self.vel * dt
        self.vel.y += 0.5                           ## GRAVITY
        self.body.x += self.vel.x * dt              ## ADDING VELOCITY TO X
        ## COLLISION ON X
        hits = self.get_hits(tiles)
        for tile in hits:
            if self.vel.x > 0:
                self.body.right = tile.rect.left
                self.vel.x = 0
            elif self.vel.x < 0:
                self.body.left = tile.rect.right
                self.vel.x = 0

        self.body.y += self.vel.y * dt              ## ADDING VELOCITY TO Y
        hits = self.get_hits(tiles)
        ## COLLISION ON Y
        for tile in hits:
            if self.vel.y > 0:
                self.is_on_ground = True
                self.body.bottom = tile.rect.top
                self.vel.y = 0
            elif self.vel.y < 0:
                self.body.top = tile.rect.bottom
                self.vel.y = 0

        ## UPDATING THE BODY PARTS
        self.left_leg.update(self.vel)
        self.right_leg.update(self.vel)
        self.eyes.update(self.vel)

    def get_hits(self, tiles):
        return [tile for tile in tiles if self.body.colliderect(tile.rect)]

    def move(self, keys):                               ## CONTROLS
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = 5 
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -5
        else:
            self.vel.x = 0
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_on_ground:
            self.vel.y = -10
            self.is_on_ground = False

    def draw(self, screen, scroll):                     ## DRAWING ALL THE PARTS
        self.right_leg.draw(screen, scroll)
        pygame.draw.rect(
            screen, 
            (0, 0, 0), 
            [(self.body.x - scroll.x, self.body.y - scroll.y), self.body.size],
            border_radius=self.body.w // 2
        )
        self.eyes.draw(screen, scroll)
        self.left_leg.draw(screen, scroll)


class Triangle:                             ## WE DON"T TALK BOUT HIM HERE
    def __init__(self, pos: vec, vel: vec):
        self.vel = vel
        self.body = pygame.Rect(0, 0, 32, 32)
        self.body.center = pos

        self.left_leg = Leg(self.body)
        self.right_leg = Leg(self.body, side="right")
        self.eyes = Eyes(self.body)

        self.is_on_ground = False

    def update(self, dt, tiles):
        self.body.x += self.vel.x * dt
        hits = self.get_hits(tiles)
        for tile in hits:
            if self.vel.x > 0:
                self.vel.x = -5
                self.body.right = tile.rect.left
                self.vel.x = 0
                if self.is_on_ground:
                    self.is_on_ground = False
            elif self.vel.x < 0:
                self.vel.x = 5
                self.vel.x = 0
                self.body.left = tile.rect.right
                if self.is_on_ground:
                    self.is_on_ground = False

        self.vel.y += 0.5
        self.body.y += self.vel.y * dt
        hits = self.get_hits(tiles)
        for tile in hits:
            if self.vel.y > 0:
                self.is_on_ground = True
                self.body.bottom = tile.rect.top
                self.vel.y = 0
            elif self.vel.y < 0:
                self.is_on_ground = False
                self.body.top = tile.rect.bottom
                self.vel.y = 0

        self.left_leg.update(self.vel)
        self.right_leg.update(self.vel)
        self.eyes.update(self.vel)

    def get_hits(self, tiles):
        return [tile for tile in tiles if self.body.colliderect(tile.rect)]

    def draw(self, screen, scroll):
        self.right_leg.draw(screen, scroll)
        pygame.gfxdraw.filled_trigon(
            screen,
            int(self.body.midtop[0] - scroll.x),
            int(self.body.midtop[1] - scroll.y),
            int(self.body.bottomright[0] - scroll.x),
            int(self.body.bottomright[1] - 2 - scroll.y),
            int(self.body.bottomleft[0] - scroll.x),
            int(self.body.bottomleft[1] - 2 - scroll.y),
            pygame.Color(0, 0, 0),
        )
        self.eyes.draw(screen, scroll)
        self.left_leg.draw(screen, scroll)


class Leg:                  ## LEGS, WHICH YOU USE USUALLY TO WALK
    def __init__(self, obj_rect: pygame.Rect, speed=5, size=14, side="left"):
        self.obj = obj_rect
        self.side = side
        if self.side == "left":
            self.tr_center = TransitionPoint(
                vec(*obj_rect.bottomleft), vec(*obj_rect.bottomright), speed=speed
            )
        elif self.side == "right":
            self.tr_center = TransitionPoint(
                vec(*obj_rect.bottomright), vec(*obj_rect.bottomleft), speed=speed
            )
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = self.tr_center.update()

    def update(self, vel: vec):
        if self.side == "left":
            self.tr_center.p1 = vec(*self.obj.bottomleft)
            self.tr_center.p2 = vec(*self.obj.bottomright)
        elif self.side == "right":
            self.tr_center.p1 = vec(*self.obj.bottomright)
            self.tr_center.p2 = vec(*self.obj.bottomleft)
        if vel.x != 0:
            self.tr_center.state = "moving"
        else:
            self.tr_center.state = "idle"
        self.rect.center = self.tr_center.update()
        # self.rect.centery = self.obj.bottom

    def draw(self, screen, scroll, color=(0, 0, 0)):
        pygame.draw.rect(
            screen,
            color,
            [(self.rect.x - scroll.x, self.rect.y - scroll.y), self.rect.size],
            border_radius=self.rect.w // 2,
        )


class Eyes:                         ## EYES, WHICH YOU USE USUALLY TO SEE
    def __init__(self, obj_rect):
        self.obj = obj_rect
        self.tr_center = TransitionPoint(
            vec(self.obj.midright[0] - 6),
            vec(self.obj.midright[0] - 6),
        )
        self.rect = pygame.Rect(0, 0, 12, 8)
        self.rect.center = self.tr_center.update()
        self.state = "opened"

    def update(self, vel):
        ## MAKING THE STATE VARIABLE READABLE
        if self.rect.h >= 8:
            self.state = "opened"
        elif self.rect.h <= 1:
            self.state = "closed"

        ## IF THE BODY IS JUMPING, THEN CLOSE THE EYES
        if vel.y < 0:
            self.close()
        ## IF BODY IS IN REST OR FALLING DOWN, OPEN EM
        if vel.y >= 0:
            self.open()

        ## FIRST UPDATING THE TRANSITION POINT MAKES IT LAG BEHIND WHICH LOOKS COOL B)
        self.rect.center = self.tr_center.update()

        self.tr_center.p1.y = self.obj.midright[1]
        self.tr_center.p2.y = self.obj.midleft[1]
        if vel.x > 0:
            self.tr_center.p1 = vec(self.obj.midright[0] - 6, self.obj.midright[1])
            self.tr_center.p2 = vec(self.obj.midright[0] - 6, self.obj.midright[1])
        elif vel.x < 0:
            self.tr_center.p1 = vec(self.obj.midleft[0] + 6, self.obj.midleft[1])
            self.tr_center.p2 = vec(self.obj.midleft[0] + 6, self.obj.midleft[1])

    def draw(self, screen, scroll, color=(255, 255, 255)):
        pygame.draw.rect(
            screen,
            color,
            [(self.rect.x - scroll.x, self.rect.y - scroll.y), (self.rect.w//2, self.rect.h)],
            border_radius=self.rect.w // 3,
        )
        pygame.draw.rect(
            screen,
            color,
            [(self.rect.x + self.rect.w//2 + 1 - scroll.x, self.rect.y - scroll.y), (self.rect.w//2, self.rect.h)],
            border_radius=self.rect.w // 3,
        )

    def close(self):                        ## CLOSE THE EYES ;)
        if self.state == "opened":
            self.rect = self.rect.inflate(0, -1)
    
    def open(self):                         ## OPEN EM ;)
        if self.state == "closed":
            self.rect = self.rect.inflate(0, 1)
