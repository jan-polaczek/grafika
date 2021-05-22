from sphere import Sphere
from point import Point3D


class SphereParser:
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
            center, radius, color = self.parse_line(line)
            sphere = Sphere(center, radius, color)
            self.objects.append(sphere)

    @staticmethod
    def parse_line(line: str):
        arr = [int(x) for x in line.replace(';', '').split()]
        center = Point3D(arr[0], arr[1], arr[2])
        radius = arr[3]
        color = arr[4], arr[5], arr[6]
        return center, radius, color
