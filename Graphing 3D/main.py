import pygame
import random
from personallib.camera import Camera
from plot import *

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 800
FRAMERATE = 60
# ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
#pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("3D Projection")
# pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 400)

cubes = []
cubes.append(Cube((0, 0, -1.5), (129, 0, 29), 1))

# Variables
running = True
rotating_cube = False
rotations = [False, False, False]
keys = {pygame.K_a : 0, pygame.K_s : 1, pygame.K_d : 2}
# Main Loop
if __name__ == '__main__':
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rotating_cube = True
                    pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rotating_cube = False
            elif event.type == pygame.MOUSEMOTION and rotating_cube:
                movement = pygame.mouse.get_rel()
                cube.rotation[0] += movement[1] / FRAMERATE / 5
                cube.rotation[1] += movement[0] / FRAMERATE / 5

        win.fill((0, 0, 0))

        for i in range(3):
            if rotations[i]:
                cube.rotation[i] += 1 / FRAMERATE

        for cube in cubes:
            cube.calculate_mesh()
            cube.draw(cam)
        
        pygame.display.update()
        clock.tick(FRAMERATE)