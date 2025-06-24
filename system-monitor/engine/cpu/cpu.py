import sys
import psutil

from config.config import Config
from log.logger import Logger

class Cpu:
    __config = None
    __logger = None

    def __init__(self, config: Config, logger: Logger):
        self.__config = config
        self.__logger = logger

        self.__warningPercentage = int(self.__config.get('CPU', 'WarningPercentage'))

    def getTemperature(self):

        try:
            # Read the temperature from /sys/class/thermal/thermal_zone0/temp
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = f.read().strip()
                # Convert the value from millidegrees Celsius to degrees Celsius
                return int(int(temp) / 1000.0)
        except:  # handle other exceptions such as attribute errors
            self.__logger.error('Cpu',message='Cannot read CPU temp, unknown error: {0}'.format(sys.exc_info()[0]))

        return None

    def getUsageAsPercentage(self):
        try:
            return int(psutil.cpu_percent())
        except:  # handle other exceptions such as attribute errors
            self.__logger.error('Cpu',message='Cannot read CPU usage, unknown error: {0}'.format(sys.exc_info()[0]))

        return None

    def isFull(self):
        return self.getUsageAsPercentage() >=  self.__warningPercentage