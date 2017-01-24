# Edge class represents a single edge in a plane, described by its tail and head points
from helpers.utils import eucledian_sqrd_distance
from helpers.draw import turtle
from structures.point import Point


class Edge:
    def __init__(self, tail=Point(x=0, y=0), head=Point(x=0, y=0)):
        self.tail = tail
        self.head = head
        self.incident_dots = []

    def __eq__(self, other):
        return True if self.tail == other.tail and self.head == other.head else False

    def flat_eq(self, other):
        return True if self == other or self == Edge(other.head, other.tail) else False

    def get_weight(self):
        return eucledian_sqrd_distance(self.tail, self.head)

    def print(self, sep='', end=''):
        print('(' + str(self.tail) + ', ' + str(self.head) + ')', sep=sep, end=end)

    def draw(self):
        turtle.up();
        turtle.setpos(self.tail)
        turtle.down()
        turtle.setpos(self.head)
        turtle.up()
