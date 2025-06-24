import sys
import psutil

from config.config import Config
from log.logger import Logger

class Memory:
    __config = None
    __logger = None

    def __init__(self, config: Config, logger: Logger):
        self.__config = config
        self.__logger = logger

        self.__warningPercentage = self.__config.get('RAM', 'WarningPercentage')

    def getUsageAsPercentage(self):
        try:
            return int((psutil.virtual_memory().available * 100) / psutil.virtual_memory().total)
        except:  # handle other exceptions such as attribute errors
            self.__logger.error('Memory',message='Cannot read CPU usage, unknown error: {0}'.format(sys.exc_info()[0]))

        return None

    def isFull(self):
        return self.getUsageAsPercentage() >= int(self.__warningPercentage)