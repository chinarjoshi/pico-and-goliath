# Uses Python's SDL wrapper to interface with hardware.
import pygame
# Used for trignometric functions.
import math
# Initializes SDL.
pygame.init()

# Class responsible for initializing the display surface.
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
    'Hello there'
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
        for i in range(2):
            self.position[i] += self.velocity[i]
            if self.velocity[i] > 0:
                self.velocity[i] -= self.drag
            elif self.velocity[i] < 0:
                self.velocity[i] += self.drag

    def boundary_check(self):
        for i in range(2):
            if self.position[i] < Screen.offset:
                self.velocity[i] *= -.5
                self.position[i] = Screen.offset
            elif self.position[i] > Screen.size[i] - Screen.offset:
                self.velocity[i] *= -.5
                self.position[i] = Screen.size[i] - Screen.offset

    def speed_check(self):
        for i in range(2):
            if self.velocity[i] > 2:
                self.velocity[i] = 2
            if self.velocity[i] < -2:
                self.velocity[i] = -2

    def mouse_click(self, coordinates):
        for i in range(2):
            self.velocity[i] += .005 * coordinates[i]

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Disk.touching(pygame.mouse.get_pos()):
                    pygame.mouse.get_rel()
                    disk_pressed = True
                    print("WORDKS")

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
