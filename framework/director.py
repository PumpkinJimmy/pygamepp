import pygame
from pygame.locals import *
from framework.singleton import Singleton

class Director(Singleton):
    EMPTY_SCENE = 0
    def __init__(self,
                 title="Pygame++",
                 resolution=(800, 600),
                 tick=60,
                 mode=0,
                 depth_color=32,
                 font_famliy=None,
                 font_size=32,
                 cap_size=72
                 ):
        Director._instance = self
        self.title = title
        self.resolution = resolution
        self.tick = tick
        self.mode = mode
        self.depth_color = depth_color
        self.font_family = font_famliy
        self.font_size = font_size
        self.cap_size = cap_size
        self.font = pygame.font.Font(self.font_family, self.font_size)
        self.rect = Rect(0, 0, self.resolution[0], self.resolution[1])
        self.scene = Director.EMPTY_SCENE
        self.next_scene = Director.EMPTY_SCENE
    def replace_scene(self, scene):
        self.next_scene = scene