"""
Defines the 4 main disk classes as the main interaction of the game.

This module is to be used with the PicoAndGoliath object to create the main
agents of the game. This module defines the Disk parent class along with
the Ball, Pico, and Goliath classes.

    Typical usage:

        pico = Pico()
        goliath = Goliath()

        while Running:
            for agent in pico, goliath:
                agent.accelerate()
                agent.boundary_check()
                agent.key_down()

"""
import pygame as pg
from .settings import size


class Disk(pg.sprite.Sprite):
    """
    Template class for all disk-like objects.

    Defines certain shared methods that set-up the phsyics engine for the
    game. All disk-like objects acclerate, have a max speed, and are contained
    within the boundaries of the game.

    Args:
        pg (Sprite): Inherits from the sprite class defined by pygame

    """

    def __init__(self, position: list):
        """
        Inits Disk with starting position, velocity, and default max speed.

        Args:
            position (list): The starting position of the disk given by the game loop.

        """
        super(Disk, self).__init__()
        self.initial_position = tuple(position)
        self.position = position
        self.velocity = [0, 0]
        self.max_speed = 2

    def accelerate(self):
        """
        Updates the Disk's position and velocity vectors.

        Uses the disks horizontal and vertical velocity components to update the
        disk's position, and uses the drag coeffient to decrease the velocity.

        """
        for i in range(2):
            self.position[i] += self.velocity[i]
            if self.velocity[i] > 0:
                self.velocity[i] -= self.drag
            elif self.velocity[i] < 0:
                self.velocity[i] += self.drag

    def speed_check(self):
        """
        Keeps Disk's speed within its maximum speed.

        Checks if either component of the velocity vector is greater than
        the maximum speed. If so, assigns that component to the maximum speed.

        """
        for i in range(2):
            if self.velocity[i] > self.max_speed:
                self.velocity[i] = self.max_speed
            if self.velocity[i] < -self.max_speed:
                self.velocity[i] = -self.max_speed

    def boundary_check(self):
        """
        Keeps the Disk's position within the boundaries of the game.

        Checks to see if either position component is outside the boundaries
        while offset by the image's pixel dimensions. If so, reverses the sign
        of the corresponding speed component and slightly decreases speed.

        """
        if self.position[1] < 0:
            self.velocity[1] *= -.8
            self.position[1] = 0
        elif self.position[1] > size[1] - self.offset:
            self.velocity[1] *= -.8
            self.position[1] = size[1] - self.offset
    
    def update_hitbox(self):
        """
        Updates the rect attribute based on the Disk's current position.
        """
        self.rect = pg.Rect(self.position[0], self.position[1], 
                                  self.offset, self.offset)
    

