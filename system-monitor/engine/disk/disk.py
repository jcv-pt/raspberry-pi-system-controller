import shutil
import sys

from config.config import Config
from log.logger import Logger

class Disk:
    __config = None
    __logger = None

    def __init__(self, config: Config, logger: Logger):
        self.__logger = logger

        self.__diskList = config.get('Disks', 'Devices').split(',')
        self.__diskWarningPercentage = config.get('Disks', 'WarningPercentage')

    def isFull(self):
        try:
            isFull = False
            for disk in self.__diskList:
                total, used, free = shutil.disk_usage(disk)
                usedPercentage = (used * 100) / total
                if usedPercentage >= int(self.__diskWarningPercentage):
                    isFull = True

            return isFull
        except:
            self.__logger.error('Disk',message='Cannot determine disk space: {0}'.format(sys.exc_info()[0]))

        return None