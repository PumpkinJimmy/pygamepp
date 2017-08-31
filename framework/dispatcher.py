import logging


class SignalDispatcher:
    """
    调度器的抽象接口
    单例模式
    """

    def connect(self, sender, signal, slot):
        return NotImplemented

    def send(self, sender, signal):
        return NotImplemented


class SimpleSignalDispatcher(SignalDispatcher):
    """
    信号/槽的简单实现
    """
    def __init__(self):
        self._connections = {}

    def connect(self, sender, signal, slot, receiver=None):
        """
        嵌套字典保存槽函数，以sender,signal为键
        slot可以是一个函数，也可以是一个字符串
        当slot是一个字符串时，槽函数为receiver的（"on_" + slot）方法
        当slot不合法时，使用_invalid_slot占位
        """
        if callable(slot):
            self._connections.setdefault(sender, {}).setdefault(signal, []).append(slot)
        elif type(slot) == str:
            if receiver is not None:
                method = self._get_method(receiver, slot)
                self._connections.setdefault(sender, {}).setdefault(signal, []).append(method)
                if method == self._invalid_slot:
                    logging.warning("No given method")
            else:
                logging.warning("Invalid Receiver")
        else:
            logging.warning("Invalid Slot")

    def _get_method(self, obj, name):
        return getattr(obj, "on_" + name, self._invalid_slot)

    def _invalid_slot(self, *args, **kwds):
        """"
        不合法槽，占位。
        """
        logging.error("Call a invalid slot")
        raise Exception("Call a invalid slot")

    def send(self, sender, signal, *args, **kwds):
        """"
        查表广播
        """
        for slot in self._connections.get(sender, {}).get(signal, []):
            slot(*args, **kwds)


simple_dispatcher = SimpleSignalDispatcher()