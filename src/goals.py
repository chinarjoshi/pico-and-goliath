"""
Defines the Goal class to be used as the win state.

This module is to be used with the PicoAndGoliath object to create the win
state of the game

    Typical usage example:

        goal1 = Goal('left')
        if goal_collision(ball, goal1):
            ...

"""
import pygame as pg
import numpy as np
from .settings import size


class Goal(pg.sprite.Sprite):
    """
    Encapulates data for goal objects on either side of screen.

    Defines the goal objects so that the ball can be scored. Contains collision
    detection and boundary check methods. Goal objects constantly move up and
    down to make the game more dynamic.

    Args:
        pg (Sprite): Sprite class defined by pygame.

    """

    def __init__(self, type: str):
        """
        Inits the Goal object with starting values and image.

        Initializes Goal objects with a starting position in the center,
        opposite velocity vectors, and hitbox bitmap calculated from image.
        There are two types of goal, left and right, defined by input to the
        constructor method.

        Args:
            type (str): Defines left or right type goal object.

        """
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
            self.position = np.array([size[0] - self.offset[0],
                                      size[1]/2 - self.offset[1]])
            self.velocity = [0, -1]
    
    def __str__(self):
        """
        Defines string represenation of the Goal object.
        
        Defines the string representation of the object in order to be used
        as a dictionary key.

        Returns:
            A string representation of the Goal object.
            str: 'goal'

        """
        return 'goal'

    def accelerate(self):
        """
        Updates position vector based on velocity vector.
        """
        self.position[1] += self.velocity[1]
    
    def boundary_check(self):
        """
        Checks if the Goal object is out of bounds.

        Checks if the vertical position component offset by the image dimensions
        is out of bounds, if so then flip the sign of the corresponding velocity
        component.

        """
        if self.position[1] < 70:
            self.velocity[1] *= -1
            self.position[1] = 70
        elif self.position[1] > size[1] - self.offset[1]:
            self.velocity[1] *= -1
            self.position[1] = size[1] - self.offset[1]
    
    def update_hitbox(self):
        """
        Updates the image hitbox based on the current position and offset.
        """
        self.rect = pg.Rect(self.position[0], self.position[1], 
                                  self.offset[0], self.offset[1])