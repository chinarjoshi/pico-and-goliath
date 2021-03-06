import pygame as pg
from settings import size


class Disk(pg.sprite.Sprite):
    'Parent class for disk types'
    def __init__(self, position: list):
        super(Disk, self).__init__()
        self.initial_position = tuple(position)
        self.position = position
        self.velocity = [0, 0]
        self.max_speed = 2

    def accelerate(self):
        for i in range(2):
            self.position[i] += self.velocity[i]
            if self.velocity[i] > 0:
                self.velocity[i] -= self.drag
            elif self.velocity[i] < 0:
                self.velocity[i] += self.drag

    def speed_check(self):
        for i in range(2):
            if self.velocity[i] > self.max_speed:
                self.velocity[i] = self.max_speed
            if self.velocity[i] < -self.max_speed:
                self.velocity[i] = -self.max_speed

    def boundary_check(self):
        if self.position[1] < 0:
            self.velocity[1] *= -.8
            self.position[1] = 0
        elif self.position[1] > size[1] - self.offset:
            self.velocity[1] *= -.8
            self.position[1] = size[1] - self.offset
    
    def update_hitbox(self):
        self.rect = pg.Rect(self.position[0], self.position[1], 
                                  self.offset, self.offset)
    

class Ball(Disk):
    'Soccer ball class'
    def __init__(self, position: list):
        self.offset = 64
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load('images/ball.png')
        self.mask = pg.mask.from_surface(self.image)
        self.max_speed = 20
        self.mass = 1
        self.drag = .002

    def boundary_check(self):
        if self.position[0] < 0:
            self.velocity[0] *= -.8
            self.position[0] = 0
        elif self.position[0] > size[0] - self.offset:
            self.velocity[0] *= -.8
            self.position[0] = size[0] - self.offset
        if self.position[1] < 0:
            self.velocity[1] *= -.8
            self.position[1] = 0
        elif self.position[1] > size[1] - self.offset:
            self.velocity[1] *= -.8
            self.position[1] = size[1] - self.offset
        

class Pico(Disk):
    'Player on the left side of the screen'
    def __init__(self, position: list):
        self.offset = 64
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load("images/david.png")
        self.mask = pg.mask.from_surface(self.image)
        self.acceleration = .12
        self.drag = .02
        self.mass = .5
        self.max_speed = 7
    
    def __str__(self):
        return 'pico'

    def key_down(self, keys):
        if keys[pg.K_d]:
            self.velocity[0] += self.acceleration
        if keys[pg.K_a]:
            self.velocity[0] -= self.acceleration
        if keys[pg.K_w]:
            self.velocity[1] -= self.acceleration
        if keys[pg.K_s]:
            self.velocity[1] += self.acceleration
    
    def boundary_check(self):
        super().boundary_check()
        if self.position[0] < 0:
            self.velocity[0] *= -.5
            self.position[0] = 0
        elif self.position[0] > size[0]/2 - self.offset:
            self.velocity[0] *= -.5
            self.position[0] = size[0]/2 - self.offset
    

class Goliath(Disk):
    'Player on the right side of screen'
    def __init__(self, position: list):
        self.offset = 128
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load("images/goliath.png")
        self.mask = pg.mask.from_surface(self.image)
        self.acceleration = .06
        self.drag = .003
        self.mass = .25
        self.max_speed = 6.5
    
    def __str__(self):
        return 'goliath'

    def key_down(self, keys):
        if keys[pg.K_RIGHT]:
            self.velocity[0] += self.acceleration
        if keys[pg.K_LEFT]:
            self.velocity[0] -= self.acceleration
        if keys[pg.K_UP]:
            self.velocity[1] -= self.acceleration
        if keys[pg.K_DOWN]:
            self.velocity[1] += self.acceleration

    def boundary_check(self):
        super().boundary_check()
        if self.position[0] < size[0]/2:
            self.velocity[0] *= -.8
            self.position[0] = size[0]/2
        elif self.position[0] > size[0] - self.offset:
            self.velocity[0] *= -.8
            self.position[0] = size[0] - self.offset