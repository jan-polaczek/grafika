from point import Point3D
from typing import Union, Tuple


class LightSource:
    def __init__(self, center: Point3D, i_a: Tuple[int, int, int], i_s: Tuple[int, int, int], i_d: Tuple[int, int, int]):
        self.center = center
        self.i_a = i_a
        self.i_s = i_s
        self.i_d = i_d

    def __repr__(self):
        return f'Light Source (center: {self.center})'
