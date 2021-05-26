from light_source import LightSource
from point import Point3D
from typing import Tuple
import numpy as np


def normalize(v: np.array):
    return v / np.linalg.norm(v)


# nazwy wektorów takie jak na angielskiej wikipedii
class Phong:
    def __init__(self, light_source: LightSource, camera_position: Point3D):
        self.light_source = light_source
        self.camera_pos = camera_position
        self.light_pos_np = None
        self.camera_pos_np = None

    def apply_phong(self, point: np.array, k_s: Tuple[float, float, float], k_d: Tuple[float, float, float], k_a: Tuple[float, float, float], alpha: float, sphere):
        v = self.get_v(point)
        n = self.get_n(point, sphere)
        l = self.get_l(point)
        r = self.get_r(l, n)
        rgb = np.array([
            self.calculate_phong_part(k_s_i, k_d_i, k_a_i, i_s_i, i_d_i, i_a_i, v, n, l, r, alpha)
            for k_s_i, k_d_i, k_a_i, i_s_i, i_d_i, i_a_i
            in zip(k_s, k_d, k_a, self.light_source.i_s, self.light_source.i_d, self.light_source.i_a)])
        return rgb

    @staticmethod
    def calculate_phong_part(k_s_i, k_d_i, k_a_i, i_s_i, i_d_i, i_a_i, v, n, l, r, alpha):
        res = k_a_i * i_a_i
        l_n = l.dot(n)
        res += k_d_i * i_d_i * l_n if l_n > 0 else 0
        r_v = r.dot(v)
        res += k_s_i * i_s_i * r_v ** alpha if r_v > 0 else 0
        return min(int((res / 255)), 255)

    def set_pos_np(self):
        self.light_pos_np = self.light_source.center.to_np()
        self.camera_pos_np = self.camera_pos.to_np()

    def get_v(self, point: np.array):
        return normalize(point - self.camera_pos_np)

    def get_n(self, point: np.array, sphere):
        return normalize(point - sphere.center.to_np())

    def get_l(self, point: np.array):
        return normalize(self.light_pos_np - point)

    def get_r(self, l: np.array, n: np.array):
        return normalize(l - 2 * (l.dot(n)) * n)
