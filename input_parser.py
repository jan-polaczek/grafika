from line import Line3D


class InputParser:
    def __init__(self, path):
        self.path = path
        self.objects = []

    def parse(self):
        with open(self.path, 'r') as file:
            self.handle_file(file)
        return self.objects

    def handle_file(self, file):
        for line in file:
            if line[0] == '#':
                continue
            coors = [int(coordinate) for coordinate in line.split()]
            if len(coors) == 0:
                continue
            line_3d = Line3D(coors)
            self.objects.append(line_3d)
