import math
from random import choice

from helpers import utils
from libraries import cg_lib
from solutions.exhaustive_search import return_left_hull, return_right_hull, return_new_hull
from structures.edge import Edge

fct_edges = []
gct_edges = []
rct_edges = []
characteristic = []
valid_dots_mapping = {}
reconstructed_map = {'fct': False, 'gct': False, 'rct': False}


def get_fct_edges(reconstructed=False, dots=None, hull=None):
    if reconstructed and not reconstructed_map['fct']:
        cg_lib.reconstruct_incident_dots(dots, fct_edges, hull)
    reconstructed_map['fct'] = True
    return fct_edges


def get_gct_edges(reconstructed=False, dots=None, hull=None):
    if reconstructed and not reconstructed_map['gct']:
        cg_lib.reconstruct_incident_dots(dots, gct_edges, hull)
        reconstructed_map['gct'] = True
    return gct_edges


def get_rct_edges(reconstructed=False, dots=None, hull=None):
    if reconstructed and not reconstructed_map['rct']:
        cg_lib.reconstruct_incident_dots(dots, rct_edges, hull)
        reconstructed_map['rct'] = True
    return rct_edges


def get_characteristic():
    return characteristic


def calculate_triangulation_weight(edges):
    weight = 0
    for edge in edges:
        weight += edge.get_weight()
    return weight


def find_valid_dot(dots, tail_dot, head_dot, hull):
    for dot in dots:
        if utils.ccw(tail_dot, head_dot, dot) < 0 and \
           cg_lib.form_empty_triangle(dots, tail_dot, head_dot, dot) and \
           cg_lib.is_inside_polygon(hull, dot) and \
           not cg_lib.does_intersect_polygon(hull, tail_dot, dot) and \
           not cg_lib.does_intersect_polygon(hull, head_dot, dot):
            return dot
    return None


def find_greedy_dot(dots, tail_dot, head_dot, hull):
    greedy_dot = None
    temp_weight = math.inf
    for dot in dots:
        if utils.ccw(tail_dot, head_dot, dot) < 0 and \
           cg_lib.form_empty_triangle(dots, tail_dot, head_dot, dot) and \
           cg_lib.is_inside_polygon(hull, dot) and \
           not cg_lib.does_intersect_polygon(hull, tail_dot, dot) and \
           not cg_lib.does_intersect_polygon(hull, head_dot, dot) and \
           (utils.eucledian_sqrd_distance(tail_dot, dot) + utils.eucledian_sqrd_distance(dot, head_dot)) < temp_weight:
            greedy_dot = dot
            temp_weight = (utils.eucledian_sqrd_distance(tail_dot, dot) + utils.eucledian_sqrd_distance(dot, head_dot))
    return greedy_dot


def find_random_dot(dots, tail_dot, head_dot, hull):
    hull_tuple = tuple(hull)
    if tuple(hull_tuple) in valid_dots_mapping:
        return choice(valid_dots_mapping[hull_tuple])
    valid_dots = []
    for dot in dots:
        if utils.ccw(tail_dot, head_dot, dot) < 0 and \
           cg_lib.form_empty_triangle(dots, tail_dot, head_dot, dot) and \
           cg_lib.is_inside_polygon(hull, dot) and \
           not cg_lib.does_intersect_polygon(hull, tail_dot, dot) and \
           not cg_lib.does_intersect_polygon(hull, head_dot, dot):
            valid_dots.append(dot)
    valid_dots_mapping[hull_tuple] = valid_dots
    return choice(valid_dots)


