# Point class represents a single point in a plane, described by its x and y coordinates
from helpers.utils import collections
from helpers.draw import turtle


class Point(collections.namedtuple('PointBase', ['x', 'y'])):

    def print(self, sep='', end=''):
        print('(' + str(self.x) + ', ' + str(self.y) + ')', sep=sep, end=end)

    def draw(self):
        turtle.setpos(self.x, self.y)
        turtle.down()
        turtle.dot()