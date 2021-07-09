import pygame
import random
from personallib.camera import Camera
from cube import *

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 600
FRAMERATE = 60
# ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
#pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("3D Projection")
# pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()
screen = pygame.Surface((500, 500))

# Objects
cam = Camera(screen, 0, 0, 200)
cam.set_bounds((-20, -20), (20, 20))

cubes = []
cubes.append(PerspectiveCube(0, 0.4, 0, 2))
cubes.append(PerspectiveCube(2, 0, 0, 1))

# Variables
running = True
x = 0
y = 0
z = 0
forward = False
backward = False
left = False
right = False
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
                    cam.zoom_out(10, limit=1)
                elif event.key == pygame.K_y:
                    cam.zoom_in(10)
                elif event.key == pygame.K_z:
                    cam.zoom_in(1)
                elif event.key == pygame.K_w:
                    forward = True
                elif event.key == pygame.K_s:
                    backward = True
                elif event.key == pygame.K_a:
                    left = True
                elif event.key == pygame.K_d:
                    right = True
                elif event.key in directions:
                    panning[directions[event.key]] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    forward = False
                elif event.key == pygame.K_s:
                    backward = False
                elif event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_d:
                    right = False
                elif event.key in directions:
                    panning[directions[event.key]] = False
                    if True not in panning:
                        speed = 1

        win.fill((0, 0, 0))
        screen.fill((0, 0, 0))
        
        for cube in cubes:  
            if forward:
                cube.cameraPos[2] += 2/FRAMERATE
                #cam.zoom_in(1, 112)
            if backward:
                cube.cameraPos[2] -= 2/FRAMERATE
                #cam.zoom_out(1, 16)
            if left:
                cube.cameraPos[0] -= 2/FRAMERATE
            if right:
                cube.cameraPos[0] += 2/FRAMERATE
            if panning[0]:
                cube.cameraRot[1] = (cube.cameraRot[1] - 2/FRAMERATE)
                # cam.pan((speed, 0))
            if panning[1]:
                cube.cameraRot[1] = (cube.cameraRot[1] + 2/FRAMERATE)
                # cam.pan((-speed, 0))
            if panning[2]:
                cube.cameraRot[0] = (cube.cameraRot[0] - 2/FRAMERATE)
                # cam.pan((0, speed))
            if panning[3]:
                cube.cameraRot[0] = (cube.cameraRot[0] + 2/FRAMERATE)
                # cam.pan((0, -speed))
        if True in panning:
            speed += 0.5
        cam.enforce_bounds()

        for cube in cubes:
            cube.project()

        centres = [cube.get_centre() for cube in cubes]
        magnitudes = [(math.sqrt(sum([centre[i] ** 2 for i in range(3)])), j) for j, centre in enumerate(centres)]
        orderCubes = [magnitude[1] for magnitude in sorted(magnitudes, reverse=True)]
        for i in orderCubes: 
            cubes[i].draw(cam)
        
        #cam.draw_line((cam.x - (cam.width / 2), (cam.y - (cam.height / 2))), (cam.x + (cam.width / 2), (cam.y + (cam.height / 2))), (255, 255, 255))
        #cam.draw_rect((cam.x - 0.1, cam.y - 0.1, 0.2, 0.2), (255, 255, 255))
        pygame.draw.rect(win, (255, 255, 255), (149, 49, 502, 502))
        win.blit(screen, ((WIN_WIDTH - 500) // 2, (WIN_HEIGHT - 500) // 2))

        pygame.display.update()
        clock.tick(FRAMERATE)