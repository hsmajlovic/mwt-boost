import math

from helpers.utils import *
from libraries import cg_lib
from structures.edge import Edge

global_temporary_mwt_weight = math.inf
hull_mwt_values = dict()

# Begin of debugging related
testing_dots_order = dict()


def get_triangulation_from_dots_order(dots, dots_order, hull, triangulation_edges=[]):
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        if Edge(hull[0], hull[1]) not in triangulation_edges:
            triangulation_edges.append(Edge(hull[0], hull[1]))
        if Edge(hull[1], hull[2]) not in triangulation_edges:
            triangulation_edges.append(Edge(hull[1], hull[2]))
        return
    offset_and_tuple = is_cyclic_inside_dict(dots_order, hull)
    if offset_and_tuple:
        new_dot = dots_order[offset_and_tuple[1]]
        if new_dot in hull:
            if len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots):
                if Edge(hull[0 if new_dot == hull[2] else 1], new_dot) not in triangulation_edges:
                    triangulation_edges.append(Edge(hull[0 if new_dot == hull[2] else 1], new_dot))
            elif new_dot != hull[2 and new_dot != hull[len(hull) - 1]]:
                    if Edge(hull[0], hull[1]) not in triangulation_edges:
                        triangulation_edges.append(Edge(hull[0], hull[1]))
                    if new_dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                        if Edge(hull[1], new_dot) not in triangulation_edges:
                            triangulation_edges.append(Edge(hull[1], new_dot))
                    if new_dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2],
                                                                                   hull[len(hull) - 1]):
                        if Edge(hull[0], new_dot) not in triangulation_edges:
                            triangulation_edges.append(Edge(hull[0], new_dot))
            get_triangulation_from_dots_order(dots, dots_order, return_right_hull(new_dot, hull), triangulation_edges)
            get_triangulation_from_dots_order(dots, dots_order, return_left_hull(new_dot, hull), triangulation_edges)
        else:
            if Edge(hull[0], hull[1]) not in triangulation_edges:
                triangulation_edges.append(Edge(hull[0], hull[1]))
            get_triangulation_from_dots_order(dots, dots_order, return_new_hull(new_dot, hull), triangulation_edges)
    else:
        return
    return triangulation_edges


def get_testing_dots_order():
    return testing_dots_order
# End of debugging related


def valid_dots(dots, tail_dot, head_dot, hull):
    temp_valid_dots = []
    for dot in dots:
        if ccw(tail_dot, head_dot, dot) < 0 and \
                cg_lib.form_empty_triangle(dots, tail_dot, head_dot, dot) and \
                cg_lib.is_inside_polygon(hull, dot) and \
                not cg_lib.does_intersect_polygon(hull, tail_dot, dot) and \
                not cg_lib.does_intersect_polygon(hull, head_dot, dot):
            temp_valid_dots.append(dot)
    return temp_valid_dots


def return_right_hull(dot, hull):
    temp_hull = []
    start_dot_index = hull.index(dot)
    while start_dot_index != 0 and start_dot_index != 1:
        temp_hull.append(hull[start_dot_index])
        start_dot_index = (start_dot_index + 1) % len(hull)
    temp_hull.append(hull[start_dot_index])
    if start_dot_index == 0 and len(temp_hull) == 2:
        temp_hull.append(hull[1])
    if not cg_lib.is_polygon_clockwise(temp_hull):
        temp_hull.reverse()
    return temp_hull


def return_left_hull(dot, hull):
    temp_hull = []
    start_dot_index = hull.index(dot)
    while start_dot_index != 0 and start_dot_index != 1:
        temp_hull.append(hull[start_dot_index])
        start_dot_index = len(hull) - 1 if start_dot_index == 0 else start_dot_index - 1
    temp_hull.append(hull[start_dot_index])
    if start_dot_index == 1 and len(temp_hull) == 2:
        temp_hull.append(hull[0])
    temp_hull.reverse()
    if not cg_lib.is_polygon_clockwise(temp_hull):
        temp_hull.reverse()
    return temp_hull


