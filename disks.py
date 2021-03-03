import pygame

offset = 32
size = (1500, 1000)

class Disk:
    'Parent class for child disks'
    def __init__(self, position):
        self.image = pygame.image.load('images/soccer.png')
        # ** Replace with named tuple here!!!!
        self.position = position
        self.velocity = [0, 0]
        self.acceleration = .05
        self.drag = .001

    def accelerate(self):
        for i in range(2):
            self.position[i] += self.velocity[i]
            if self.velocity[i] > 0:
                self.velocity[i] -= self.drag
            elif self.velocity[i] < 0:
                self.velocity[i] += self.drag

    def speed_check(self):
        for i in range(2):
            if self.velocity[i] > 2:
                self.velocity[i] = 2
            if self.velocity[i] < -2:
                self.velocity[i] = -2


class David(Disk):
    'Player on the left side of the screen'
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load("images/david.png")
        self.acceleration = .06

    def key_down(self, keys):
        if keys[pygame.K_d]:
            self.velocity[0] += self.acceleration

        if keys[pygame.K_a]:
            self.velocity[0] -= self.acceleration

        if keys[pygame.K_w]:
            self.velocity[1] -= self.acceleration
            
        if keys[pygame.K_s]:
            self.velocity[1] += self.acceleration
    
    def boundary_check(self):
        if self.position[0] < offset:
            self.velocity[0] *= -.5
            self.position[0] = offset
        elif self.position[0] > size[0]/2 - offset:
            self.velocity[0] *= -.5
            self.position[0] = size[0]/2 - offset

        if self.position[1] < offset:
            self.velocity[1] *= -.5
            self.position[1] = offset
        elif self.position[1] > size[1] - offset:
            self.velocity[1] *= -.5
            self.position[1] = size[1] - offset
    
    
class Goliath(Disk):
    'Player on the right side of screen'
    def __init__(self, position):
        super().__init__(position)
        self.image = pygame.image.load("images/goliath.png")
        self.acceleration = .02

    def key_down(self, keys):
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += self.acceleration

        if keys[pygame.K_LEFT]:
            self.velocity[0] -= self.acceleration

        if keys[pygame.K_UP]:
            self.velocity[1] -= self.acceleration

        if keys[pygame.K_DOWN]:
            self.velocity[1] += self.acceleration

    def boundary_check(self):
        if self.position[0] < size[0]/2 + offset:
            self.velocity[0] *= -.5
            self.position[0] = size[0]/2 + offset
        elif self.position[0] > size[0] - offset:
            self.velocity[0] *= -.5
            self.position[0] = size[0] - offset

        if self.position[1] < offset:
            self.velocity[1] *= -.5
            self.position[1] = offset
        elif self.position[1] > size[1] - offset:
            self.velocity[1] *= -.5
            self.position[1] = size[1] - offset