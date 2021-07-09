import numpy as np
import math

def x_rotation(theta):
    matrix = np.zeros((3, 3))
    c = math.cos(theta)
    s = math.sin(theta)
    matrix[0] = [1, 0, 0]
    matrix[1] = [0, c, -s]
    matrix[2] = [0, s, c]
    return matrix

def y_rotation(theta):
    matrix = np.zeros((3, 3))
    c = math.cos(theta)
    s = math.sin(theta)
    matrix[0] = [c, 0, -s]
    matrix[1] = [0, 1, 0]
    matrix[2] = [s, 0, c]
    return matrix

def z_rotation(theta):
    matrix = np.zeros((3, 3))
    c = math.cos(theta)
    s = math.sin(theta)
    matrix[0] = [c, -s, 0]
    matrix[1] = [s, c, 0]
    matrix[2] = [0, 0, 1]
    return matrix

def rotation_matrix(rotation):
    matrix = z_rotation(rotation[2])
    matrix = np.dot(y_rotation(rotation[1]), matrix)
    matrix = np.dot(x_rotation(rotation[0]), matrix)
    return matrix

class Cube:
    def __init__(self, position, rotation, size):
        self.position = position
        self.rotation = [math.radians(rotation[i]) for i in range(len(rotation))]
        self.size = size
        self.vertices = []
        self.edgeIndices = []
        self.mesh = []
        self.calculate_mesh()

    def calculate_mesh(self):
        self.edgeIndices = []
        self.vertices = [[i, j, k] for k in range(2) for j in range(2) for i in range(2)]
        edgeIndices = [[start, end] for start in range(len(self.vertices)) for end in range(len(self.vertices)) if sum( [ abs(i[0] - i[1]) for i in zip(self.vertices[start], self.vertices[end]) ] ) == 1]
        for edge in edgeIndices:
            if [edge[0], edge[1]] not in self.edgeIndices and [edge[1], edge[0]] not in self.edgeIndices:
                self.edgeIndices.append(edge)
        self.vertices = [np.reshape([(vertex[i] - 0.5) * self.size for i in range(3)], (3, 1)) for vertex in self.vertices]
        rotationMatrix = rotation_matrix(self.rotation)
        self.vertices = [np.reshape(np.dot(rotationMatrix, vertex), 3) for vertex in self.vertices]
        self.vertices = [[vertex[i] + self.position[i] for i in range(3)] for vertex in self.vertices]
        self.mesh = [[self.vertices[edge[0]], self.vertices[edge[1]]] for edge in self.edgeIndices]

    def get_mesh(self):
        return self.mesh