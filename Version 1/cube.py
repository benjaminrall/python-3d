import math

def remove_dupes(x):
    n = []
    for i in x:
        if (i[0], i[1]) not in n and (i[1], i[0]) not in n:
            n.append(i)
    return n

def GetXRotation(t):
    m = Matrix(3, 3)
    c = math.cos(t)
    s = math.sin(t)
    m.SetRow(0, [1, 0, 0])
    m.SetRow(1, [0, c, -s])
    m.SetRow(2, [0, s, c])
    return m

def GetYRotation(t):
    m = Matrix(3, 3)
    c = math.cos(t)
    s = math.sin(t)
    m.SetRow(0, [c, 0, -s])
    m.SetRow(1, [0, 1, 0])
    m.SetRow(2, [s, 0, c])
    return m


def GetZRotation(t):
    m = Matrix(3, 3)
    c = math.cos(t)
    s = math.sin(t)
    m.SetRow(0, [c, -s, 0])
    m.SetRow(1, [s, c, 0])
    m.SetRow(2, [0, 0, 1])
    return m


def GetMatrix(coord):
    m = Matrix(3, 1)
    for i in range(3):
        m.SetRow(i, [coord[i]])
    return m

def GetCoord(m):
    coord = []
    for row in m.matrix:
        coord.append(row[0])
    coord = (coord[0], coord[1], coord[2])
    return coord

class Cube:
    def __init__(self, x, y):
        self.position = (x, y)
        self.rotation = (0, 0, 0)
        self.vertices = [(0, 0, 0), (0, 0, 1), 
                         (0, 1, 0), (0, 1, 1),
                         (1, 0, 0), (1, 0, 1), 
                         (1, 1, 0), (1, 1, 1)]
        self.edges = remove_dupes([ (v1, v2) for v1 in self.vertices for v2 in self.vertices if sum( [ abs(i[0] - i[1]) for i in zip(v1, v2) ] ) == 1 ])
        self.rotated_edges = []
        self.get_rotations()

    def draw(self, cam):
        for line in self.rotated_edges:
            start = line[0][0:2]
            end = line[1][0:2]
            cam.DrawLine((start[0] + self.position[0], start[1] + self.position[1]), (end[0] + self.position[0], end[1] + self.position[1]), (255, 255, 255))

    def get_rotations(self):
        self.rotated_edges = []
        for edge in self.edges:
            m_start = GetMatrix(edge[0])
            m_end = GetMatrix(edge[1])
            x_start = Matrix.Multiply(GetXRotation(self.rotation[0]), m_start)
            x_end = Matrix.Multiply(GetXRotation(self.rotation[0]), m_end)
            y_start = Matrix.Multiply(GetYRotation(self.rotation[1]), x_start)
            y_end = Matrix.Multiply(GetYRotation(self.rotation[1]), x_end)
            z_start = Matrix.Multiply(GetZRotation(self.rotation[2]), y_start)
            z_end = Matrix.Multiply(GetZRotation(self.rotation[2]), y_end)
            c_start = GetCoord(z_start)
            c_end = GetCoord(z_end)
            self.rotated_edges.append((c_start, c_end))            
        
    def rotate(self, rotation):
        self.rotation = rotation
        self.get_rotations()

class Matrix:
    def __init__(self, r, c):
        self.matrix = []
        self.columns = []
        for i in range(r):
            row = []
            for j in range(c):
                row.append(0)
            self.matrix.append(row)
        self.dimensions = (r, c)
        self.CalculateColumns()

    def SetRow(self, i, v):
        self.matrix[i] = v
        self.CalculateColumns()

    def CalculateColumns(self):
        self.columns = [ list(i) for i in zip(*self.matrix) ]
    
    @staticmethod 
    def Multiply(m1, m2):
        if m1.dimensions[1] != m2.dimensions[0]:
            return 0
        result = Matrix(m1.dimensions[0], m2.dimensions[1])
        for row in range(m1.dimensions[0]):
            newRow = []
            for col in range(m2.dimensions[1]):
                newRow.append(sum([ i[0] * i[1] for i in zip(m1.matrix[row], m2.columns[col]) ]))
            result.SetRow(row, newRow)
        return result