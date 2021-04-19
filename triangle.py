
class Triangle3D:
    def __init__(self, points, color=(255, 0, 0)):
        self.vertices = points
        self.color = color
        
    def __str__(self):
        return str(self.vertices[0]) + '; ' + str(self.vertices[1]) + '; ' + str(self.vertices[2])


class Triangle2D:
    def __init__(self, vertices, color):
        self.a, self.b, self.c = vertices
        self.color = color
