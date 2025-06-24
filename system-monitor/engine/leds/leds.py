from gpiozero import LED
import time
import threading

from config.config import Config
from log.logger import Logger

class Led:
    __config = None
    __logger = None

    def __init__(self, config: Config, logger: Logger, devicePin: int):
        self.__thread = None
        self.__config = config
        self.__logger = logger
        self.__devicePin = devicePin
        self.__isThreadRunning = False

        # Use gpiozero LED abstraction
        self.__led = LED(self.__devicePin)

    def on(self):
        if self.__isThreadRunning:
            self.__reset()
        self.__led.on()

    def off(self):
        if self.__isThreadRunning:
            self.__reset()
        self.__led.off()

    def flash(self):
        if not self.__isThreadRunning:
            self.__thread = threading.Thread(target=self.__run)
            self.__thread.start()

    def stop(self):
        self.__isThreadRunning = False

    def shutdown(self):
        self.stop()
        self.off()
        self.__led.close()  # Free resources

    def __run(self):
        self.__isThreadRunning = True
        try:
            while self.__isThreadRunning:
                self.__led.on()
                time.sleep(1)
                self.__led.off()
                time.sleep(1)
        except Exception as e:
            self.__logger.error('Leds', message=f'Error while flashing LED: {repr(e)}')

    def __reset(self):
        self.stop()
        time.sleep(2)
