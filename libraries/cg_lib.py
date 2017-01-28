from helpers.utils import *
from structures.edge import Edge
from structures.point import Point


def return_simple_polygon(dots):
    shadow_dots = copy.copy(dots)
    reference_dot = min(shadow_dots, key=attrgetter('y'))
    shadow_dots.sort(key=lambda a: -a.x if a.y == reference_dot.y and a.x != reference_dot.x else a.y)
    shadow_dots[1:] = sorted(shadow_dots[1:],
                             key=lambda a: (math.inf - shadow_dots[0].x + a.x) * (-math.inf) if (a.y - shadow_dots[
                                 0].y) == 0 else (a.x - shadow_dots[0].x) / (
                                 a.y - shadow_dots[0].y))
    return shadow_dots


def return_convex_hull(dots):
    simple_polygon = return_simple_polygon(dots)
    convex_hull = [simple_polygon[0], simple_polygon[1]]

    acromion = 1
    for i in range(2, len(simple_polygon)):
        if ccw(convex_hull[acromion - 1], convex_hull[acromion], simple_polygon[i]) <= 0:
            acromion += 1
            convex_hull.append(simple_polygon[i])
            continue
        while ccw(convex_hull[acromion - 1], convex_hull[acromion], simple_polygon[i]) > 0:
            if acromion > 1:
                acromion -= 1
                convex_hull.pop()
            else:
                break
        acromion += 1
        convex_hull.append(simple_polygon[i])

    return convex_hull


def is_inside_triangle(p1, p2, p3, p):
    if ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)) == 0:
        return False
    alpha = ((p2.y - p3.y) * (p.x - p3.x) + (p3.x - p2.x) * (p.y - p3.y)) / ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y))
    if ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)) == 0:
        return False
    beta = ((p3.y - p1.y) * (p.x - p3.x) + (p1.x - p3.x) * (p.y - p3.y)) / ((p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y))
    gamma = 1.0 - alpha - beta
    return True if alpha >= 0 and beta >= 0 and gamma >= 0 else False


def is_inside_polygon(polygon, dot):
    if dot in polygon:
        return True
    rotating_point = Point(x=-500, y=500)
    epsilon = 1
    point_rotated = True
    while point_rotated:
        for polygon_dot in polygon:
            point_rotated = False
            if ccw(dot, polygon_dot, rotating_point) == 0:
                rotating_point.x += (epsilon * (-1 if rotating_point.y > 0 else 1))
                rotating_point.y += (epsilon * (-1 if rotating_point.x < 0 else 1))
                if rotating_point.y < 0:
                    print('Major Warning - Point rotated heavily.')
                point_rotated = True
                break
    cross_count = 0
    for i in range(len(polygon)):
        if are_intersected({'tail': polygon[i], 'head': polygon[(i + 1) % len(polygon)]},
                           {'tail': dot, 'head': rotating_point}):
            cross_count += 1
    return True if cross_count % 2 == 1 else False


def are_intersected(e1, e2):
    if (ccw(e1['tail'], e1['head'], e2['tail']) == 0 and (
        sign(e2['tail'].x - e1['tail'].x) != sign(e2['tail'].x - e1['head'].x))) or (
                ccw(e1['tail'], e1['head'], e2['head']) == 0) and (
            sign(e2['head'].x - e1['tail'].x) != sign(e2['head'].x - e1['head'].x)):
        return True
    if (sign(ccw(e1['tail'], e1['head'], e2['tail'])) != sign(ccw(e1['tail'], e1['head'], e2['head']))) and (
                sign(ccw(e2['tail'], e2['head'], e1['tail'])) != sign(ccw(e2['tail'], e2['head'], e1['head']))):
        return True
    return False


def is_polygon_clockwise(polygon):
    cw_sum = 0
    for i in range(len(polygon)):
        cw_sum += ((polygon[(i+1) % len(polygon)].x - polygon[i].x)*(polygon[(i+1) % len(polygon)].y + polygon[i].y))
    return True if cw_sum > 0 else False


def does_intersect_polygon(polygon, tail_dot, head_dot):
    n = len(polygon)
    for i in range(n):
        if tail_dot == polygon[i]:
            continue
        if tail_dot == polygon[(i+1) % n]:
            continue
        if head_dot == polygon[i]:
            continue
        if head_dot == polygon[(i + 1) % n]:
            continue
        if are_intersected({'tail': tail_dot, 'head': head_dot}, {'tail': polygon[i], 'head': polygon[(i+1) % n]}):
            return True
    return False


def form_empty_triangle(dots, tail_dot, head_dot, dot):
    for dot_candidate in dots:
        if dot_candidate == tail_dot:
            continue
        if dot_candidate == head_dot:
            continue
        if dot_candidate == dot:
            continue
        if is_inside_triangle(tail_dot, head_dot, dot, dot_candidate):
            return False
    return True


def is_empty_polygon(polygon, dots):
    for dot in dots:
        if dot in polygon:
            continue
        if is_inside_polygon(polygon, dot):
            return False
    return True


# Begin of heuristics related
def get_polygon_edges(dots):
    temp_edges = []
    for i in range(len(dots)):
        temp_edges.append(Edge(dots[i], dots[(i + 1) % len(dots)]))
    return temp_edges


def reconstruct_incident_dots(dots, edges, hull):
    hull_edges = get_polygon_edges(hull)
    for edge in edges:
        if edge in hull_edges:
            continue
        for edge_candidate in edges:
            if edge.flat_eq(edge_candidate):
                continue
            if form_empty_triangle(dots, edge.tail, edge.head, edge_candidate.head):
                if edge_candidate.tail == edge.tail and \
                        (Edge(edge_candidate.head, edge.head) in edges or Edge(edge.head,
                                                                               edge_candidate.head) in edges) and \
                                edge_candidate.head not in edge.incident_dots:
                    edge.incident_dots.append(edge_candidate.head)
                elif edge_candidate.tail == edge.head and \
                        (Edge(edge_candidate.head, edge.tail) in edges or Edge(edge.tail,
                                                                               edge_candidate.head) in edges) and \
                                edge_candidate.head not in edge.incident_dots:
                    edge.incident_dots.append(edge_candidate.head)
            if form_empty_triangle(dots, edge.tail, edge.head, edge_candidate.tail):
                if edge_candidate.head == edge.tail and \
                        (Edge(edge_candidate.tail, edge.head) in edges or Edge(edge.head,
                                                                               edge_candidate.tail) in edges) and \
                                edge_candidate.tail not in edge.incident_dots:
                    edge.incident_dots.append(edge_candidate.tail)
                elif edge_candidate.head == edge.head and \
                        (Edge(edge_candidate.tail, edge.tail) in edges or Edge(edge.tail,
                                                                               edge_candidate.tail) in edges) and \
                                edge_candidate.tail not in edge.incident_dots:
                    edge.incident_dots.append(edge_candidate.tail)


def diagonal_difference(edge):
    return edge.get_weight() - eucledian_sqrd_distance(edge.incident_dots[0], edge.incident_dots[1])


def in_convex_square(edge):
    if ccw(edge.tail, edge.incident_dots[0], edge.head) == 0:
        return False
    if ccw(edge.tail, edge.incident_dots[1], edge.head) == 0:
        return False
    return are_intersected({'tail': edge.tail, 'head': edge.head},
                           {'tail': edge.incident_dots[0], 'head': edge.incident_dots[1]})
# End of heuristics related
