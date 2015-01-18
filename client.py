__author__ = 'nncsang'

import socket
import GlobalVariable
from Logger import Logger
from DataStructures.Message import Message
from Scapper.LiveScoreScraper import LiveScoreScraper

Logger.notify(Logger.INFO, 'Starting working')

try:
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((GlobalVariable.HOST, GlobalVariable.PORT))
except socket.error:
    Logger.notify(Logger.ERROR, 'Can not connect to server!!! Make sure you\'ve already started the server!!')
    Logger.notify(Logger.INFO, 'Program exited')
    Logger.log('Can not connect to server!!!')
    exit();

Logger.notify(Logger.INFO, 'Starting to SCRAP tables')
json_data = LiveScoreScraper.scrap();
Logger.notify(Logger.INFO, 'Finished scraping tables')
Logger.notify(Logger.INFO, 'Connected to server on ' + GlobalVariable.HOST + ':' + str(GlobalVariable.PORT))
Logger.notify(Logger.INFO, 'Sending UPDATE request to server')

try:
    request = Message("UPDATE", [], json_data)
    cli.send(str(request))
except socket.error:
    Logger.notify(Logger.ERROR, 'Error when sending UPDATE request to server');
    Logger.log('Error when sending UPDATE request to server. The request is: ' + str(request))

Logger.notify(Logger.INFO, 'UPDATE request is sent')
Logger.notify(Logger.INFO, 'Waiting for confirmation')
try:
    ans = cli.recv(1024)
except:
    Logger.log('Error when waiting for confirmation from server')
    Logger.notify(Logger.ERROR, 'Error when waiting for confirmation from server');

Logger.notify(Logger.INFO, 'Got the answer from server: ' + ans)
Logger.notify(Logger.INFO, 'Program exited successfully')
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