class Ball(Disk):
    """
    Encapulates the ball's attributes and assigns customized methods.

    The ball inherits from the Disk class which in turn inherits from pygame's
    Sprite class. The image and mask are loaded from the images directory.

    Args:
        Disk (Sprite): Template class for all disk-like objects. 

    """

    def __init__(self, position: list):
        """
        Inits ball with image, mask, and physics-engine constants.

        Expands upon the Disk classes initialization with its corresponding
        image and mask from the images directory. Defines the mass, maximum
        speed, and drag coefficient.

        Args:
            position (list): The starting position given by the game loop.

        """
        self.offset = 64
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load('images/ball.png')
        self.mask = pg.mask.from_surface(self.image)
        self.max_speed = 20
        self.mass = 1
        self.drag = .002

    def boundary_check(self):
        """
        Keeps the ball's position within the boundaries of the game.

        Checks to see if either position component is outside the boundaries
        similarly to the Disk class, but instead uses a reflection coefficient
        of .8 to keep the game faster paced.

        """
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
    """
    Encapulates Pico's attributes and assigns customized methods.

    Pico is the smaller playable character on the left bound of the screen.
    He is faster but lighter than Goliath, and he interacts with the other
    disk-like objects of the game through the defined physics engine.

    Args:
        Disk (Sprite): Template class for all disk-like objects.

    """

    def __init__(self, position: list):
        """
        Inits Pico with image, mask, and physics-engine constants.

        Expands upon the Disk classes initialization with its corresponding
        image and mask from the images directory. Defines the mass, maximum
        speed, and drag coefficient.

        Args:
            position (list): The starting position given by the game loop.

        """
        self.offset = 64
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load("images/david.png")
        self.mask = pg.mask.from_surface(self.image)
        self.acceleration = .12
        self.drag = .02
        self.mass = .5
        self.max_speed = 7
    
    def __str__(self):
        """
        String representation of Pico.

        Used for accessing dictionary key using only the Pico object.

        Returns:
            A string representation of Pico to be used as a dict key.

            str: 'pico'

        """
        return 'pico'

    def key_down(self, keys: list):
        """
        Checks if WASD is pressed in order to accelerate Pico.

        Checks if w, a, s, or d returns True in a list of all currectly pressed
        keys. If it does, then change the corresponding velocity component
        in either the positive or negative direction.

        Args:
            keys (list): Contains boolean values of the currently pressed keys.

        """
        if keys[pg.K_d]:
            self.velocity[0] += self.acceleration
        if keys[pg.K_a]:
            self.velocity[0] -= self.acceleration
        if keys[pg.K_w]:
            self.velocity[1] -= self.acceleration
        if keys[pg.K_s]:
            self.velocity[1] += self.acceleration
    
    def boundary_check(self):
        """
        Checks if either position component is outside of bounds.

        If any position component is outside of the boundaries of the game,
        then the corresponding velocity component is reversed and halved in
        order to control Pico's speed.

        """
        super().boundary_check()
        if self.position[0] < 0:
            self.velocity[0] *= -.5
            self.position[0] = 0
        elif self.position[0] > size[0]/2 - self.offset:
            self.velocity[0] *= -.5
            self.position[0] = size[0]/2 - self.offset
    

class Goliath(Disk):
    """
    Encapulates Goliath's attributes and assigns customized methods.

    Goliath is the larger playable character on the right bound of the screen.
    He is more powerful but heftier than Pico, and he interacts with the other
    disk-like objects with the defined physics engine.

    Args:
        Disk (Sprite): Template class for all disk-like objects.

    """

    def __init__(self, position: list):
        """
        Inits Goliath with image, mask, and physics constants.

        Expands upon the disk class and makes Goliath bulkier than Pico with
        a larger image and mask, slower acceleration and max speed, and lower
        drag coefficient.

        Args:
            position (list): Initial position provided by the game loop.

        """
        self.offset = 128
        super().__init__([position[0] - self.offset/2, position[1] - self.offset/2])
        self.image = pg.image.load("images/goliath.png")
        self.mask = pg.mask.from_surface(self.image)
        self.acceleration = .06
        self.drag = .008
        self.mass = .25
        self.max_speed = 6.5
    
    def __str__(self):
        """
        String representation of Goliath.

        Used for accessing Goliath's corresponding dictionary entry using only
        a Goliath object.

        Returns:
            A string representation of Goliath to be used as a dict key.

            str: 'goliath'

        """
        return 'goliath'

    def key_down(self, keys: any):
        """
        Checks if WASD is pressed in order to accelerate Goliath.

        Checks if w, a, s, or d returns True in a list of all currectly pressed
        keys. If it does, then change the corresponding velocity component
        in either the positive or negative direction.

        Args:
            keys (list): Contains boolean values of the currently pressed keys.

        """
        if keys[pg.K_RIGHT]:
            self.velocity[0] += self.acceleration
        if keys[pg.K_LEFT]:
            self.velocity[0] -= self.acceleration
        if keys[pg.K_UP]:
            self.velocity[1] -= self.acceleration
        if keys[pg.K_DOWN]:
            self.velocity[1] += self.acceleration

    def boundary_check(self):
        """
        Checks if either position component is outside of bounds.

        If any position component is outside of the boundaries of the game,
        then the corresponding velocity component is reversed and halved in
        order to control Pico's speed.

        """
        super().boundary_check()
        if self.position[0] < size[0]/2:
            self.velocity[0] *= -.8
            self.position[0] = size[0]/2
        elif self.position[0] > size[0] - self.offset:
            self.velocity[0] *= -.8
            self.position[0] = size[0] - self.offset