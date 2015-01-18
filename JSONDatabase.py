__author__ = 'nncsang'

import GlobalVariable
import json
from DataStructures.League import League
from DataStructures.Team import Team

class JSONDatabase:

    @staticmethod
    def write(data):
        db = open(GlobalVariable.LEAGUE_DATABSE, 'w+');
        db.write(data)
        db.close()

    @staticmethod
    def read():
        db = open(GlobalVariable.LEAGUE_DATABSE, 'r');
        data = json.load(db)
        db.close()


        leagues = []
        for league_obj in data:
            league_obj = league_obj['league']
            league = League(league_obj['name'])

            for team_obj in league_obj['teams']:
                league.teams.append(Team(team_obj['name'], team_obj['rank'], team_obj['goaldiff'], team_obj['point']))

            leagues.append(league)

        return leagues;