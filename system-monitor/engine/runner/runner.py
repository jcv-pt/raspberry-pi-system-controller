from filesystem.signals import Signals
from time import sleep

class Runner:
    __config = None
    __logger = None
    __app = None
    __instance = None

    def __init__(self, instance, *args, **kwargs):
        self.__instance = instance(*args, **kwargs)

    def start(self):
        self.__instance.start()

    def run(self):
        osSignals = Signals()
        while osSignals.isRunning():
            sleep(1)

    def stop(self):
        self.__instance.stop()
