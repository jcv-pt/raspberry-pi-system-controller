from config.config import Config
from log.logger import Logger
from ..disk.disk import Disk
from ..cpu.cpu import Cpu
from ..memory.memory import Memory
from ..reach.reachability import Reachability

class Report:
    @staticmethod
    def getSystemReport(config: Config, logger: Logger):

        # Init system libs
        reachability = Reachability(config, logger)
        disks = Disk(config, logger)
        cpu = Cpu(config, logger)
        memory = Memory(config, logger)

        # CPU : Acquire cpu data
        cpuTemp = cpu.getTemperature()
        cpuPercent = cpu.getUsageAsPercentage()

        # RAM : Acquire ram data
        ramPercent = memory.getUsageAsPercentage()

        # REACH : Check for network reachable hosts
        isReachable = reachability.check()

        # DISK : Check for free space
        isDiskFull = disks.isFull()

        message = ('Raspberry Monitor - System status: \n - CpuTemp : {0}C \n - CpuPercent : {1}% \n - RamPercent : {2}% \n - Network Reachable : {3} \n - Disk Full : {4}'
        .format(cpuTemp, cpuPercent, ramPercent,'Yes' if isReachable else 'No', 'Yes' if isDiskFull else 'No'))

        print(message)