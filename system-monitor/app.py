import os
import argparse
import time

from datetime import datetime

from log.logger import Logger
from config.config import Config
from engine.engine import Engine
from engine.report.report import Report
from engine.test.test import Test
from engine.runner.runner import Runner

class App:

    def run(self):

        # Initialize app args
        argParser = argparse.ArgumentParser(description='Raspberry PI : Monitor Engine - Monitors Machine Status & Fans')
        argParser.add_argument('--verbose', dest='verbose', type=int, default=1, help='Weather to display logging output')
        argParser.add_argument('--debug', dest='debug', type=int, default=0, help='Weather to print debug data to console')
        argParser.add_argument('--report', dest='report', action='store_true', help='Print system report')
        argParser.add_argument('--test', dest='test', type=str, default='', help='Test leds')

        args = argParser.parse_args()

        # Initialize app var
        app = {
            'rid': datetime.today().strftime('%Y-%m-%d_%H%M%S'),
            'stime': time.time(),
            'sdate': datetime.today().strftime('%Y-%m-%d'),
            'path': os.path.abspath(os.getcwd()),
            'verbose': bool(args.verbose),
            'debug': bool(args.debug),
            'report': bool(args.report),
            'test': args.test,
        }

        # Initialize logger & config
        config = Config(app['path'] + '/data/config/default.ini')
        logger = Logger(app['path'] + '/data/logs/', app['rid'], verbose=app['verbose'], debug=app['debug'], maxLogLines=int(config.get('Logs', 'MaxLogLines')), maxFilesCount=int(config.get('Logs', 'MaxFilesCount')))

        # Initialize runner handler depending on console request
        if app['report'] is True:
            runner = Runner(Report, config, logger)
        elif app['test'] != '':
            runner = Runner(Test, config, logger, app)
        else:
            runner = Runner(Engine, config, logger)

        # Start task
        runner.start()

        # Run task
        runner.run()

        # Stop task
        runner.stop()

        # Report & cleanup
        logger.info(message='Shutting down...')
        logger.purge()

        # Exit
        if logger.hasErrors() is True:
            exit(1)

        exit(0)