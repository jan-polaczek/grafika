import sys, pygame
from camera import Camera
from sphere_parser import SphereParser

INPUT_PATH = 'spheres.txt'
black = 0, 0, 0
white = 255, 255, 255
screen_size = 320, 240
pygame.init()


class Scene:
    def __init__(self):
        input_parser = SphereParser(INPUT_PATH)
        spheres, light_source = input_parser.parse()
        self.camera = Camera(screen_size, spheres, light_source)
        self.screen = pygame.display.set_mode(screen_size, pygame.SCALED)
        self.screen.fill(black)
        self.camera_transforms = self.set_camera_transforms()
        self.transforms_to_perform = self.set_transforms_to_perform()
        self.points = self.camera.render()

    def run(self):
        pygame.event.set_grab(False)
        self.screen.fill(black)
        for event in pygame.event.get():
            self.handle_event(event)
        self.draw()
        pygame.display.update()

    def draw(self):
        for point_color in self.points:
            point, color = point_color
            point = self.translate_to_global(point)
            try:
                self.screen.set_at(point, color)
            except ValueError:
                print(color)

    def handle_event(self, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        if event.type == pygame.MOUSEWHEEL:
            self.handle_mousewheel(event.y)
        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.rel)
        self.screen.fill(black)

    def handle_keydown(self, key):
        if key in self.camera_transforms:
            self.camera_transforms[key]()
        self.points = self.camera.render()

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
            pygame.K_UP: self.camera.pan_forward,
            pygame.K_DOWN: self.camera.pan_backward,
            pygame.K_w: self.camera.pan_up,
            pygame.K_s: self.camera.pan_down,
            pygame.K_e: self.camera.rotate_clockwise,
            pygame.K_q: self.camera.rotate_counter_clockwise,
            pygame.K_EQUALS: self.camera.zoom_in,
            pygame.K_MINUS: self.camera.zoom_out
        }

    def set_transforms_to_perform(self):
        return {key: False for key in self.set_camera_transforms().keys()}

    def translate_to_global(self, point):
        return int(point[0] + screen_size[0] / 2), int(point[1] + screen_size[1] / 2)

