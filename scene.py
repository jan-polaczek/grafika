import sys, pygame
from camera import Camera
from triangle_parser import TriangleParser
from input_parser import InputParser

INPUT_PATH = 'triangles.txt'
FPS = 30
black = 0, 0, 0
white = 255, 255, 255
pygame.init()


class Scene:
    def __init__(self):
        input_parser = TriangleParser(INPUT_PATH)
        input_parser2 = InputParser('lines.txt')
        triangles = input_parser.parse()
        lines = input_parser2.parse()
        self.camera = Camera(lines, triangles)
        self.screen = pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED)
        self.screen.fill(black)
        self.camera_transforms = self.set_camera_transforms()
        self.transforms_to_perform = self.set_transforms_to_perform()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

    def run(self):
        pygame.event.set_grab(True)
        self.screen.fill(black)
        for event in pygame.event.get():
            self.handle_event(event)
        self.perform_transforms()
        self.draw()
        pygame.display.update()
        self.clock.tick(FPS)

    def draw_triangles(self):
        self.camera.draw_triangles(self.screen)

    def draw(self):
        lines_2d, triangles_2d = self.camera.render()
        for line in lines_2d:
            if line.start is None or line.end is None:
                continue
            pygame.draw.line(self.screen, white, self.translate_to_global(line.start), self.translate_to_global(line.end))

        for triangle in triangles_2d:
            if triangle.a is None or triangle.b is None or triangle.c is None:
                continue
            points = self.translate_to_global(triangle.a), self.translate_to_global(triangle.b), self.translate_to_global(triangle.c)
            pygame.draw.polygon(self.screen, triangle.color, points)

    def handle_event(self, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        if event.type == pygame.KEYUP:
            self.handle_keyup(event.key)
        if event.type == pygame.MOUSEWHEEL:
            self.handle_mousewheel(event.y)
        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.rel)
        self.screen.fill(black)

    def handle_keydown(self, key):
        if key in self.transforms_to_perform:
            self.transforms_to_perform[key] = True

    def handle_keyup(self, key):
        if key in self.transforms_to_perform:
            self.transforms_to_perform[key] = False

    def handle_mousewheel(self, amount):
        self.camera.zoom(amount)

    def handle_mouse_motion(self, movement):
        self.camera.rotate(movement)

    def perform_transforms(self):
        for key in self.transforms_to_perform.keys():
            if self.transforms_to_perform[key]:
                self.camera_transforms[key]()

    def set_camera_transforms(self):
        return {
            pygame.K_d: self.camera.pan_right,
            pygame.K_a: self.camera.pan_left,
            pygame.K_UP: self.camera.pan_up,
            pygame.K_DOWN: self.camera.pan_down,
            pygame.K_w: self.camera.pan_forward,
            pygame.K_s: self.camera.pan_backward,
            pygame.K_e: self.camera.rotate_clockwise,
            pygame.K_q: self.camera.rotate_counter_clockwise,
            pygame.K_EQUALS: self.camera.zoom_in,
            pygame.K_MINUS: self.camera.zoom_out
        }

    def set_transforms_to_perform(self):
        return {key: False for key in self.set_camera_transforms().keys()}

    def translate_to_global(self, point):
        return point[0] + self.screen.get_size()[0] / 2, point[1] + self.screen.get_size()[1] / 2

