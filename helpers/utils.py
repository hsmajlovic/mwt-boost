import collections
import copy
import math
import random

from operator import attrgetter


def ccw(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def eucledian_sqrd_distance(p1, p2):
    return (p2.y - p1.y) * (p2.y - p1.y) + (p2.x - p1.x) * (p2.x - p1.x)


def sign(value):
    if value > 0:
        return 1
    if value == 0:
        return 0
    if value < 0:
        return -1


def do_cycle_left(l, offset=1):
    n = len(l)
    l[:n - offset], l[n - offset:] = l[offset:], l[:offset]


def are_cyclic_eq(l1, l2):
    temp_list = copy.copy(l1)
    while True:
        do_cycle_left(temp_list)
        if temp_list == l2:
            return True
        if temp_list == l1:
            return False
    return


def is_cyclic_inside_dict(dictionary, l):
    offset = 0
    temp_list = copy.copy(l)
    while True:
        do_cycle_left(temp_list)
        offset += 1
        if tuple(temp_list) in dictionary:
            return offset % len(temp_list), tuple(temp_list)
        if temp_list == l:
            return None
    return


def count_collisions(l):
    counter = 0
    for elem in l:
        if elem in [x for x in l if id(x) != id(elem)]:
            counter += 1
    return counter
