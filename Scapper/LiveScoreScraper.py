__author__ = 'nncsang'

import urllib2
import Logger
from HTMLParser import HTMLParser
from DataStructures.League import League
from DataStructures.Team import Team
import json
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
                count = 0

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
                                            team.goaldiff = self.data[i]
                                        elif count == 4:
                                            team.point = self.data[i]


                                    i += 1;

                                #print '----------'
                                leagues[-1].add(team)

                    i += 1

            i += 1
        return leagues




class LiveScoreScaper:
    url = 'http://www.livescore.com/'

    @staticmethod
    def scap():
        try:
            response = urllib2.urlopen('http://www.livescore.com/')
            html = response.read()
            parser = LiveScoreParser()
            parser.feed(html)
            leagues = parser.process()
            print json.JSONEncoder.encode(leagues)
            for league in leagues:
                print league

        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                Logger.log('We failed to reach a server: ' + e.reason)
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                Logger.log('The server couldn\'t fulfill the request.' + e.code)
        else:
            pass

        #print(html)