import logging
import pygame

from framework import dispatcher
from framework.schedule import Scheduler
from framework.event import EventDispatcher, EventListener


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
        self.event_dispatcher = None
        self._listeners = []
        self.installed = False
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
        child.parent = self
        if tag is not None:
            self.children_table[tag] = child

    def remove_child(self, child):
        child.parent = None
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
        """
        准备事件监听
        如果self.installed，事件监听会被马上加载
        """
        self._listeners.append(EventListener(None, event_type, callback, receiver=self))
        if self.installed:
            self.load_listener(self._listeners)

    def load_listener(self, listeners):
        """
        职责链
        向上请求一个事件调度器来添加事件监听
        :return: 事件调度器或None（在listeners为空时）
        """
        if len(listeners) == 0:
            return
        if self.event_dispatcher is None:
            if self.parent is None:
                logging.warning("No event dispatcher. Failed load listeners")
                return
            self.parent.load_listener(listeners)
            # self.event_dispatcher = self.parent.load_listener(listeners)
        else:
            for listener in listeners:
                listener.sender = self
                self.event_dispatcher.add_listener(listener)
        return self.event_dispatcher

    def remove_listener(self, node):
        """
        职责链
        向上请求一个事件调度器来移除给定节点所有相关事件监听
        :param node: 节点
        :return: 事件调度器
        """
        if self.event_dispatcher is None:
            if self.parent is not None:
                self.parent.remove_listener(node)
                # self.event_dispatcher = self.parent.remove_listener(node)
        else:
            self.event_dispatcher.remove_listener_by_sender(node)
            self.event_dispatcher.remove_listener_by_receiver(node)
        return self.event_dispatcher

    def on_enter(self):
        """
        节点载入时执行
        先调用当前结点on_enter，再调用孩子
        """
        self.installed = True
        self.load_listener(self._listeners)
        self._listeners = []
        for child in self.children:
            child.on_enter()

    def on_exit(self):
        """
        节点卸载时执行
        先调用孩子on_enter，再调用当前节点
        """
        for child in self.children:
            child.on_exit()
        self.installed = False
        self.remove_listener(self)

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
