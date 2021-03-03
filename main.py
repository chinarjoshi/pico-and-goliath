# Uses Python's SDL wrapper to interface with hardware.
import pygame

from sys import exit
from disks import David, Goliath, Disk
from goals import Goal1, Goal2
# David v Goliath
FPS = 144
fpsClock = pygame.time.Clock()

# Initializes SDL.
pygame.init()

# Class responsible for initializing the display surface.
offset = 32
size = (1500, 1000)
window = pygame.display.set_mode(size)

# Ball icon from https://www.flaticon.com/authors/freepik.
icon = pygame.image.load("images/soccer.png").convert()
background = pygame.image.load('images/fields.png')

pygame.display.set_caption("Shuffleboard++")
pygame.display.set_icon(icon)

player1 = David([size[0]/4, size[1]/2])
player2 = Goliath([3*size[0]/4, size[1]/2])
ball = Disk([750, 500])

# Game Loop
def game_flow(running = True):
    disk_pressed = False
    while running:
        # Iterates through all of the events of pygame.
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and player1.touching(pygame.mouse.get_pos()):
                pygame.mouse.get_rel()
                disk_pressed = True

            if event.type == pygame.MOUSEBUTTONUP and disk_pressed:
                player1.mouse_click(pygame.mouse.get_rel())
                disk_pressed = False

        update_player([player1, player2])
        update_window(window, [player1, player2, ball])

        # Fills the new frame with the background, redraws disk, and updates screen.
        pygame.display.update()
        fpsClock.tick(FPS)

def update_player(players):
    for player in players:
        player.key_down(pygame.key.get_pressed())
        player.accelerate()
        player.boundary_check()

def update_window(window, objects):
    window.fill((255, 255, 255))
    for object in objects:
        window.blit(object.image, (object.position[0] - offset, object.position[1] - offset))


if __name__ == "__main__" and pygame.display.get_init():
    game_flow()