import pygame
import random
from personallib.camera import Camera
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
screen = pygame.Surface((400, 400))

# Objects
cam = Camera(screen, 0, 0, 64)
cam.set_bounds((-20, -20), (20, 20))

cubes = [Cube(0, 0)]
for i in range(20):
    cubes.append(Cube(random.randint(-5, 6) * 3, random.randint(-5, 6) * 3))

# Variables
running = True
x = 0
y = 0
z = 0
inc = 0.01
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
        screen.fill((0, 0, 0))
        
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
            cam.zoom_in(1, 112)
        if zoomingOut:
            cam.zoom_out(1, 16)
        if panning[0]:
            cam.pan((speed, 0))
        if panning[1]:
            cam.pan((-speed, 0))
        if panning[2]:
            cam.pan((0, speed))
        if panning[3]:
            cam.pan((0, -speed))
        if True in panning:
            speed += 0.5
        cam.enforce_bounds()
        
        #cam.draw_line((cam.x - (cam.width / 2), (cam.y - (cam.height / 2))), (cam.x + (cam.width / 2), (cam.y + (cam.height / 2))), (255, 255, 255))
        #cam.draw_rect((cam.x - 0.1, cam.y - 0.1, 0.2, 0.2), (255, 255, 255))
        pygame.draw.rect(win, (255, 255, 255), (199, 99, 402, 402))
        win.blit(screen, ((WIN_WIDTH - 400) // 2, (WIN_HEIGHT - 400) // 2))

        pygame.display.update()

        clock.tick(FRAMERATE)