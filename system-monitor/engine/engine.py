from time import sleep, time
from config.config import Config
from log.logger import Logger
from .fan.fan import Fan
from .disk.disk import Disk
from .cpu.cpu import Cpu
from .memory.memory import Memory
from .reach.reachability import Reachability
from .leds.leds import Led

import os
import threading
import traceback

class Engine:
    __config = None
    __logger = None
    __thread = None
    __temperature = None
    __running = False
    __failureManifest = {}

    def __init__(self, config: Config, logger: Logger):
        self.__config = config
        self.__logger = logger

        # Initialize class modules
        self.__fan = Fan(self.__config, self.__logger)
        self.__reachability = Reachability(self.__config, self.__logger)
        self.__disks = Disk(self.__config, self.__logger)
        self.__cpu = Cpu(self.__config, self.__logger)
        self.__memory = Memory(self.__config, self.__logger)

        # Initialize vars
        self.__tempLastUpdate = None
        self.__alertMode = self.__config.get('Indicators', 'AlertMode')

        #Intialize LED's handlers
        self.__ledActive = Led(self.__config, self.__logger,int(self.__config.get('Indicators', 'GPIORunning')))
        self.__ledNetwork = Led(self.__config, self.__logger, int(self.__config.get('Indicators', 'GPIOConnectivity')))
        self.__ledWarning = Led(self.__config, self.__logger, int(self.__config.get('Indicators', 'GPIOAlert')))

    def start(self):
        self.__running = True
        # Switch on the running indicator
        self.__ledActive.on()
        # Start the run thread
        self.__thread = threading.Thread(target=self.__run)
        self.__thread.start()

    def stop(self):
        self.__logger.info('Engine', message='Stop signal received, terminating engine thread...')
        self.__running = False
        # Switch off running indicators
        self.__ledActive.shutdown()
        self.__ledNetwork.shutdown()
        self.__ledWarning.shutdown()

    def isRunning(self):
        return self.__running

    def __run(self):
        while self.__running:
            try:
                self.__iterate()
            except Exception as ex:
                self.__logger.error('Engine',message='CRASH, entering crash mode, engine iteration reported a failure: {0}'.format(repr(ex)))
                self.__logger.error('Engine',message='- Stack: {0}'.format(traceback.format_exc()))
                self.__crash()

            sleep(15)

    def __iterate(self):

        # CPU : Acquire cpu data
        cpuTemp = self.__cpu.getTemperature()
        cpuPercent =  self.__cpu.getUsageAsPercentage()
        isCpuFull = self.__cpu.isFull()

        # RAM : Acquire ram data
        ramPercent = self.__memory.getUsageAsPercentage()
        isRamFull = self.__memory.isFull()

        # REACH : Check for network reachable hosts
        isReachable = self.__reachability.check()

        # DISK : Check for free space
        isDiskFull = self.__disks.isFull()

        # FAN : Adjust fan rotation based on CPU temp. Add a 30 sec between updates
        currentEpoch = int(time())
        if self.__tempLastUpdate is None or self.__tempLastUpdate + 30 > currentEpoch:
            self.__tempLastUpdate = currentEpoch
            self.__fan.adjustRotation(cpuTemp)

        # Set Indicators State - Network
        if isReachable is True:
            self.__ledNetwork.on()
        else:
            if self.__alertMode == 'flash':
                self.__ledNetwork.flash()
            else:
                self.__ledNetwork.off()

        # Set Indicators State - Warning
        if isReachable is False or isDiskFull is True or isRamFull is True or isCpuFull is True:
            if self.__alertMode == 'flash':
                self.__ledWarning.flash()
            else:
                self.__ledWarning.on()
        else:
            self.__ledWarning.off()

        # Log
        self.__logger.info('Engine', message='Iteration status: CpuTemp [{0}C], CpuPercent [{1}%], RamPercent [{2}%], Fan Rotation [{3}%], Network Reachable [{4}], Disk Full [{5}]'.format(cpuTemp, cpuPercent, ramPercent, self.__fan.getRotationPercent(), 'Yes' if isReachable else 'No', 'Yes' if isDiskFull else 'No'))

    def __reset(self):
        self.__logger.info('Engine', message='Reset requested, engine values restored to default')

    def __crash(self):
        self.stop()
        os._exit(1)
