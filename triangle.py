from point import Point3D
from camera import convert_point_to_array
import numpy as np
import pygame


class Triangle3D:

    def __init__(self, points, color = None):
        self.vertices = points
        self.color = color
        
    def __repr__(self):
        return f'A: {self.vertices[0]} B: {self.vertices[1]} C: {self.vertices[2]} color: {self.color}'

    def draw(self, display, final_transform, f):
        if not color:
            self.color = (255, 0, 0)

        vertices2D = [final_transform.dot(convert_point_to_array(point))
            for v in self.vertices]

        for v in vertices2D:
            v = v * (f / v[2, 0])
            v = (v[0][0] * 400, v[1][0] * 400)

        pygame.draw.polygon(display, self.color, vertices2D)