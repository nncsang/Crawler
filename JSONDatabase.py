__author__ = 'nncsang'

import GlobalVariable
import json

from DataStructures.League import League
from DataStructures.Team import Team
from Logger import Logger
from Database import Database

class JSONDatabase(Database):

    def write(self, data):
        Logger.notify(Logger.INFO, "Opening database")
        db = open(GlobalVariable.LEAGUE_DATABSE, 'w+');

        leagues = []
        for league_obj in json.loads(data):

            league_obj = league_obj['league']
            league = League(league_obj['name'])

            Logger.notify(Logger.INFO, "Storing " + league_obj['name'])

            for team_obj in league_obj['teams']:
                team = Team(team_obj['name'], team_obj['rank'], team_obj['goaldiff'], team_obj['point']);
                league.teams.append(team)
                Logger.notify(Logger.INFO, "Storing record \"" + str(team) + '\"')

            leagues.append(league)

        db.write(data)
        Logger.notify(Logger.INFO, "Closing database")
        db.close()

    def read(self):
        db = open(GlobalVariable.LEAGUE_DATABSE, 'r');
        data = json.load(db)
        db.close()

        leagues = []
        for league_obj in data:

            league_obj = league_obj['league']
            league = League(league_obj['name'])

            for team_obj in league_obj['teams']:
                team = Team(team_obj['name'], team_obj['rank'], team_obj['goaldiff'], team_obj['point']);
                league.teams.append(team)

            leagues.append(league)

        return leagues;