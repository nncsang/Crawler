__author__ = 'nncsang'

import logging
import GlobalVariable
import time
class Logger:

    logging.basicConfig(filename = GlobalVariable.LOG_FILE, format = '%(levelname)s:%(message)s', level = logging.DEBUG)

    INFO = 0
    WARN = 1;
    ERROR = 2
    @staticmethod
    def log(e):
        logging.error(' ' + time.strftime("%d/%m/%Y") + ' ' +  time.strftime("%I:%M:%S - ") + str(e))

    @classmethod
    def notify(self, type, message):
        time_now = time.strftime("%d/%m/%Y") + ' ' +  time.strftime("%I:%M:%S") + ' ';
        if (type == self.INFO):
            print(time_now + 'INFO:\t' + message)

        if (type == self.WARN):
            print(time_now + 'WARN:\t' + message)

        if (type == self.ERROR):
            print(time_now + 'ERROR:\t' + message)