def first_choice_triangulation(dots, hull):
    global fct_edges

    if len(hull) < 3:
        print("Major error occurred. Hull invalid.")
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        fct_edges.append(Edge(hull[0], hull[1]))
        fct_edges.append(Edge(hull[1], hull[2]))
        return utils.eucledian_sqrd_distance(hull[0], hull[1]) + utils.eucledian_sqrd_distance(hull[1], hull[2])
    v_dot = find_valid_dot(dots, hull[0], hull[1], hull)
    if not v_dot:
        print("Major error occurred. No valid dots.")
    new_value = utils.eucledian_sqrd_distance(hull[0], hull[1])
    if v_dot in hull:
        if len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots):
            fct_edges.append(Edge(hull[0 if v_dot == hull[2] else 1], v_dot))
            new_value = utils.eucledian_sqrd_distance(hull[0 if v_dot == hull[2] else 1], v_dot)
        else:
            if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                new_value += utils.eucledian_sqrd_distance(hull[1], v_dot)
            if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                new_value += utils.eucledian_sqrd_distance(hull[0], v_dot)
            if v_dot == hull[2]:
                new_value = 0
            elif v_dot == hull[len(hull) - 1]:
                new_value = 0
            if new_value != 0:
                fct_edges.append(Edge(hull[0], hull[1]))
                if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                    fct_edges.append(Edge(hull[1], v_dot))
                if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                    fct_edges.append(Edge(hull[0], v_dot))
        new_value += first_choice_triangulation(dots, return_right_hull(v_dot, hull))
        new_value += first_choice_triangulation(dots, return_left_hull(v_dot, hull))
    else:
        fct_edges.append(Edge(hull[0], hull[1]))
        new_value += first_choice_triangulation(dots, return_new_hull(v_dot, hull))
    return new_value


def greedy_choice_triangulation(dots, hull):
    global gct_edges

    if len(hull) < 3:
        print("Major error occurred. Hull invalid.")
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        gct_edges.append(Edge(hull[0], hull[1]))
        gct_edges.append(Edge(hull[1], hull[2]))
        return utils.eucledian_sqrd_distance(hull[0], hull[1]) + utils.eucledian_sqrd_distance(hull[1], hull[2])
    v_dot = find_greedy_dot(dots, hull[0], hull[1], hull)
    if not v_dot:
        print("Major error occurred. No valid dots.")
    new_value = utils.eucledian_sqrd_distance(hull[0], hull[1])
    if v_dot in hull:
        if len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots):
            gct_edges.append(Edge(hull[0 if v_dot == hull[2] else 1], v_dot))
            new_value = utils.eucledian_sqrd_distance(hull[0 if v_dot == hull[2] else 1], v_dot)
        else:
            if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                new_value += utils.eucledian_sqrd_distance(hull[1], v_dot)
            if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                new_value += utils.eucledian_sqrd_distance(hull[0], v_dot)
            if v_dot == hull[2]:
                new_value = 0
            elif v_dot == hull[len(hull) - 1]:
                new_value = 0
            if new_value != 0:
                gct_edges.append(Edge(hull[0], hull[1]))
                if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                    gct_edges.append(Edge(hull[1], v_dot))
                if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                    gct_edges.append(Edge(hull[0], v_dot))
        new_value += greedy_choice_triangulation(dots, return_right_hull(v_dot, hull))
        new_value += greedy_choice_triangulation(dots, return_left_hull(v_dot, hull))
    else:
        gct_edges.append(Edge(hull[0], hull[1]))
        new_value += greedy_choice_triangulation(dots, return_new_hull(v_dot, hull))
    return new_value


