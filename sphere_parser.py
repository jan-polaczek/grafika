from sphere import Sphere
from light_source import LightSource
from point import Point3D


class SphereParser:
    def __init__(self, path):
        self.path = path
        self.spheres = []
        self.light_source = None

    def parse(self):
        with open(self.path, 'r') as file:
            self.handle_file(file)
        return self.spheres, self.light_source

    def handle_file(self, file):
        for line in file:
            if line[0] == '#' or line == '\n':
                continue
            self.parse_line(line)

    def parse_line(self, line: str):
        arr = [int(x) for x in line.replace(';', '').split()]
        center = Point3D(arr[0], arr[1], arr[2])
        if len(arr) == 7:
            radius = arr[3]
            color = arr[4], arr[5], arr[6]
            self.spheres.append(Sphere(center, radius, color))
        else:
            i_a = arr[3], arr[4], arr[5]
            i_d = arr[6], arr[7], arr[8],
            i_s = arr[9], arr[10], arr[11]
            self.light_source = LightSource(center, i_a, i_d, i_s)

