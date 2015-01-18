__author__ = 'nncsang'

from DataStructures.Message import Message

class Buffer:
    def __init__(self, buffer = ''):
        self.buffer = buffer

    def parse(self):
        m = Message();
        consumed = m.parse(self.buffer)
        self.buffer = self.buffer[consumed:]
        return m if consumed > 0 else None

    def updateBuffer(self, buffer):
        self.buffer += buffer