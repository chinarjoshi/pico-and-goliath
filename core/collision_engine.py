"""
Defines the collision engine to be used by Disk and Goal objects.

This module is to be used with the PicoAndGoliath object in order to detect
collision between the various agents.

    Typical usage:

        collision_engine = CollisionEngine()
        ...
        collision_engine.goal_collision(ball, goal1)

"""
import pygame as pg
from .disks import Ball, Disk
from .goals import Goal
from .music import Sounds


class CollisionEngine:
    """
    Detects mask collisions between disks and between the ball and goal.

    Contains methods for detecting collision between the images for the ball
    and goal.

    Returns:
        pg: Sprite collision bitmap to be used for default boolean value.

    """

    def __init__(self):
        """
        Inits the Sounds object to be used to play collision effects.
        """
        self.sounds = Sounds()

    def goal_collision(self, player: Disk, goal: Goal):
        """
        Collision engine between Disk subclass and goal.

        Checks if either Pico or Goliath is currectly intersecting with the
        goal object using mask collision provided by pygame.

        Args:
            player (Disk): Either Pico or Goliath object, polymorphism is used
                as they both inherit from Disk.
            goal (Goal): Goal object to be used for intersection.

        Returns:
            pg: Sprite collision bitmap to be used for default boolean value.

        """
        return pg.sprite.collide_mask(player, goal)

    def disk_collision(self, player: Disk, ball: Ball, volume: int):
        """
        Collision engine within Disk subclasses.

        Checks if either Pico or Goliath is currently intersecting  with the
        Ball object. If so, recalculates their velocity vectors using a sum
        algoritm. In addition, plays the corresponding collision sound effect.

        Args:
            player (Disk): Either Pico or Goliath object.
            ball (Ball): Ball object used for intersection detection.
            volume (int): Volume at which the collision sound effect should
                play.

        """
        if pg.sprite.collide_mask(player, ball):
            self.sounds.set_volume(volume)
            self.sounds.impact_effects[player.__str__()].play()
            for i in range(2):
                net_force = (player.velocity[i] + ball.velocity[i])
                player.velocity[i] = net_force * (player.mass / (player.mass + ball.mass))
                ball.velocity[i] = net_force * (ball.mass / (ball.mass + player.mass))