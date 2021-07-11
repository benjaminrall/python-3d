import numpy as np
import math
import copy

from numpy.core.fromnumeric import sort
from pygame.version import ver

def dot_product(a, b):
    return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])

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

class Graph:
    def __init__(self) -> None:
        pass

class Vector(Graph):
    def __init__(self, x, y, z):
        self.vertices = [[0, 0, 0], [x, y, z]]
        self.edgeIndices = [[0, 1]]
        self.mesh = []

    def calculate_mesh(self, position, rotation, scale):
        vertices = copy.copy(self.vertices)
        vertexDistances = [[abs(vertex[i]) for i in range(3)] for vertex in vertices]
        for i, vertex in enumerate(vertexDistances):
            if max(vertex) > scale / 2:
                multiplier = (scale / 2) / max(vertex)
                vertices[i] = [ coord * multiplier for coord in vertices[i]]
        vertices = [np.reshape(vertex, (3, 1)) / scale for vertex in vertices]
        m_rotation = rotation_matrix(rotation)
        vertices = [np.reshape(np.dot(m_rotation, vertex), 3) for vertex in vertices]
        vertices = [[vertex[i] + position[i] for i in range(3)] for vertex in vertices]
        vertices = [[vertex[i] * (1 / vertex[2]) for i in range(3)] for vertex in vertices]
        self.mesh = [[vertices[edge[0]], vertices[edge[1]]] for edge in self.edgeIndices]

    def draw(self, cam):
        for edge in self.mesh:
            start = edge[0]
            end = edge[1]
            cam.draw_line((start[0], start[1]),(end[0], end[1]), (255, 0, 255))

