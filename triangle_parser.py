from triangle import Triangle3D
from point import Point3D


class TriangleParser:

    def __init__(self, path):
        self.path = path
        self.objects = []

    def parse(self):
        with open(self.path, 'r') as file:
            self.handle_file(file)
        return self.objects

    def handle_file(self, file_):
        current_line = 0
        all_lines = file_.readlines()
        while current_line < len(all_lines):
            if all_lines[current_line][0] == '#' or all_lines[current_line] == '\n':
                current_line += 1
                continue
            current_line = self.read_object_data(current_line, all_lines)

        return self.objects

    def read_object_data(self, line_idx, lines):
        num_triangle = int(lines[line_idx])
        start = line_idx + 1
        end = start + num_triangle
        current_objects = []

        for line in lines[start:end]:
            vertices = line.split(';')
            new_vertices = []
            for v in vertices:
                vertex = [float(coordinate) for coordinate in v.split()]
                new_vertices.append(Point3D(vertex[0], vertex[1], vertex[2]))

            current_objects.append(Triangle3D(new_vertices))

        color = tuple(int(value) for value in lines[end].split())
        
        for triangle in current_objects:
            triangle.color = color

        self.objects.extend(current_objects)

        return end + 1
