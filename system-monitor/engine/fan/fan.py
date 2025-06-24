import json

from ..pwm.pwm import PWM
from config.config import Config
from log.logger import Logger

class Fan:
    __config = None
    __logger = None
    __pwm = None

    __minRotationPercent = None
    __maxRotationPercent = None
    __currentRotationPercent = 0
    __shutdownIsStopped = False
    __shutdownGraceTime = None

    def __init__(self, config: Config, logger: Logger):
        # Init libs
        self.__config = config
        self.__logger = logger
        self.__pwm = PWM(self.__config, self.__logger)

        # Init variables
        self.__minRotationPercent = 0
        self.__maxRotationPercent = 100
        self.__shutdownGraceTime = int(self.__config.get('Fan', 'ShutdownGraceTime'))
        self.__rotationProfiles = json.loads(self.__config.get('Fan', 'RotationProfile'))

        self.__currentRotationPercent = self.__maxRotationPercent

    def adjustRotation(self, cpuTemp: int):
        # Calculate rotation based on profiles
        rotationPercent = self.__calculateRotationPercent(cpuTemp)
        # Set pwm to %
        if rotationPercent != self.__currentRotationPercent:
            self.__currentRotationPercent = rotationPercent
            self.__pwm.setDutyCycle(self.__currentRotationPercent)
            # Report
            self.__logger.info('Fan', message='Status update : Rotation[{0}%], Status [{1}]'.format(self.__currentRotationPercent,'ON' if self.__shutdownIsStopped is False else 'OFF'))

    def getRotationPercent(self):

        return self.__currentRotationPercent

    def __calculateRotationPercent(self, cpuTemp: int):

        rotationPercent = self.__maxRotationPercent

        for profile in self.__rotationProfiles:
            if float(profile['from']) <= float(cpuTemp) <= float(profile['to']):
                rotationPercent = int(profile['rotation'])
                break

        if rotationPercent < self.__minRotationPercent:
            rotationPercent = self.__minRotationPercent

        if rotationPercent > self.__maxRotationPercent:
            rotationPercent = self.__maxRotationPercent

        return rotationPercent
