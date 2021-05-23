from point import Point3D
from typing import Union, Tuple


class LightSource:
    def __init__(self, center: Point3D, color: Tuple[int, int, int]):
        self.center = center
        self.color = color

    def __repr__(self):
        return f'Light Source (center: {self.center}, color: {self.color})'
