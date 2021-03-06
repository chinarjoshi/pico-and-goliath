'Given position and velocity of two objects, return new velocity of either object'
import pygame
from disks import Ball, Disk
from goals import Goal
from music import Sounds


class CollisionEngine:
    'Detects mask collisions between disks and between the ball and goal'
    def __init__(self):
        self.sounds = Sounds()

    def goal_collision(self, player: Disk, goal: Goal):
        'Collision engine between Disk subclass and goal'
        return pygame.sprite.collide_mask(player, goal)

    def disk_collision(self, player: Disk, ball: Ball, volume):
        'Collision engine within Disk subclasses'
        if pygame.sprite.collide_mask(player, ball):
            self.sounds.set_volume(volume)
            self.sounds.impact_effects[player.__str__()].play()
            for i in range(2):
                net_force = (player.velocity[i] + ball.velocity[i])
                player.velocity[i] = net_force * (player.mass / (player.mass + ball.mass))
                ball.velocity[i] = net_force * (ball.mass / (ball.mass + player.mass))