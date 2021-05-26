from point import Point3D
from typing import Union, Tuple


class Sphere:
    def __init__(self, center: Point3D = Point3D(0, 0, 0), radius: Union[int, float] = 20,
                 k_s: Tuple[int, int, int] = (255, 255, 255),
                 k_d: Tuple[int, int, int] = (255, 255, 255),
                 k_a: Tuple[int, int, int] = (255, 255, 255),
                 alpha: float = 2.0):
        self.center = center
        self.radius = radius
        self.k_s = k_s
        self.k_d = k_d
        self.k_a = k_a
        self.alpha = alpha

    def __repr__(self):
        return f'Sphere(center: {self.center}, radius: {self.radius})'
