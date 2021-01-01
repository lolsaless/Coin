import time
import signal
import argparse

from smtm import *
import requests
import threading

class SmtmSimulator:
    def __init__(self, end=None, count=None):
        self.logger = LogManager.get_logger("SmtmSimulator")
        self.__stop = False
        self.end = end
        self.count = count

        if self.end is not None:
            self.end = self.end.replace('T', ' ')

        self.logger.info(f'end: {end}')
        self.logger.info(f'count: {count}')
        self.logger.info(f'simulation is started ===================')

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def main(self):
        operator = SimulationOperator()
        self.operator = operator
        operator.initialize(requests, threading, 
            SimulationDataProvider(),
            StrategyBuyAndHold(),
            SimulationTrader(),
            end=self.end,
            count=self.count,
            budget=50000)
        operator.setup(2)

        if operator.start() != True:
            self.logger.warning("Fail start")
            return

        while not self.__stop:
            time.sleep(1)

    def stop(self, signum, frame):
        self.__stop = True
        if self.operator is not None:
            self.operator.stop()
        self.logger.info("Receive Signal {0}".format(signum))
        self.logger.info("Stop Singing")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--end", help="simulation end datetime yyyy-MM-dd HH:mm:ss ex)2020-02-10T17:50:37", default=None)
    parser.add_argument("--count", help="simulation tick count", default=None)
    args = parser.parse_args()

    simulator = SmtmSimulator(args.end, args.count)
    simulator.main()
