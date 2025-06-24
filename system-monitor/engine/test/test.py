from config.config import Config
from log.logger import Logger
from ..leds.leds import Led
from ..fan.fan import Fan
from time import sleep
import threading

class Test:

    def __init__(self, config: Config, logger: Logger, app):
        self.__config = config
        self.__logger = logger
        self.__app = app
        self.__isShutdown = False

    def start(self):
        if self.__app['test'] == 'leds':
            # Start the run thread
            self.__thread = threading.Thread(target=self.__testLeds)
        elif self.__app['test'] == 'fan':
            # Start the run thread
            self.__thread = threading.Thread(target=self.__testFan)
        else:
            self.__logger.info('Test', message='Invalid test type, press CTRL + C to exit')
            return

        self.__thread.start()

    def __testLeds(self):

        #Intialize LED's handlers
        __ledActive = Led(self.__config, self.__logger,int(self.__config.get('Indicators', 'GPIORunning')))
        __ledNetwork = Led(self.__config, self.__logger, int(self.__config.get('Indicators', 'GPIOConnectivity')))
        __ledWarning = Led(self.__config, self.__logger, int(self.__config.get('Indicators', 'GPIOAlert')))

        self.__logger.info('Test', message='Starting LED test sequence')

        __ledActive.flash()
        __ledNetwork.flash()
        __ledWarning.flash()

        while self.__isShutdown is False:
            sleep(1)

        __ledActive.stop()
        __ledNetwork.stop()
        __ledWarning.stop()

    def __testFan(self):

        __fan = Fan(self.__config, self.__logger)

        while self.__isShutdown is False:
            __fan.adjustRotation(100)
            sleep(10)
            if self.__isShutdown is True:
                break
            __fan.adjustRotation(0)
            sleep(10)

    def stop(self):
        self.__logger.info('Test', message='Stopping test sequence')
        self.__isShutdown = True