class Plane(Graph):
    def __init__(self, normal, point):
        self.normal = normal
        self.point = point
        d = (normal[0] * point[0]) + (normal[1] * point[1]) + (normal[2] * point[2])
        self.coefficients = {"x": self.normal[0], "y": self.normal[1], "z": self.normal[2], "d": -d}
        self.vertices = []
        self.scale = 10
        self.cubeLines = [ [a, b] for a in [[-1, -1, -1], [1, -1, 1], [-1, 1, 1], [1, 1, -1]] for b in [[1, 0, 0], [0, 1, 0], [0, 0, 1]] ]
        self.calculate_scale(self.scale)

    def draw(self, cam):
        if False:
            for edge in self.mesh:
                start = edge[0]
                end = edge[1]
                cam.draw_line((start[0], start[1]),(end[0], end[1]), (255, 0, 0))
        if len(self.mesh) > 2:
            cam.draw_polygon(self.mesh, (255, 0, 0))

    def calculate_mesh(self, position, rotation, scale):
        if scale != self.scale:
            self.calculate_scale(scale)
            self.scale = scale
        vertices = copy.copy(self.vertices)
        if len(vertices) == 0:
            self.mesh = []
            return
        vertices = sorted(vertices)
        startPoint = vertices[0]
        orderedVertices = []
        for vertex in vertices[1:]:
            if vertex[1] > startPoint[1]:
                orderedVertices.append(vertex)
        vertices = sorted(vertices, reverse=True)
        for vertex in vertices:
            if vertex[1] <= startPoint[1]:
                orderedVertices.append(vertex)
        vertices = orderedVertices
        
        vertices = [np.reshape(vertex, (3, 1)) / scale for vertex in vertices]
        m_rotation = rotation_matrix(rotation)
        vertices = [np.reshape(np.dot(m_rotation, vertex), 3) for vertex in vertices]
        vertices = [[vertex[i] + position[i] for i in range(3)] for vertex in vertices]
        vertices = [[vertex[i] * (1 / vertex[2]) for i in range(3)] for vertex in vertices]
        edgeIndices = [[i, j] for i in range(len(vertices)) for j in range(len(vertices))]
        self.mesh = [[vertices[edge[0]], vertices[edge[1]]] for edge in edgeIndices]

        self.mesh = vertices

    def calculate_scale(self, scale):

        # INTERSECTION
        size = scale / 2
        points = []
        lines = [ [ [ coord * size for coord in line[0] ], line[1] ] for line in self.cubeLines ]
        for line in lines:
            diff = dot_product(line[1], self.normal)
            if diff != 0:
                d = (dot_product([ self.point[i] - line[0][i] for i in range(3) ], self.normal)) / diff
                l = [ d * line[1][i] for i in range(3) ]
                point = [ line[0][i] + l[i] for i in range(3) ]
                points.append(point)
        correctedPoints = []
        for point in points:
            inBounds = True
            for coord in point:
                if not -size <= coord <= size:
                    inBounds = False
            if inBounds:
                correctedPoints.append(point)
        self.vertices = correctedPoints

        if False:
            # GRID SCRAPING
            step = 50
            r = step + 1
            halfstep = step / 2
            jumps = scale / step
            points = []
            for x in range(0, r, 1):
                x = (x - halfstep) * jumps
                for z in range(0, r, 1):
                    z = (z - halfstep) * jumps
                    y = -(self.coefficients["x"] * x) - (self.coefficients["z"] * z) - self.coefficients["d"]
                    point = [x, y, z]
                    if point not in points:
                        points.append(point)
                for y in range(0, r, 1):
                    y = (y - halfstep) * jumps
                    z = -(self.coefficients["x"] * x) - (self.coefficients["y"] * y) - self.coefficients["d"]
                    point = [x, y, z]
                    if point not in points:
                        points.append(point)
                    for z in range(0, r, 1):
                        z = (z - halfstep) * jumps
                        x = -(self.coefficients["y"] * y) - (self.coefficients["z"] * z) - self.coefficients["d"]
                        point = [x, y, z]
                        if point not in points:
                            points.append(point)
            checkedPoints = []
            for point in points:
                if (point[0] * self.coefficients["x"]) + (point[1] * self.coefficients["y"]) + (point[2] * self.coefficients["z"]) + self.coefficients["d"] == 0:
                    checkedPoints.append(point)
            bounds = [-halfstep * jumps, halfstep * jumps]
            adjustedPoints = []
            for point in checkedPoints:
                inBounds = True
                for coord in point:
                    if not (bounds[0] <= coord <= bounds[1]):
                        inBounds = False
                if inBounds:
                    if bounds[0] in point or bounds[1] in point:
                        adjustedPoints.append(point)
            self.vertices = adjustedPoints
        if False:
            # EDGE JUMPING
            points = []
            size = scale / 2
            vertices = [[i, j, k] for k in range(2) for j in range(2) for i in range(2)]
            edgeIndicesTemp = [[start, end] for start in range(len(vertices)) for end in range(len(vertices)) if sum( [ abs(i[0] - i[1]) for i in zip(vertices[start], vertices[end]) ] ) == 1]
            edgeIndices = []
            for edge in edgeIndicesTemp:
                if [edge[0], edge[1]] not in edgeIndices and [edge[1], edge[0]] not in edgeIndices:
                    edgeIndices.append(edge)
            for i in range(len(vertices)):
                for j in range(len(vertices[i])):
                    if vertices[i][j] == 0:
                        vertices[i][j] = -size
                    else:
                        vertices[i][j] = size
            step = 10000
            accuracy = 0
            increment = scale / step
            for i in edgeIndices:
                edge = [vertices[i[0]], vertices[i[1]]]
                if edge[0][0] != edge[1][0]:
                    y = edge[0][1]
                    z = edge[0][2]
                    for x in range(step + 1):
                        x = (x *  increment) - (size / 2) 
                        if round((x * self.coefficients["x"]) + (y * self.coefficients["y"]) + (z * self.coefficients["z"]) + self.coefficients["d"], accuracy) == 0:
                            points.append([x, y, z])
                            break
                elif edge[0][1] != edge[1][1]:
                    x = edge[0][0]
                    z = edge[0][2]
                    for y in range(step + 1):
                        y = (y *  increment) - (size / 2) 
                        if round((x * self.coefficients["x"]) + (y * self.coefficients["y"]) + (z * self.coefficients["z"]) + self.coefficients["d"], accuracy) == 0:
                            points.append([x, y, z])
                            break
                elif edge[0][2] != edge[1][2]:
                    x = edge[0][0]
                    y = edge[0][1]
                    for z in range(step + 1):
                        z = (z *  increment) - (size / 2) 
                        if round((x * self.coefficients["x"]) + (y * self.coefficients["y"]) + (z * self.coefficients["z"]) + self.coefficients["d"], accuracy) == 0:
                            points.append([x, y, z])
                            break
            self.vertices = points
