import sys, logging
import pygame
from pygame.locals import *
from framework.layer import EmptyLayer
from framework.singleton import Singleton
from framework.schedule import Scheduler
from framework.event import EventDispatcher
from framework.director import Director


class Application(Singleton):
    """
    应用程序类
    单例模式
    负责在开始时初始化导演类
    维护主循环
    """

    def __init__(self, **kwargs):
        pygame.init()
        pygame.font.init()
        Application._instance = self
        self.director = Director(**kwargs)
        self.screen = None
        self.clock = pygame.time.Clock()

        self.scheduler = Scheduler.instance()
        # self.event_dispatcher = EventDispatcher.instance()
        self.init()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.director.resolution,
                                              self.director.mode,
                                              self.director.depth_color)
        pygame.display.set_caption(self.director.title)

    def run(self):
        if self.director.next_scene is Director.EMPTY_SCENE:
            logging.warning("No scene.Stop running")
            return
        while 1:
            scene = self.director.scene
            if self.director.next_scene != scene:
                if scene != Director.EMPTY_SCENE:
                    scene.on_exit()
                scene = self.director.next_scene
                if scene != Director.EMPTY_SCENE:
                    scene.on_enter()
                self.director.scene = scene
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                scene.handle(event)
            dt = self.clock.tick(self.director.tick)
            self.scheduler.update(dt)
            scene._draw(self.screen)

    def run_with_scene(self, scene):
        self.director.next_scene = scene
        self.run()
