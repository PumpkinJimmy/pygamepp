import logging
from framework.singleton import Singleton


class Scheduler(Singleton):
    """
    记录所有定时器回调
    单例模式
    """

    def __init__(self):
        self.updaters = []

    def add_updater(self, updater):
        self.updaters.append(updater)

    def remove_updater(self, updater):
        try:
            self.updaters.remove(updater)
        except ValueError:
            logging.warning("Unschdule a not exist updater")

    def update(self, dt):
        for updater in self.updaters:
            updater(dt)
