
class Triangle3D:
    def __init__(self, points, color=(255, 0, 0)):
        self.vertices = points
        self.color = color
        self.projection = None
        
    def __str__(self):
        return str(self.vertices[0]) + '; ' + str(self.vertices[1]) + '; ' + str(self.vertices[2])


class Triangle2D:
    def __init__(self, vertices, color):
        self.a, self.b, self.c = vertices
        self.color = color

    def get_min_max_x(self):
        min_x = min([self.a[0], self.b[0], self.c[0]])
        max_x = max([self.a[0], self.b[0], self.c[0]])
        return min_x, max_x

    def get_min_max_y(self):
        min_y = min([self.a[1], self.b[1], self.c[1]])
        max_y = max([self.a[1], self.b[1], self.c[1]])
        return min_y, max_y