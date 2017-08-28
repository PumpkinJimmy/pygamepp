import pygame
from framework.app import Application
from framework.scene import Scene

from framework.node import Node


class Layer(Node):
    """
    层节点，负责事件响应，发送信号
    考虑动作的执行（还是说放在Node?）
    """

    def init(self):
        super(Layer, self).init()
        self.shallow = False
        self.image = pygame.Surface(Application.instance().resolution)
        self.rect = self.image.get_rect()

    @classmethod
    def create_scene(cls):
        scene = Scene()
        layer = cls(scene)
        scene.add_child(layer)
        return scene

    def handle(self, event):
        self.send(event.type, event)
        for child in self.children:
            child.handle(child)