def random_choice_lite_triangulation(dots, hull):
    global characteristic

    relevant_index = len(characteristic)
    if len(hull) < 3:
        print("Major error occurred. Hull invalid.")
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        characteristic.append({'hull': hull, 'final': True})
        return utils.eucledian_sqrd_distance(hull[0], hull[1]) + utils.eucledian_sqrd_distance(hull[1], hull[2])
    else:
        characteristic.append({'hull': hull, 'final': False})
    v_dot = find_random_dot(dots, hull[0], hull[1], hull)
    if not v_dot:
        print("Major error occurred. No valid dots.")
    new_value = utils.eucledian_sqrd_distance(hull[0], hull[1])
    if v_dot in hull:
        if len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots):
            new_value = utils.eucledian_sqrd_distance(hull[0 if v_dot == hull[2] else 1], v_dot)
        else:
            if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                new_value += utils.eucledian_sqrd_distance(hull[1], v_dot)
            if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                new_value += utils.eucledian_sqrd_distance(hull[0], v_dot)
            if v_dot == hull[2]:
                new_value = 0
            elif v_dot == hull[len(hull) - 1]:
                new_value = 0
        new_value += random_choice_lite_triangulation(dots, return_right_hull(v_dot, hull))
        new_value += random_choice_lite_triangulation(dots, return_left_hull(v_dot, hull))
    else:
        new_value += random_choice_lite_triangulation(dots, return_new_hull(v_dot, hull))
    characteristic[relevant_index]['weight'] = new_value
    characteristic[relevant_index]['length'] = len(characteristic) - relevant_index
    return new_value


def random_choice_triangulation(dots, hull):
    global rct_edges
    global characteristic

    relevant_index = len(characteristic)
    if len(hull) < 3:
        print("Major error occurred. Hull invalid.")
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        characteristic.append({'hull': hull, 'final': True})
        rct_edges.append(Edge(hull[0], hull[1]))
        rct_edges.append(Edge(hull[1], hull[2]))
        return utils.eucledian_sqrd_distance(hull[0], hull[1]) + utils.eucledian_sqrd_distance(hull[1], hull[2])
    else:
        characteristic.append({'hull': hull, 'final': False})
    v_dot = find_random_dot(dots, hull[0], hull[1], hull)
    if not v_dot:
        print("Major error occurred. No valid dots.")
    new_value = utils.eucledian_sqrd_distance(hull[0], hull[1])
    if v_dot in hull:
        if len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots):
            rct_edges.append(Edge(hull[0 if v_dot == hull[2] else 1], v_dot))
            new_value = utils.eucledian_sqrd_distance(hull[0 if v_dot == hull[2] else 1], v_dot)
        else:
            if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                new_value += utils.eucledian_sqrd_distance(hull[1], v_dot)
            if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                new_value += utils.eucledian_sqrd_distance(hull[0], v_dot)
            if v_dot == hull[2]:
                new_value = 0
            elif v_dot == hull[len(hull) - 1]:
                new_value = 0
            if new_value != 0:
                rct_edges.append(Edge(hull[0], hull[1]))
                if v_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                    rct_edges.append(Edge(hull[1], v_dot))
                if v_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                    rct_edges.append(Edge(hull[0], v_dot))
        new_value += random_choice_triangulation(dots, return_right_hull(v_dot, hull))
        new_value += random_choice_triangulation(dots, return_left_hull(v_dot, hull))
    else:
        rct_edges.append(Edge(hull[0], hull[1]))
        new_value += random_choice_triangulation(dots, return_new_hull(v_dot, hull))
    characteristic[relevant_index]['weight'] = new_value
    characteristic[relevant_index]['length'] = len(characteristic) - relevant_index
    return new_value


def get_fct(dots, hull):
    global fct_edges
    global reconstructed_map
    reconstructed_map['fct'] = False
    fct_edges = []
    return first_choice_triangulation(dots, hull)


def get_gct(dots, hull):
    global gct_edges
    global reconstructed_map
    reconstructed_map['gct'] = False
    gct_edges = []
    return greedy_choice_triangulation(dots, hull)


def get_rct(dots, hull, lite=True):
    global rct_edges
    global characteristic
    global reconstructed_map
    reconstructed_map['rct'] = False
    rct_edges = []
    characteristic = []
    return random_choice_lite_triangulation(dots, hull) if lite else random_choice_triangulation(dots, hull)


def get_seed_triangulations(dots, hull):
    global fct_edges
    global gct_edges

    fct_edges = []
    gct_edges = []
    return {
        'first_choice':  first_choice_triangulation(dots, hull),
        'greedy_choice': greedy_choice_triangulation(dots, hull)
    }
