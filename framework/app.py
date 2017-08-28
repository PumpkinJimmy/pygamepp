import sys, logging
import pygame
from pygame.locals import *
from framework.singleton import Singleton
from framework.schedule import Scheduler

class Application(Singleton):
    """
    应用程序类
    单例模式
    负责在开始时初始化基本信息
    维护主循环，处理事件的接收/分发
    """

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
        pygame.init()
        pygame.font.init()
        Application._instance = self
        self.title = title
        self.resolution = resolution
        self.tick = tick
        self.mode = mode
        self.depth_color = depth_color
        self.font_family = font_famliy
        self.font_size = font_size
        self.cap_size = cap_size
        self.font = pygame.font.Font(self.font_family, self.font_size)
        self.screen = None
        self.clock = pygame.time.Clock()
        self.scene = None
        self.scheduler = Scheduler.instance()
        self.init()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution, self.mode, self.depth_color)
        pygame.display.set_caption(self.title)

    def run(self):
        if self.scene is None:
            logging.warning("No scene.Stop running")
            return
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.scene._handle(event)
            dt = self.clock.tick(self.tick)
            # self.scene._update(dt)
            self.scheduler.update(dt)
            self.scene._draw(self.screen)

    def run_with_scene(self, scene):
        self.scene = scene
        self.run()

    def replace_scene(self, scene):
        self.scene = scene
