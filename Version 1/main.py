import pygame
import random
from camera import Camera
from cube import Cube

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 600
FRAMERATE = 240
# ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
#pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("3D Projection")
# pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 0, 0, 128)

cubes = []
for i in range(1):
    for j in range(1):
        cubes.append(Cube(3 * i, 3 * j))

# Variables
running = True
x = 0
y = 0
z = 0
inc = 0.005
rx = True
ry = True
rz = True
zoomingIn = False
zoomingOut = False
directions = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1, pygame.K_UP: 2, pygame.K_DOWN: 3}
panning = [False, False, False, False]
speed = 1

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
                elif event.key == pygame.K_w:
                    zoomingIn = True
                elif event.key == pygame.K_s:
                    zoomingOut = True
                elif event.key in directions:
                    panning[directions[event.key]] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    zoomingIn = False
                elif event.key == pygame.K_s:
                    zoomingOut = False
                elif event.key in directions:
                    panning[directions[event.key]] = False
                    if True not in panning:
                        speed = 1

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
        if zoomingIn:
            cam.zoom += 1
        if zoomingOut:
            cam.zoom = max(1, cam.zoom - 1)
        if panning[0]:
            cam.Pan((speed, 0))
        if panning[1]:
            cam.Pan((-speed, 0))
        if panning[2]:
            cam.Pan((0, speed))
        if panning[3]:
            cam.Pan((0, -speed))
        if True in panning:
            speed += 0.5
        
        pygame.display.update()

        clock.tick(FRAMERATE)