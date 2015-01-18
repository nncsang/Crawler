__author__ = 'nncsang'

class League:
    def __init__(self, name):
        self.name = name;
        self.teams = [];

    def add(self, team):
        self.teams.append(team)

    def __str__(self):
        return self.name + '\n' + '\n'.join([str(team) for team in self.teams]) + '\n' + '*****************' + '\n'
