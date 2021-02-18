import pygame
import math
# initialize pygame
pygame.init()

class Screen:
    def __init__(self):
        self.size = (1000, 1000)
        self.offset = 32
        self.window = pygame.display.set_mode((self.size[0], self.size[1]))

        # Ball icon from https://www.flaticon.com/authors/freepik.
        self.icon = pygame.image.load("soccer-ball-variant.png").convert()
        pygame.display.set_caption("Shuffleboard++")
        pygame.display.set_icon(self.icon)
    
    def update(self, Img, x, y):
        self.window.blit(Img, (x - self.offset, y - self.offset))

# Overhaul this to polar coordinate system when finished.
class Disk:
    def __init__(self):
        self.Img = pygame.image.load("soccer-ball-variant.png")
        self.position = [500, 800]
        self.velocity = [0, 0]
        self.acceleration = .0025
        self.drag = .0005

    def key_down(self, keys):
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += self.acceleration

        if keys[pygame.K_LEFT]:
            self.velocity[0] -= self.acceleration

        if keys[pygame.K_UP]:
            self.velocity[1] -= self.acceleration

        if keys[pygame.K_DOWN]:
            self.velocity[1] += self.acceleration
    
    def accelerate(self):
        for position, velocity in zip(self.position, self.velocity):
            position += velocity
            if velocity > 0:
                velocity -= self.drag
            elif velocity < 0:
                velocity += self.drag

    def boundary_check(self):
        for position, velocity in zip(self.position, self.velocity):
            if position < Screen.offset:
                velocity *= -.5
                position = Screen.offset
            elif position > Screen.size[i] - Screen.offset:
                velocity *= -.5
                position = Screen.size[i] - Screen.offset
    
    def speed_check(self):
        for velocity in self.velocity:
            if velocity > 2:
                velocity = 2
            if velocity < -2:
                velocity = -2

    def mouse_click(self, coordinates):
        for velocity, coordinate in zip(self.velocity, coordinates):
            velocity += .005 * coordinate

    def touching(self, point):
        distance = ((self.position[0] - point[0])**2 + (self.position[1] - point[1])**2)**(1/2)
        return distance < Screen.offset


# Game Loop
def game_flow(running = True):
    disk_pressed = False
    while running:
        # Iterates through all of the events of pygame.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and Disk.touching(pygame.mouse.get_pos()):
                pygame.mouse.get_rel()
                disk_pressed = True

            if event.type == pygame.MOUSEBUTTONUP and disk_pressed:
                Disk.mouse_click(pygame.mouse.get_rel())
                disk_pressed = False
        
        # Calculations for the Disk position and velocity.
        Disk.key_down(pygame.key.get_pressed())
        Disk.accelerate()
        Disk.boundary_check()
        # Disk.speed_check()
        


        # Fills the new frame with the background, redraws disk, and updates screen.
        Screen.window.fill((255, 255, 255))
        Screen.update(Disk.Img, Disk.position[0], Disk.position[1])
        pygame.display.update()
        
Screen = Screen()
Disk = Disk()

if __name__ == "__main__" and pygame.display.get_init():
    game_flow()