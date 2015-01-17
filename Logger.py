__author__ = 'nncsang'

import logging
import GlobalVariable

class Logger:

    logging.basicConfig(filename = GlobalVariable.LOG_FILE, format = '%(levelname)s:%(message)s', level = logging.DEBUG)

    @classmethod
    def log(self, e):
        logging.error(str(e))