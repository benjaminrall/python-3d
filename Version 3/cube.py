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

class OrthographicCube:
    def __init__(self, x, y):
        self.position = (x, y)
        self.rotation = [0, 0, 0]
        self.vertices = [[0, 0, 0], [0, 0, 1], 
                         [0, 1, 0], [0, 1, 1],
                         [1, 0, 0], [1, 0, 1], 
                         [1, 1, 0], [1, 1, 1]]
        self.vertices = [[vertex[i] - 0.5 for i in range(3)] for vertex in self.vertices]
        self.edges = remove_dupes([ [v1, v2] for v1 in self.vertices for v2 in self.vertices if sum( [ abs(i[0] - i[1]) for i in zip(v1, v2) ] ) == 1 ])
        self.rotated_edges = []

    def draw(self, cam):
        for line in self.rotated_edges:
            start = line[0]
            end = line[1]
            cam.draw_line((start[0] + self.position[0], start[1] + self.position[1]), (end[0] + self.position[0], end[1] + self.position[1]), (255, 255, 255))

    def update_rotations(self):
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

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.update_rotations()

    def rotate(self, axis, degrees):
        self.rotation[axis] += degrees
        self.update_rotations()

class PerspectiveCube:
    def __init__(self, x, y, z, size=1):
        self.position = [x, y, z]
        self.rotation = [0, 0, 0]
        self.vertices = [[0, 0, 0], [0, 0, 1], 
                         [0, 1, 0], [0, 1, 1],
                         [1, 0, 0], [1, 0, 1], 
                         [1, 1, 0], [1, 1, 1]]
        self.vertices = [[vertex[i] - 0.5 for i in range(3)] for vertex in self.vertices]
        self.edgeIndexes = remove_dupes([[start, end] for start in range(len(self.vertices)) for end in range(len(self.vertices)) if sum( [ abs(i[0] - i[1]) for i in zip(self.vertices[start], self.vertices[end]) ] ) == 1 ])
        self.vertices.append([0, 0, 0])
        self.vertices = [[(vertex[i] * size) + self.position[i] for i in range(3)] for vertex in self.vertices]    
        self.projectedVertices = []    
        self.projectedEdges = []
        self.projectedFaces = []
        self.relPos = [0, 0, 1]
        self.cameraPos = [0, 0, -2]
        self.cameraRot = [0, 0, 0]
        self.faces =   [[0, 2, 6, 4], [4, 5, 7, 6], [5, 1, 3, 7], [1, 3, 2, 0], [2, 6, 7, 3], [1, 5, 4, 0]]
        self.faceOrder = []
        self.project()

    def draw(self, cam):
        for edge in self.projectedEdges:
            break
            start = edge[0]
            end = edge[1]
            cam.draw_line((start[0], start[1]),(end[0], end[1]), (255, 255, 255))
        colours = [(0, 255, 0), (255, 0, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 0, 255)]
        for i in self.faceOrder:
            face = self.projectedFaces[i]
            cam.draw_polygon(face, colours[i])

    def project(self):
        adjustedVertices = [np.reshape([vertex[i] - self.cameraPos[i] for i in range(3)], (3, 1)) for vertex in self.vertices]
        projectedVertices = []
        for vertex in adjustedVertices:
            vertex = np.dot(GetXRotation(self.cameraRot[0]), vertex)
            vertex = np.dot(GetYRotation(self.cameraRot[1]), vertex)
            vertex = np.reshape(vertex, 3)
            x = ((self.relPos[2]/vertex[2]) * vertex[0]) + self.relPos[0]
            y = ((self.relPos[2]/vertex[2]) * vertex[1]) + self.relPos[1]
            projectedVertices.append([x, y, vertex[2]])
        self.projectedVertices = projectedVertices
        nearCulling = 0.1

        self.projectedEdges = [[projectedVertices[edge[0]], projectedVertices[edge[1]]] for edge in self.edgeIndexes if projectedVertices[edge[0]][2] > nearCulling and projectedVertices[edge[1]][2] > nearCulling]
        self.projectedFaces = [[projectedVertices[face[0]], projectedVertices[face[1]], projectedVertices[face[2]], projectedVertices[face[3]]] for face in self.faces if projectedVertices[face[0]][2] > nearCulling and projectedVertices[face[1]][2] > 0 and projectedVertices[face[2]][2] > nearCulling and projectedVertices[face[3]][2] > 0]
        unorderedCentres = [ [ [sum([face[j][i] for j in range(4)]) for i in range(3)][k] / 4 for k in range(3) ] for face in self.projectedFaces ]
        magnitudes = [(math.sqrt(sum([centre[i] ** 2 for i in range(3)])), j) for j, centre in enumerate(unorderedCentres)]
        orderedMagnitudes = sorted(magnitudes, reverse=True)
        self.faceOrder = [magnitude[1] for magnitude in orderedMagnitudes]
    
    def get_centre(self):
        return self.projectedVertices[-1]