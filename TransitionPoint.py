from imports import *

## THIS IS THE MAIN THING OF THIS WHOLE PROJECT :P
class TransitionPoint:
    def __init__(self, p1: vec, p2: vec, speed=1, loop=True, state="moving"):
        """
        p1: starting point of the transition
        p2: ending point of the transition
        speed=1: is well speed
        loop=True: if set to true, the transition will repeat after completing, else not
        state="moving": "moving" means it will be, well, moving, and "idle" means it will be idle LOL
        """
        self.p1 = p1
        self.p2 = p2
        self.f = 0
        self.speed = speed
        self.loop = loop
        self.state = state

    def update(self):
        if self.state == "moving":
            self.f += self.speed
            if self.loop:
                if self.f >= 100:
                    self.speed *= -1
                elif self.f <= 0:
                    self.speed *= -1
            else:
                if self.f >= 100:
                    self.state = "idle"
        return self.p1.lerp(self.p2, self.f/100)

        