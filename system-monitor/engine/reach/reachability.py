import sys

from config.config import Config
from log.logger import Logger
from ..ping.ping import Ping

class Reachability:
    __config = None
    __logger = None

    def __init__(self, config: Config, logger: Logger):
        self.__config = config
        self.__logger = logger

        self.__hostList = config.get('Connectivity', 'Hosts').split(',')

    def check(self):
        try:
            reachableCount = 0
            for host in self.__hostList:
                if host == 'gateway':
                    reachableCount += int(Ping.gateway())
                else:
                    reachableCount += int(Ping.host(host))
            return reachableCount == len(self.__hostList)
        except:
            self.__logger.error('Reach',message='Cannot check network reachability: {0}'.format(sys.exc_info()[0]))

        return None

