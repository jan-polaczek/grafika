from point import Point3D


class Line3D:
    def __init__(self, coors):
        self.start = Point3D(coors[0], coors[1], coors[2])
        self.end = Point3D(coors[3], coors[4], coors[5])


class Line2D:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'Start: {self.start} End: {self.end}'
