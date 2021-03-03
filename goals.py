import pygame


class Goal:
    def __init__(self, image, position, velocity):
        self.image = pygame.image.load(f'images/{image}')
        self.position = position
        self.velocity = velocity
    def accelerate(self):