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
        if (type == self.INFO):
            print('INFO:\t' + message)

        if (type == self.WARN):
            print('WARN:\t' + message)

        if (type == self.ERROR):
            print('ERROR:\t' + message)
