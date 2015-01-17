__author__ = 'nncsang'

import socket
import GlobalVariable
from Scapper.LiveScoreScraper import LiveScoreScraper

# cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# cli.connect((GlobalVariable.HOST, GlobalVariable.PORT))

LiveScoreScraper.scrap();
# print "Connected!"
#
# while True:
#     cmd=raw_input("Input:  ")
#
#     if len(cmd)==0:
#         break
#     cli.send(cmd)
#     ans = cli.recv(1024)
#     print "Output: %s" % ans
#
# cli.close()