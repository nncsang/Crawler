__author__ = 'nncsang'
class Team:
    def __init__(self, name = None, rank = None, played_match = None, point = None):
        self.name = name;
        self.rank = rank;
        self.played_match = played_match;
        self.point = point

    def __str__(self):
        return ('%s - %s - played match: %s - point: %s') % (self.rank, self.name, self.played_match, self.point)
