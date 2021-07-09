import math

class Camera3D:
    def __init__(self, win, position, rotation, fov, near = 0, far = math.inf, mode = 1):
        self.win = win
        self.winWidth = win.get_width()
        self.winHeight =  win.get_height()
        self.width = self.winWidth / fov
        self.height = self.winHeight / fov
        self.fov = fov
        self.position = position
        self.rotation = rotation
        self.near = near
        self.far = far
        self.mode = mode

    def get_screen_coord(self, coord):
        pass