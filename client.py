__author__ = 'nncsang'

import socket
import GlobalVariable

from Logger import Logger
from DataStructures.Message import Message
from Scapper.LiveScoreScraper import LiveScoreScraper
from DataStructures.Buffer import Buffer

import json

def display_ranking_tables(data):
    data = json.loads(data)
    print('\t'+ '*' * 55)
    for league_obj in data:
        league_obj = league_obj['league']

        print('\t' + league_obj['name'])
        print('\t\t' + "\t\t".join(("Rank", "Name", "Played Match", "Point")))
        for team_obj in league_obj['teams']:
            print('\t\t' + "\t".join((team_obj['rank'], team_obj['name'], team_obj['played_match'], team_obj['point'])))
        print('\t'+ '*' * 55 + '\n')


Logger.notify(Logger.INFO, 'Starting working')

Logger.notify(Logger.INFO, 'Starting to SCRAP tables')
json_data = LiveScoreScraper.scrap(GlobalVariable.TABLE_URL);
Logger.notify(Logger.INFO, 'Finished scraping tables')
Logger.notify(Logger.INFO, 'Connected to server on ' + GlobalVariable.HOST + ':' + str(GlobalVariable.PORT))
Logger.notify(Logger.INFO, 'Sending LOGIN request to server')

try:
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((GlobalVariable.HOST, GlobalVariable.PORT))
except socket.error, e:
    Logger.notify(Logger.ERROR, 'Can not connect to server!!! Make sure you\'ve already started the server!!')
    Logger.notify(Logger.INFO, 'Program exited')
    Logger.log('Can not connect to server!!!. Error: ' + str(e))
    exit();

buffer = Buffer()

previous_message = None
try:
    request = Message("LOGIN", [], "nncsang")
    cli.send(str(request))
    Logger.notify(Logger.INFO, 'LOGIN request is sent')
    Logger.notify(Logger.INFO, 'Waiting for response')
    previous_message = request

    while(True):
        ans = cli.recv(1024)
        buffer.updateBuffer(ans)

        while(True):
            message = buffer.parse()

            if (message == None):
                break

            if (previous_message.type == "LOGIN" and message.type == "ACK"):
                request = Message("PASS", ["nncsang"], "1234")
                cli.send(str(request))
                Logger.notify(Logger.INFO, 'Response for LOGIN: ' + message.payload)
                Logger.notify(Logger.INFO, 'PASS request is sent')
                previous_message = request
                continue

            if (message.type == "ERR"):
                Logger.notify(Logger.INFO, 'Error for ' + previous_message.type + ': ' + message.payload)
                Logger.notify(Logger.INFO, 'Program exiting with error')
                exit()
                continue


            if (message.type == "ACK"):

                if (previous_message.type == "UPDATE"):
                    Logger.notify(Logger.INFO, 'Server said UPDATE request is OK')
                    request = Message("SELECT", ["ALL"], '')
                    cli.send(str(request))
                    Logger.notify(Logger.INFO, 'SELECT request is sent')
                    Logger.notify(Logger.INFO, 'Waiting for response')
                    previous_message = request;
                    continue

                if (previous_message.type == "CLOSE"):
                    Logger.notify(Logger.INFO, 'Server said CLOSE request is accepted')
                    Logger.notify(Logger.INFO, 'Program exited')
                    exit()
                    continue

                if (previous_message.type == "PASS"):
                    Logger.notify(Logger.INFO, 'Response for PASS: ' + message.payload)
                    request = Message("UPDATE", [], json_data)
                    cli.send(str(request))
                    Logger.notify(Logger.INFO, 'UPDATE request is sent')
                    Logger.notify(Logger.INFO, 'Waiting for response')
                    previous_message = request
                    continue

            if (message.type == "RES_SELECT"):
                display_ranking_tables(message.payload)
                request = Message("CLOSE", [], '')
                previous_message = request
                cli.send(str(request))
                Logger.notify(Logger.INFO, 'CLOSE request is sent')
                Logger.notify(Logger.INFO, 'Waiting for confirmation')
                continue


except socket.error, e:

    if (request.type == "UPDATE"):
        Logger.notify(Logger.ERROR, 'Error when sending UPDATE request to server');
        Logger.log('Error when sending UPDATE request to server. The request is: ' + str(request) + " .Error: " + str(e))

    if (request.type == "CLOSE"):
        Logger.notify(Logger.ERROR, 'Error when sending CLOSE connection request to server');
        Logger.log('Error when sending UPDATE request to server. The request is: ' + str(request) + " .Error: " + str(e))
        Logger.notify(Logger.INFO, 'Program exited')

    exit()




