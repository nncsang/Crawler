__author__ = 'nncsang'
class Team:
    def __init__(self, name = None, rank = None, goaldiff = None, point = None):
        self.name = name;
        self.rank = rank;
        self.goaldiff = goaldiff;
        self.point = point

    def __str__(self):
        return ('%s - %s - goaldiff: %s - point: %s') % (self.rank, self.name, self.goaldiff, self.point)
