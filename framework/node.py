import pygame

from framework import dispatcher
from framework.schedule import Scheduler
from framework.event import EventDispatcher

class Node:
    """
    节点类
    提供Composite模式的接口
    绑定Rect
    委托Surface接口
    提供Draw缺省实现
    提供信号/槽接口
    提供update hook
    提供handle hook
    考虑动作功能？
    """

    def __init__(self, parent=None, image=None, rect=None):
        self.parent = parent
        self.children = []
        self.children_table = {}
        self._dispatcher = dispatcher.simple_dispatcher
        if image is None:
            self.__image = pygame.Surface((0, 0))
        else:
            self.__image = image
        if rect is None:
            self.rect = self.image.get_rect()
        else:
            self.rect = rect
        self.init()

    def __getattr__(self, item):
        return getattr(self.__image, item)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, new_image):
        self.__image = new_image
        rect = self.rect
        self.rect = self.__image.get_rect()
        self.rect.topleft = rect.topleft

    def add_child(self, child, zorder=0, tag=None):
        # assert issubclass(Node, type(child))
        self.children.append(child)
        if tag is not None:
            self.children_table[tag] = child

    def remove_child(self, child):
        self.children.remove(child)

    def remove_child_with_tag(self, tag):
        child = self.children_table[tag]
        del self.children_table[tag]
        self.children.remove(child)

    def get_children(self):
        return self.children

    def get_child_by_tag(self, tag):
        return self.children_table.get(tag)

    def set_position(self, pos):
        self.rect.topleft = pos

    def set_x(self, x):
        self.rect.left = x

    def set_y(self, y):
        self.rect.top = y

    def get_x(self):
        return self.rect.left

    def get_y(self):
        return self.rect.top

    def get_rect(self):
        return self.rect

    def init(self):
        """
        初始化hook
        """

    def _draw(self, surf):
        """
        Draw操作
        递归绘制所有孩子
        待完成：按照z-order顺序绘制孩子
        """
        res_rect = surf.blit(self.__image, self.rect)
        for child in self.children:
            child._draw(surf)
        pygame.display.update(res_rect)
        self.draw(surf)

    def schedule(self, callback):
        Scheduler.instance().add_updater(callback)

    def schedule_update(self):
        Scheduler.instance().add_updater(self.update)

    def unschedule(self, callback):
        Scheduler.instance().remove_updater(callback)

    def unschedule_update(self):
        Scheduler.instance().remove_updater(self.update)

    def listen(self, event_type, callback):
        EventDispatcher.instance().add_listener(event_type, callback)

    def update(self, dt):
        """
        Update hook
        """

    def handle(self, event):
        """
        事件hook
        """

    def draw(self, surf):
        """
        渲染hook
        """

    def send(self, signal, *args, **kwds):
        """
        发送信号
        """
        self._dispatcher.send(self, signal, *args, **kwds)

    def connect(self, signal, slot, receiver=None):
        """
        连接信号与槽
        """
        self._dispatcher.connect(self, signal, slot, receiver)