def return_new_hull(dot, hull):
    new_hull = copy.copy(hull)
    new_hull.insert(1, dot)
    if not cg_lib.is_polygon_clockwise(new_hull):
        new_hull.reverse()
    return new_hull


def return_mwt_weight(dots, hull, value=0):
    # # Begin of debugging related
    # global testing_dots_order
    # # End of debugging related

    # # Begin of Branch and Bound related
    # global global_temporary_mwt_weight
    # if value > global_temporary_mwt_weight:
    #     return math.inf
    # # End of Branch and Bound related

    # Begin of memoisation related
    global hull_mwt_values
    offset_and_tuple = is_cyclic_inside_dict(hull_mwt_values, hull)
    if offset_and_tuple is not None and len(hull) > 3:
        return hull_mwt_values[offset_and_tuple[1]]
    # End of memoisation related

    temporary_mwt_weight = math.inf
    if len(hull) < 3:
        print("Major error occurred. Hull invalid.")
    if len(hull) == 3 and cg_lib.form_empty_triangle(dots, hull[0], hull[1], hull[2]):
        return eucledian_sqrd_distance(hull[0], hull[1]) + eucledian_sqrd_distance(hull[1], hull[2])
    quad_hull = (len(hull) == 4 and cg_lib.is_empty_polygon(hull, dots))
    v_dots = valid_dots(dots, hull[0], hull[1], hull)
    if len(v_dots) == 0:
        print("Major error occurred. No valid dots.")
    for dot in v_dots:
        if quad_hull:
            new_value = eucledian_sqrd_distance(hull[0 if dot == hull[2] else 1], dot)
        else:
            new_value = eucledian_sqrd_distance(hull[0], hull[1])
        if dot in hull:
            if not quad_hull:
                if dot == hull[3] and cg_lib.form_empty_triangle(dots, hull[1], hull[2], hull[3]):
                    new_value += eucledian_sqrd_distance(hull[1], dot)
                if dot == hull[len(hull) - 2] and cg_lib.form_empty_triangle(dots, hull[0], hull[len(hull) - 2], hull[len(hull) - 1]):
                    new_value += eucledian_sqrd_distance(hull[0], dot)
                if dot == hull[2]:
                    new_value = 0
                if dot == hull[len(hull) - 1]:
                    new_value = 0
            new_value += return_mwt_weight(dots, return_right_hull(dot, hull), value + new_value)
            new_value += return_mwt_weight(dots, return_left_hull(dot, hull), value + new_value)
        else:
            new_value += return_mwt_weight(dots, return_new_hull(dot, hull), value + new_value)
        if new_value < temporary_mwt_weight:
            # # Begin of debugging related
            # relevant_offset_and_tuple = is_cyclic_inside_dict(testing_dots_order, hull)
            # testing_dots_order[relevant_offset_and_tuple[1] if relevant_offset_and_tuple is not None else tuple(hull)] = dot
            # # End of debugging related
            temporary_mwt_weight = new_value
        # # Begin of Branch and Bound related
        # if value == 0:
        #     global_temporary_mwt_weight = temporary_mwt_weight if temporary_mwt_weight < global_temporary_mwt_weight \
        #         else global_temporary_mwt_weight
        # # End of Branch and Bound related

    # Begin of memoisation related
    hull_mwt_values[tuple(hull)] = temporary_mwt_weight
    # End of memoisation related

    return temporary_mwt_weight


def do_exhaustive_search(dots, hull):
    # # Begin of Branch and Bound related
    # global global_temporary_mwt_weight
    # global_temporary_mwt_weight = st_lib.calculate_triangulation_weight(st_lib.get_gct_edges()) if \
    #     len(st_lib.get_gct_edges()) > 0 else st_lib.get_seed_triangulations(dots, hull)['greedy_choice']
    # # End of Branch and Bound related
    return return_mwt_weight(dots, hull)
