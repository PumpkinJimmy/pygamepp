import pygame
from framework.layer import Layer
from pygame.locals import *

from framework.node import Node


class GameLayer(Layer):
    def init(self):
        super(GameLayer, self).init()
        img_ball = pygame.image.load("ball.png").convert_alpha()
        self.ball = Node(self, img_ball)
        self.ball.set_position((50, 50))
        self.add_child(self.ball)
        self.schedule_update()

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # self.ball.scroll(-5)
                self.ball.set_x(self.ball.get_x() - 5)
            elif event.key == K_RIGHT:
                self.ball.set_x(self.ball.get_x() + 5)
            elif event.key == K_UP:
                self.ball.set_y(self.ball.get_y() - 5)
            elif event.key == K_DOWN:
                self.ball.set_y(self.ball.get_y() + 5)
