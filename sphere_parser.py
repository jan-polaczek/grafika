from sphere import Sphere
from light_source import LightSource
from point import Point3D


class SphereParser:
    def __init__(self, path):
        self.path = path
        self.spheres = []
        self.light_sources = []

    def parse(self):
        with open(self.path, 'r') as file:
            self.handle_file(file)
        return self.spheres, self.light_sources

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
            color = arr[3], arr[4], arr[5]
            self.light_sources.append(LightSource(center, color))

