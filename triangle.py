class Triangle3D:

    def __init__(self, points, color=None):
        self.vertices = points
        self.color = color
        if not color:
            self.color = (255, 0, 0)
        
    def __repr__(self):
        return f'A: {self.vertices[0]} B: {self.vertices[1]} C: {self.vertices[2]} color: {self.color}'


class Triangle2D:
    def __init__(self, vertices, color):
        self.a, self.b, self.c = vertices
        self.color = color
