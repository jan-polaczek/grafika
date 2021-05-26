import numpy as np


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Point ({self.x}, {self.y}, {self.z})'

    def __str__(self):
        return f'{self.x} {self.y} {self.z}'

    def to_np(self):
        return np.array([self.x, self.y, self.z], dtype='int64')
