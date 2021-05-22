from point import Point3D
from typing import Union, Tuple


class Sphere:
    def __init__(self, center: Point3D, radius: Union[int, float], color: Tuple[int, int, int]):
        self.center = center
        self.radius = radius
        self.color = color

    def __repr__(self):
        return f'Sphere(center: {self.center}, radius: {self.radius}, color: {self.color})'
