from framework.singleton import Singleton
from framework.dispatcher import simple_dispatcher

class EventDispatcher(Singleton):
    def __init__(self):
        self.dispatcher = simple_dispatcher

    def add_listener(self, signal, slot):
        self.dispatcher.connect(self, signal, slot)

    def handle(self, event):
        self.dispatcher.send(self, event.type, event)

def listen(event_type):
    """
    装饰器，添加回调
    未完成
    """

    def _listen(callback):
        EventDispatcher.instance().add_listener(event_type, callback)
        return callback

    return _listen
