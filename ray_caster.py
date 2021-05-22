from point import Point3D
from sphere import Sphere
from typing import List, Tuple, Union
import numpy as np
from math import sin, cos


class RayCaster:
    def __init__(self, camera_position: Point3D, camera_rotation: Point3D, spheres: List[Sphere], screen_dimensions: Tuple[int, int]):
        self.camera_position = camera_position
        self.camera_rotation = camera_rotation
        self.spheres = spheres
        self.screen_dimensions = screen_dimensions

    def scan(self) -> List[Tuple[Point3D, Tuple[Point3D, Sphere]]]:
        result = []
        for x in range(int(-self.screen_dimensions[0] / 2), int(self.screen_dimensions[0] / 2), 2):
            for y in range(int(-self.screen_dimensions[1] / 2), int(self.screen_dimensions[1] / 2), 2):
                z = -20
                pixel = Point3D(x, y, z)
                partial_result = self.cast_rays_per_pixel(pixel)
                if partial_result:
                    result.append((pixel, partial_result))
        return result

    def cast_rays_per_pixel(self, pixel: Point3D) -> Tuple[Point3D, Sphere]:
        t = -1
        result = False
        for sphere in self.spheres:
            ray_cast = self.cast_ray(pixel, sphere)
            if not ray_cast:
                continue
            new_t, x, y, z = ray_cast
            if new_t > t or t == -1:
                result = Point3D(x, y, z), sphere
                t = new_t
        return result

    def cast_ray(self, point: Point3D, sphere: Sphere) -> Union[bool, Tuple[float, float, float, float]]:
        rot = self.camera_rotation
        origin = self.camera_position.to_np()
        direction = np.array([
            point.x * cos(-rot.y) * cos(-rot.z) - point.y * sin(-rot.z) + point.z * sin(-rot.y),
            point.y * cos(-rot.x) * cos(-rot.z) + point.x * sin(-rot.z) - point.z * sin(-rot.x),
            point.z * cos(-rot.x) * cos(-rot.y) - point.x * sin(-rot.y) + point.y * sin(-rot.x)
        ]) - origin
        #direction = point.to_np() - origin
        center = sphere.center.to_np()

        oc = origin - center
        a = direction.dot(direction)
        b = 2 * direction.dot(oc)
        c = oc.dot(oc) - sphere.radius ** 2
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return False
        t = (-b - discriminant ** 0.5) / (2 * a)
        if t > 0:
            return False
        return t, 0, 0, 0
