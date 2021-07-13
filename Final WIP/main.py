import pygame
import random
from camera import Camera3D
from cube import Cube

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

# Objects
cam = Camera3D(win, [0, 0, -2], [0, 0, 0], 60)

cube = Cube([0, 0, 0], [0, 0, 45], 2)

# Variables
running = True

# Main Loop
if __name__ == '__main__' and False:
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
                elif event.key == pygame.K_a:
                    left = True
                elif event.key == pygame.K_d:
                    right = True
                elif event.key in directions:
                    panning[directions[event.key]] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    zoomingIn = False
                elif event.key == pygame.K_s:
                    zoomingOut = False
                elif event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_d:
                    right = False
                elif event.key in directions:
                    panning[directions[event.key]] = False
                    if True not in panning:
                        speed = 1

        win.fill((0, 0, 0))
        
        for cube in cubes:
            if rx:
                cube.rotate(0, inc)
            if ry:
                cube.rotate(1, inc)
            if rz:
                cube.rotate(2, inc)
            cube.draw(cam)
        for cube in cubes:  
            if zoomingIn:
                cube.cameraPos[2] += 2/FRAMERATE
                #cam.zoom_in(1, 112)
            if zoomingOut:
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

        for cube in cubes:
            cube.project()
        
        #cam.draw_line((cam.x - (cam.width / 2), (cam.y - (cam.height / 2))), (cam.x + (cam.width / 2), (cam.y + (cam.height / 2))), (255, 255, 255))
        #cam.draw_rect((cam.x - 0.1, cam.y - 0.1, 0.2, 0.2), (255, 255, 255))

        pygame.display.update()

        clock.tick(FRAMERATE)