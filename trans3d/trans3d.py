from numpy import *
import pygame
from framework.app import Application
from framework.layer import Layer
resolution = (800, 600)
trans = mat([[1, sqrt(2) / 2, 0],
             [0, sqrt(2) / 2, 1]])
cart_trans = mat([[1, 0],
                  [0, -1]])
cart_b = mat([[0],
              [resolution[1]]])
def to_2d(trans, pos):
    return trans * mat(pos)
def to_cart(trans, pos, b=None):
    if b is None:
        return trans * mat(pos)
    else:
        return trans * mat(pos) + b
class MyLayer(Layer):
    def init(self):
        self.image = pygame.Surface((Application.instance().resolution))
        for x in (0, 100):
            for y in (0, 100):
                for z in (0, 100):
                    pos = mat((x, y, z)).T
                    point = to_cart(cart_trans, to_2d(trans, pos), cart_b)
                    print(point)
                    pygame.draw.circle(self.image, (255, 255, 255), point, 10, 0)

if __name__ == "__main__":
    app = Application()
    scene = MyLayer.create_scene()
    app.run_with_scene(scene)