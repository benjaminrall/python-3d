import pygame
import random
from personallib.camera import Camera
from plot import *
from graph import *

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
cam = Camera(win, 0, 0, 600)
plot = Plot((0, 0, -2), (0, 0, 0), 10)
graphs = [Vector(6, 3, 3), Vector(5, 3, 3), Vector(8, -6, 2), Vector(-13, 5, -3), Vector(-0.2, -0.4, 0.5), Vector(3, 8, -6), Vector(-17, 34, 13)]
graphs = [Plane((2, 3, -5), (0, 2, -3)), Plane((1, 0, 0), (0, 2, 3)) , Plane((0.2, 1, -0.1), (0, -4, 0))]
graphs = [Plane((1, 1, 1), (-2, -2, -2)), Vector(-5, -5, -5), Vector(2, 5, -3), Vector(7, 3, 8)]

# Variables
running = True
rotating_cube = False
rotations = [False, False, False, False]
keys = {pygame.K_s : 0, pygame.K_d : 1, pygame.K_w : 2, pygame.K_a : 3}
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
                elif event.button == 4:
                    plot.scale = max(plot.scale - 1, 1)
                elif event.button == 5:
                    plot.scale = min(plot.scale + 1, 100)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rotating_cube = False
            elif event.type == pygame.MOUSEMOTION and rotating_cube:
                movement = pygame.mouse.get_rel()
                plot.rotation[0] = min(max(plot.rotation[0] + (movement[1] / FRAMERATE / 5), math.radians(-90)), math.radians(90))
                plot.rotation[1] += movement[0] / FRAMERATE / 5
            elif event.type == pygame.KEYDOWN:
                if event.key in keys:
                    rotations[keys[event.key]] = True
                elif event.key == pygame.K_r:
                    plot.rotation = [0, 0, 0]
            elif event.type == pygame.KEYUP:
                if event.key in keys:
                    rotations[keys[event.key]] = False

        win.fill((25, 25, 25))

        for i in range(4):
            if rotations[i]:
                plot.rotation[i % 2] += {0 : 1, 1 : -1}[i // 2] / FRAMERATE

        plot.calculate_mesh()
        plot.draw(cam, graphs)
        
        pygame.display.update()
        clock.tick(FRAMERATE)