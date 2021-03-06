import pygame as pg
import numpy as np
from settings import size


class Goal(pg.sprite.Sprite):
    'Left and right side goal objects'
    def __init__(self, type: str):
        super(Goal, self).__init__()
        self.offset = (146, 340) # Sprite dimensions
        if type == 'left':
            self.image = pg.image.load('images/goal_L.png')
            self.mask = pg.mask.from_surface(self.image)
            self.position = np.array([0, size[1]/2])
            self.velocity = [0, 1]
        else:
            self.image = pg.image.load('images/goal_R.png')
            self.mask = pg.mask.from_surface(self.image)
            self.position = np.array([size[0] - self.offset[0], size[1]/2 - self.offset[1]])
            self.velocity = [0, -1]
    
    def __str__(self):
        return 'goal'

    def accelerate(self):
        self.position[1] += self.velocity[1]
    
    def boundary_check(self):
        if self.position[1] < 70:
            self.velocity[1] *= -1
            self.position[1] = 70
        elif self.position[1] > size[1] - self.offset[1]:
            self.velocity[1] *= -1
            self.position[1] = size[1] - self.offset[1]
    
    def update_hitbox(self):
        self.rect = pg.Rect(self.position[0], self.position[1], 
                                  self.offset[0], self.offset[1])