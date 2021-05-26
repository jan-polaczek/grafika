from sphere import Sphere
from light_source import LightSource
from point import Point3D


class SphereParser:
    def __init__(self, path):
        self.path = path
        self.spheres = []
        self.light_source = None
        self.current_object = None

    def parse(self):
        with open(self.path, 'r') as file:
            self.handle_file(file)
        return self.spheres, self.light_source

    def handle_file(self, file):
        line = file.readline()
        while line != 'end':
            self.handle_line(line, file)
            line = file.readline()

    def handle_line(self, line, file):
        if len(line.strip()) == 0 or line[0] == '#':
            return
        if 'Sphere' in line:
            self.handle_sphere(file)
        if 'Light' in line:
            self.handle_light_source(file)

    def handle_sphere(self, file):
        line = file.readline()
        attrs = dict()
        while 'end' not in line:
            if len(line.strip()) == 0 or line[0] == '#':
                return
            self.handle_sphere_line(line, attrs)
            line = file.readline()
        sphere = Sphere(**attrs)
        print(attrs)
        self.spheres.append(sphere)

    def handle_light_source(self, file):
        line = file.readline()
        attrs = dict()
        while 'end' not in line:
            if len(line.strip()) == 0 or line[0] == '#':
                return
            self.handle_light_source_line(line, attrs)
            line = file.readline()
        light_source = LightSource(**attrs)
        self.light_source = light_source

    @staticmethod
    def handle_sphere_line(line, attrs):
        line_arr = line.split()
        if 'center' in line_arr[0]:
            attrs['center'] = Point3D(int(line_arr[1]), int(line_arr[2]), int(line_arr[3]))
        elif 'radius' in line_arr[0]:
            attrs['radius'] = int(line_arr[1])
        elif 'specular' in line_arr[0]:
            attrs['k_s'] = tuple([int(x) for x in line_arr[1:]])
        elif 'diffuse' in line_arr[0]:
            attrs['k_d'] = tuple([int(x) for x in line_arr[1:]])
        elif 'ambient' in line_arr[0]:
            attrs['k_a'] = tuple([int(x) for x in line_arr[1:]])
        elif 'alpha' in line_arr[0]:
            attrs['alpha'] = float(line_arr[1])

    @staticmethod
    def handle_light_source_line(line, attrs):
        line_arr = line.split()
        if 'center' in line_arr[0]:
            attrs['center'] = Point3D(int(line_arr[1]), int(line_arr[2]), int(line_arr[3]))
        elif 'specular' in line_arr[0]:
            attrs['i_s'] = tuple([int(x) for x in line_arr[1:]])
        elif 'diffuse' in line_arr[0]:
            attrs['i_d'] = tuple([int(x) for x in line_arr[1:]])
        elif 'ambient' in line_arr[0]:
            attrs['i_a'] = tuple([int(x) for x in line_arr[1:]])

