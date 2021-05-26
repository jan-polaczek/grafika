from point import Point3D
from typing import Union, Tuple


class LightSource:
    def __init__(self, center: Point3D = Point3D(0, 0, 0),
                 i_a: Tuple[int, int, int] = (255, 255, 255),
                 i_s: Tuple[int, int, int] = (255, 255, 255),
                 i_d: Tuple[int, int, int] = (255, 255, 255)):
        self.center = center
        self.i_a = i_a
        self.i_s = i_s
        self.i_d = i_d

    def __repr__(self):
        return f'Light Source (center: {self.center})'
