__author__ = 'nncsang'

#import urllib2
import socket
import GlobalVariable

from Logger import Logger
from HTMLParser import HTMLParser
from DataStructures.League import League
from DataStructures.Team import Team
import json
from JSONDatabase import JSONDatabase

class LiveScoreParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.data = []

        self.meetData = False

    def handle_starttag(self, tag, attrs):
        if (('data-name', 'england-premier-league-0') in attrs and ('data-type', 'league-table')):
            self.meetData = True

        if (self.meetData == True):
            self.data.append((tag, attrs))

    def handle_endtag(self, tag):
        if (self.meetData == True):
            self.data.append((tag, None))

    def handle_data(self, data):
        if (self.meetData == True):
            self.data.append((data))

    def process(self):
        dataSize = len(self.data)
        leagues = []
        # for i, value in enumerate(self.data):
        #     print '%d: %s' % (i, value)

        i = 0;
        while (i < dataSize):
            if (type(self.data[i]) is tuple and self.data[i][0] == 'a' and self.data[i][1] != None \
                        and ('class', 'league-name') in self.data[i][1]):

                i += 1
                leagues.append(League(self.data[i]))
                Logger.notify(Logger.INFO, 'Got table of ' + self.data[i]);

                while(i < dataSize):

                    if (type(self.data[i]) is tuple and self.data[i][0] == 'a' and self.data[i][1] != None \
                        and ('class', 'league-name') in self.data[i][1]):
                        i -= 1
                        break

                    if (type(self.data[i]) is tuple):
                        if (self.data[i][0] == 'div' and self.data[i][1] != None):
                            if (('data-type', 'team-data') in self.data[i][1]):
                                i += 1;

                                count = 0;
                                team = Team()
                                while (i < dataSize and count != 4):
                                    # print ("%s %d %s") % (type(self.data[i]), len(self.data[i]), self.data[i])
                                    if (type(self.data[i]) is str and self.data[i] != ' '):
                                        #print self.data[i]
                                        count += 1

                                        if (count == 1):
                                            team.rank = self.data[i]
                                        elif count == 2:
                                            team.name = self.data[i]
                                        elif count == 3:
                                            team.played_match = self.data[i]
                                        elif count == 4:
                                            team.point = self.data[i]


                                    i += 1;

                                #print '----------'
                                leagues[-1].add(team)

                    i += 1

            i += 1
        return leagues

class LiveScoreScraper:
    url = 'http://www.livescore.com/'

    @staticmethod
    def scrap(url):
        try:
            Logger.notify(Logger.INFO, 'Starting to FETCH html from http://www.livescore.com/');
            # response = urllib2.urlopen('http://' + url + '/')
            # html = response.read()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((GlobalVariable.TABLE_URL , 80))
            s.sendall("GET http://"+ GlobalVariable.TABLE_URL + " HTTP/1.0\n\n")

            response = [s.recv(2048)]
            while response[-1]:
                response.append(s.recv(2048))

            html = ''.join(response)
            s.close()

            Logger.notify(Logger.INFO, 'Finished fetching html from http://www.livescore.com/');
            Logger.notify(Logger.INFO, 'Starting to PARSE data from http://www.livescore.com/');
            parser = LiveScoreParser()
            parser.feed(html)
            leagues = parser.process()
            Logger.notify(Logger.INFO, 'Finished parsing data from http://www.livescore.com/');
            json_data = []
            for league in leagues:
                json_data.append({'league': {'name': league.name, 'teams': []}})

                for team in league.teams:
                    json_data[-1]['league']['teams'].append({'rank': team.rank, 'name': team.name, \
                                                   'played_match': team.played_match, 'point': team.point})


            return json.dumps(json_data);

        except socket.error as e:
            if hasattr(e, 'reason'):
                Logger.notify(Logger.ERROR, r'We failed to reach http://www.livescore.com/.')
                Logger.log('We failed to reach a server: ' + e.reason)
            elif hasattr(e, 'code'):
                Logger.notify(Logger.ERROR, r'http://www.livescore.com/ couldn\'t fulfill the request.')
                Logger.log('The server couldn\'t fulfill the request.' + e.code)
        else:
            pass
