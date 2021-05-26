from point import Point3D
from sphere import Sphere
from typing import List, Tuple, Union
import numpy as np


'''
Źródła:
http://www.ccs.neu.edu/home/fell/CS4300/Lectures/Ray-TracingFormulas.pdf
https://github.com/xhacker/raycast/tree/master/raycast
'''


def normalize(v: np.array):
    return v / np.linalg.norm(v)


class RayCaster:
    def __init__(self, camera_position: Point3D, camera_rotation: Point3D, spheres: List[Sphere], screen_dimensions: Tuple[int, int]):
        self.camera_position = camera_position
        self.camera_rotation = camera_rotation
        self.spheres = spheres
        self.screen_dimensions = screen_dimensions
        self.z = 40
        self.origin = None
        self.oc_list = []
        self.c_list = []
        self.pixels = [np.array([x, y, self.z])
                       for y in range(int(-self.screen_dimensions[1] / 2), int(self.screen_dimensions[1] / 2))
                       for x in range(int(-self.screen_dimensions[0] / 2), int(self.screen_dimensions[0] / 2))]

    def scan(self) -> List[Tuple[np.array, Tuple[Point3D, Sphere]]]:
        result = []
        self.origin = self.camera_position.to_np()
        self.oc_list = [self.origin - sphere.center.to_np() for sphere in self.spheres]

        self.c_list = [oc.dot(oc) - sphere.radius ** 2 for oc, sphere in zip(self.oc_list, self.spheres)]

        for pixel in self.pixels:
            partial_result = self.cast_rays_per_pixel(pixel)
            if partial_result:
                result.append((pixel, partial_result))
        return result

    def cast_rays_per_pixel(self, pixel: np.array) -> Tuple[np.array, Sphere]:
        t = -1
        result = False
        for i, sphere in enumerate(self.spheres):
            ray_cast = self.cast_ray(pixel, self.oc_list[i], self.c_list[i])
            if not ray_cast:
                continue
            new_t, x, y, z = ray_cast
            if new_t < t or t == -1:
                result = np.array([x, y, z]), sphere
                t = new_t
        return result

    def cast_ray(self, pixel: np.array, oc: np.array, c: np.array) -> Union[bool, Tuple[float, float, float, float]]:
        origin = self.origin
        direction = pixel - origin

        a, b, discriminant = self.calculate_discriminant(direction, oc, c)
        if discriminant < 0:
            return False
        t = (-b - discriminant ** 0.5) / (2 * a)
        if t < 0:
            return False
        x = origin[0] + t * direction[0]
        y = origin[1] + t * direction[1]
        z = origin[2] + t * direction[2]
        return t, x, y, z

    @staticmethod
    def calculate_discriminant(direction, oc, c):
        a = direction.dot(direction)
        b = 2 * direction.dot(oc)
        return a, b, b ** 2 - 4 * a * c
