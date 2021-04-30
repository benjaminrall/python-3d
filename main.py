import pygame
import random
from camera import Camera
from cube import Cube

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 800
FRAMERATE = 512
# ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("3D Projection")
# pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 200)

cubes= [Cube(0, 0)]

# Variables
running = True
x = 0
y = 0
z = 0
inc = 0.0025
rx = True
ry = True
rz = True

# Main Loop
if __name__ == '__main__':
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    rx = not rx
                elif event.key == pygame.K_y:
                    ry = not ry
                elif event.key == pygame.K_z:
                    rz = not rz
                    
        win.fill((0, 0, 0))
        
        for cube in cubes:
            cube.rotate((x, y, z))
            cube.draw(cam)

        if rx:
            x = (x + inc) % 360
        if ry:
            y = (y + inc) % 360
        if rz:
            z = (z + inc) % 360
        
        pygame.display.update()

        clock.tick(FRAMERATE)