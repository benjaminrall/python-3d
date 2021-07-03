import numpy as np
import math

def remove_dupes(x):
    n = []
    for i in x:
        if (i[0], i[1]) not in n and (i[1], i[0]) not in n:
            n.append(i)
    return np.array(n)

def GetXRotation(t):
    m = np.zeros((3, 3))
    c = math.cos(t)
    s = math.sin(t)
    m[0] = [1, 0, 0]
    m[1] = [0, c, -s]
    m[2] = [0, s, c]
    return m

def GetYRotation(t):
    m = np.zeros((3, 3))
    c = math.cos(t)
    s = math.sin(t)
    m[0] = [c, 0, -s]
    m[1] = [0, 1, 0]
    m[2] = [s, 0, c]
    return m

def GetZRotation(t):
    m = np.zeros((3, 3))
    c = math.cos(t)
    s = math.sin(t)
    m[0] = [c, -s, 0]
    m[1] = [s, c, 0]
    m[2] = [0, 0, 1]
    return m

class Cube:
    def __init__(self, x, y):
        self.position = (x, y)
        self.rotation = (0, 0, 0)
        self.vertices = [[0, 0, 0], [0, 0, 1], 
                         [0, 1, 0], [0, 1, 1],
                         [1, 0, 0], [1, 0, 1], 
                         [1, 1, 0], [1, 1, 1]]
        self.edges = remove_dupes([ [v1, v2] for v1 in self.vertices for v2 in self.vertices if sum( [ abs(i[0] - i[1]) for i in zip(v1, v2) ] ) == 1 ])
        self.rotated_edges = []

    def draw(self, cam):
        for line in self.rotated_edges:
            start = line[0]
            end = line[1]
            cam.draw_line((start[0] + self.position[0], start[1] + self.position[1]), (end[0] + self.position[0], end[1] + self.position[1]), (255, 255, 255))

    def get_rotations(self):
        self.rotated_edges = []
        for edge in self.edges:
            m_start = np.reshape(edge[0], (3, 1))
            m_end = np.reshape(edge[1], (3, 1))
            x_rot = GetXRotation(self.rotation[0])
            y_rot = GetYRotation(self.rotation[1])
            z_rot = GetZRotation(self.rotation[2])
            c_start = np.reshape(np.dot(z_rot, np.dot(y_rot, np.dot(x_rot, m_start))), 3)
            c_end = np.reshape(np.dot(z_rot, np.dot(y_rot, np.dot(x_rot, m_end))), 3)
            self.rotated_edges.append([c_start, c_end])

    def rotate(self, rotation):
        self.rotation = rotation
        self.get_rotations()