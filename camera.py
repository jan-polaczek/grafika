from point import Point3D
from ray_caster import RayCaster
from functools import cmp_to_key
from phong import Phong
import numpy as np
import math


PAN_STEP = 10
ZOOM_STEP = 0.1
MIN_F = 0.1
ROTATION_STEP = 0.03
MOUSE_ROTATION_SLOWDOWN = 0.3


def convert_point_to_array(point):
    return np.array([
        [point.x],
        [point.y],
        [point.z],
        [1]
    ])


def calculate_distance_3d(point1, point2):
    return ((point1.x - point2.x) ** 2.0 + (point1.y - point2.y) ** 2.0 + (point1.z - point2.z) ** 2.0) ** 0.5


class Camera:
    def __init__(self, screen_dimensions, spheres, light_source, triangles=None, lines=None):
        self.position = Point3D(0, 0, 0)
        self.lines = lines
        self.triangles = triangles
        self.spheres = spheres
        self.light_source = light_source
        self.f = 2
        self.rotation = Point3D(0, 0, 0)
        self.matrix = None
        self.ray_caster = RayCaster(self.position, self.rotation, self.spheres, screen_dimensions)
        self.phong = Phong(light_source, self.position)
        self.points_3d = self.ray_caster.scan()

    def render(self):
        points_2d = []
        self.phong.set_pos_np()
        for point3d in self.points_3d:
            point_2d = self.translate_point_from_raycast(point3d)
            points_2d.append(point_2d)
        print(self.light_source.center)
        return points_2d

    def translate_point_from_raycast(self, point3d):
        pixel, (point, sphere) = point3d
        color = self.phong.apply_phong(point, sphere)
        return (pixel[0], pixel[1]), color

    def pan_right(self):
        self.light_source.center.x += PAN_STEP

    def pan_left(self):
        self.light_source.center.x -= PAN_STEP

    def pan_up(self):
        self.light_source.center.y -= PAN_STEP

    def pan_down(self):
        self.light_source.center.y += PAN_STEP

    def pan_forward(self):
        self.light_source.center.z += PAN_STEP

    def pan_backward(self):
        self.light_source.center.z -= PAN_STEP

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
