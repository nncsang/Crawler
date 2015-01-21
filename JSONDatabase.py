__author__ = 'nncsang'

import GlobalVariable
import json

from DataStructures.League import League
from DataStructures.Team import Team
from Logger import Logger
from Database import Database

class JSONDatabase(Database):

    def write(self, data):
        try:
            Logger.notify(Logger.INFO, "Opening database")
            db = open(GlobalVariable.LEAGUE_DATABSE, 'w+');

            leagues = []
            for league_obj in json.loads(data):

                league_obj = league_obj['league']
                league = League(league_obj['name'])

                Logger.notify(Logger.INFO, "Storing " + league_obj['name'])

                for team_obj in league_obj['teams']:
                    team = Team(team_obj['name'], team_obj['rank'], team_obj['played_match'], team_obj['point']);
                    league.teams.append(team)
                    Logger.notify(Logger.INFO, "Storing record \"" + str(team) + '\"')

                leagues.append(league)

            db.write(data)
            db.flush()
            Logger.notify(Logger.INFO, "Closing database")
            db.close()
            return True
        except:
            return None

    def read(self):
        try:
            Logger.notify(Logger.INFO, "Opening database")
            db = open(GlobalVariable.LEAGUE_DATABSE, 'r');
            data = db.read();
            Logger.notify(Logger.INFO, "Reading records")
            db.close()

            Logger.notify(Logger.INFO, "Closing database")
            return data;
        except:
            return None