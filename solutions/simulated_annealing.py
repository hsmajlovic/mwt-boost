from math import exp
from random import random, uniform

from libraries.cg_lib import diagonal_difference, in_convex_square
from solutions.hill_climbing import flip_edge


def simulated_annealing(reconstructed_edges,
                        init_weight,
                        boltzmann=1380648.8131313131313,
                        limit=1000):
    temp_mwt_weight = init_weight
    t = 1
    alpha = uniform(0.85, 0.99)
    k = boltzmann

    solution_changed = True
    iterations_count = 0
    while solution_changed:
        solution_changed = False
        for edge in reconstructed_edges:
            iterations_count += 1
            if limit and iterations_count >= limit:
                return temp_mwt_weight
            if len(edge.incident_dots) == 0:
                continue
            diagonal_diff = diagonal_difference(edge)
            if in_convex_square(edge) and (diagonal_diff >= 0 or exp(diagonal_diff / (k * t)) > random()):
                flip_edge(reconstructed_edges, edge)
                temp_mwt_weight -= diagonal_diff
                solution_changed = True
        t *= alpha
    return temp_mwt_weight
