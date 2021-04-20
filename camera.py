from point import Point3D
from line import Line2D
from triangle import Triangle2D, Triangle3D
from rectangle import Rectangle
from functools import cmp_to_key
import numpy as np
import math


PAN_STEP = 2
ZOOM_STEP = 0.1
MIN_F = 0.1
ROTATION_STEP = 0.03
MOUSE_ROTATION_SLOWDOWN = 0.03


def convert_point_to_array(point):
    return np.array([
        [point.x],
        [point.y],
        [point.z],
        [1]
    ])


def calculate_distance_3d(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5


class Camera:
    def __init__(self, triangles, lines=None):
        self.position = Point3D(0, 0, 0)
        self.lines = lines
        self.triangles = triangles
        self.f = 2
        self.rotation = Point3D(0, 0, 0)

    def render(self):
        lines_2d = []
        if self.lines:
            for line in self.lines:
                start_2d = self.translate_point(line.start)
                end_2d = self.translate_point(line.end)
                line_2d = Line2D(start_2d, end_2d)
                lines_2d.append(line_2d)

        self.sort_triangles()
        triangles_2d = []
        for t in self.triangles:
            triangles_2d.append(t.projection)
        return lines_2d, triangles_2d

    def get_matrix(self):
        matrix_with_rotation = self.get_rotation_matrix()

        position_vector = np.array([
            [self.position.x],
            [self.position.y],
            [self.position.z]
        ])

        matrix = np.hstack((matrix_with_rotation, position_vector))
        matrix = np.vstack((matrix, np.array([0, 0, 0, 1])))
        matrix = np.linalg.inv(matrix)
        return matrix

    def get_rotation_matrix(self):
        z_rotation = np.array([
            [math.cos(self.rotation.z), -math.sin(self.rotation.z), 0],
            [math.sin(self.rotation.z), math.cos(self.rotation.z), 0],
            [0, 0, 1]
        ])

        y_rotation = np.array([
            [math.cos(self.rotation.y), 0, math.sin(self.rotation.y)],
            [0, 1, 0],
            [-math.sin(self.rotation.y), 0, math.cos(self.rotation.y)]
        ])
        x_rotation = np.array([
            [1, 0, 0],
            [0, math.cos(self.rotation.x), -math.sin(self.rotation.x)],
            [0, math.sin(self.rotation.x), math.cos(self.rotation.x)]
        ])

        rotation_matrix = z_rotation.dot(y_rotation.dot(x_rotation))
        return rotation_matrix

    def translate_point(self, point):
        point_arr = convert_point_to_array(point)
        point_2d_arr = self.get_matrix().dot(point_arr)
        if point_2d_arr[2, 0] <= 0.1:
            return None
        point_2d_arr = point_2d_arr * (self.f / point_2d_arr[2, 0])
        return point_2d_arr[0, 0] * 400, point_2d_arr[1, 0] * 400

    def sort_triangles(self):
        for t in self.triangles:
            vertices = [self.translate_point(vertex) for vertex in t.vertices]
            t.projection = Triangle2D(vertices, t.color)
            # added because of null pointer problems when to close to an object
            for v in vertices:
                if not v:
                    t.projection = None
            
        # count = len(self.triangles)
        # t = self.triangles
        # for i in range(count):
        #     for j in range(i+1, count):
        #         res = self.compare_triangles(t[i], t[j])
        #         if res == 1:
        #             tmp = t[i]
        #             t[i] = t[j]
        #             t[j] = tmp 
                
        min_max_compare = cmp_to_key(self.compare_triangles)
        self.triangles.sort(key=min_max_compare)

    def compare_triangles(self, t1, t2):
        # if not t1.projection or not t2.projection:
        #     return 0

        # r1 = Rectangle(t1.projection)
        # r2 = Rectangle(t2.projection)

        # if not r1.does_overlap(r2):
        #     return 0

        dist_t1_max = max([calculate_distance_3d(vertex, self.position) for vertex in t1.vertices])
        dist_t1_min = min([calculate_distance_3d(vertex, self.position) for vertex in t1.vertices])
        dist_t2_max = max([calculate_distance_3d(vertex, self.position) for vertex in t2.vertices])
        dist_t2_min = min([calculate_distance_3d(vertex, self.position) for vertex in t2.vertices])

        if dist_t1_min > dist_t2_max:
            return -1
        elif dist_t2_min > dist_t1_max:
            return 1
        elif dist_t1_max > dist_t2_min and dist_t2_max > dist_t1_max:
            return 1
        elif dist_t2_max > dist_t1_min and dist_t1_max > dist_t2_max:
            return -1
        elif dist_t1_min >= dist_t2_min and dist_t1_max <= dist_t2_max:
            return -1
        elif dist_t2_min >= dist_t1_min and dist_t2_max <= dist_t1_max:
            return 1

        return 0


    def pan_right(self):
        self.pan_x(1)

    def pan_left(self):
        self.pan_x(-1)

    def pan_up(self):
        self.pan_y(-1)

    def pan_down(self):
        self.pan_y(1)

    def pan_forward(self):
        self.pan_z(1)

    def pan_backward(self):
        self.pan_z(-1)

    def rotate_clockwise(self):
        self.rotate_z(1)

    def rotate_counter_clockwise(self):
        self.rotate_z(-1)

    def pan_x(self, direction):
        self.position.x += PAN_STEP * direction * math.cos(self.rotation.y) * math.cos(self.rotation.z)
        self.position.y += PAN_STEP * direction * math.sin(self.rotation.z)
        self.position.z += - PAN_STEP * direction * math.sin(self.rotation.y)

    def pan_y(self, direction):
        self.position.x += - PAN_STEP * direction * math.sin(self.rotation.z)
        self.position.y += PAN_STEP * direction * math.cos(self.rotation.z) * math.cos(self.rotation.x)
        self.position.z += PAN_STEP * direction * math.sin(self.rotation.x)

    def pan_z(self, direction):
        self.position.x += PAN_STEP * direction * math.sin(self.rotation.y)
        self.position.y += - PAN_STEP * direction * math.sin(self.rotation.x)
        self.position.z += PAN_STEP * direction * math.cos(self.rotation.y) * math.cos(self.rotation.x)

    def rotate_y(self, direction):
        self.rotation.y += ROTATION_STEP * direction

    def rotate_x(self, direction):
        self.rotation.x += ROTATION_STEP * direction

    def rotate_z(self, direction):
        self.rotation.z += ROTATION_STEP * direction

    def zoom(self, direction):
        self.f = max(self.f + ZOOM_STEP * direction, MIN_F)

    def rotate(self, amount):
        self.rotate_y(amount[0] * MOUSE_ROTATION_SLOWDOWN)
        self.rotate_x(-amount[1] * MOUSE_ROTATION_SLOWDOWN)

    def zoom_in(self):
        self.zoom(1)
    
    def zoom_out(self):
        self.zoom(-1)
