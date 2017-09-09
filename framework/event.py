from framework.singleton import Singleton
from framework.dispatcher import SignalDispatcher


# class EventDispatcher(Singleton):
#     def __init__(self):
#         self.dispatcher = simple_dispatcher
#
#     def add_listener(self, signal, slot):
#         self.dispatcher.connect(self, signal, slot)
#
#     def handle(self, event):
#         self.dispatcher.send(self, event.type, event)
class EventListener:
    def __init__(self, sender, signal, slot, receiver=None):
        self.sender = sender
        self.signal = signal
        self.slot = slot
        self.receiver = receiver


class EventDispatcher(SignalDispatcher):
    def __init__(self):
        self.listeners = []

    def connect(self, sender, signal, slot, receiver=None):
        listener = EventListener(sender, signal, slot, receiver)
        self.listeners.append(listener)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener_by_sender(self, sender):
        for listener in self.listeners[:]:
            if listener.sender == sender:
                self.listeners.remove(listener)

    def remove_listener_by_receiver(self, receiver):
        for listener in self.listeners[:]:
            if listener.receiver == receiver:
                self.listeners.remove(listener)

    def send(self, sender, signal, *args, **kwargs):
        for listener in self.listeners:
            if listener.sender == sender and listener.signal == signal:
                listener.slot(*args, **kwargs)


def listen(event_type):
    """
    装饰器，添加回调
    未完成
    """

    def _listen(callback):
        EventDispatcher.instance().add_listener(event_type, callback)
        return callback

    return _listen
