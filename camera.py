import pygame

class Camera:
    
    def __init__(self, win, x, y, zoom):
        self.zoom = zoom
        self.win = win
        self.win_width = win.get_width()
        self.win_height =  win.get_height()
        self.width = self.win_width / zoom
        self.height = self.win_height / zoom
        self.x = x
        self.y = y

    def DrawRect(self, rect, colour):
        if self.RectInBounds(rect):
            pygame.draw.rect(self.win, colour, self.GetScreenRect(rect))

    def RectInBounds(self, rect):
        return (rect[0] <= self.x + (self.width / 2)) and (rect[0] + rect[2] >= self.x - (self.width / 2)) and (rect[1] + rect[3] >= self.y - (self.height / 2)) and (rect[1] <= self.y + (self.height / 2))

    def GetScreenRect(self, rect):
        w = rect[2] * self.zoom
        h = rect[3] * self.zoom
        x = (-self.x * self.zoom) + ((rect[0] + (self.width / 2)) * self.zoom)
        y = (-self.y * self.zoom) + ((rect[1] + (self.height / 2)) * self.zoom)
        return (x, y, w, h)

    def GetScreenCoord(self, coord):
        x = (-self.x * self.zoom) + ((coord[0] + (self.width / 2)) * self.zoom)
        y = (-self.y * self.zoom) + ((coord[1] + (self.height / 2)) * self.zoom)
        return (x, y)

    def DrawLine(self, start, end, colour):
        pygame.draw.line(self.win, colour, self.GetScreenCoord(start), self.GetScreenCoord(end))

    def ZoomOut(self):
        self.zoom = max(self.zoom / 2, 1)
        self.width = self.win_width / self.zoom
        self.height = self.win_height / self.zoom
    
    def ZoomIn(self):
        self.zoom = min(self.zoom * 2, 1024)
        self.width = self.win_width / self.zoom
        self.height = self.win_height / self.zoom
    
    def Pan(self, pos):
        self.x -= pos[0] / self.zoom
        self.y -= pos[1] / self.zoom