import RPi.GPIO as GPIO
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

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__devicePin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        if self.__isThreadRunning:
            self.__reset()
        GPIO.output(self.__devicePin, GPIO.HIGH)  # Led will be switched on

    def off(self):
        if self.__isThreadRunning:
            self.__reset()
        GPIO.output(self.__devicePin, GPIO.LOW)  # Led will be switched off

    def flash(self):
        if not self.__isThreadRunning:
            self.__thread = threading.Thread(target=self.__run)
            self.__thread.start()

    def stop(self):
        self.__isThreadRunning = False

    def shutdown(self):
        self.stop()
        self.off()
        GPIO.cleanup(self.__devicePin)

    def __run(self):
        self.__isThreadRunning = True
        try:
            while self.__isThreadRunning:
                GPIO.output(self.__devicePin, GPIO.HIGH)  # Led will be switched on
                time.sleep(1)  # Waitmode for y seconds
                GPIO.output(self.__devicePin, GPIO.LOW)  # Led will be switched off
                time.sleep(1)  # Waitmode for x seconds
        except Exception as e:
            self.__logger.error('Leds',message='Error while setting GPIO pins: {0}'.format(repr(e)))

    def __reset(self):
        self.stop()
        time.sleep(2)