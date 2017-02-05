from copy import deepcopy
from math import inf
from operator import itemgetter
from random import randint, random, choice

from libraries.cg_lib import diagonal_difference, in_convex_square
from libraries.st_lib import get_rct, get_characteristic, get_rct_edges
from solutions.hill_climbing import flip_edge


def find_non_final_hull(characteristic):
    index = randint(0, len(characteristic) - 2)
    while characteristic[index]['final']:
        index = randint(0, len(characteristic) - 2)
    return index


def buzz_the_bee(dots, bee, force=False, movable=True):
    work_index = 0 if force else find_non_final_hull(bee['characteristic'])
    potential_food_fitness = get_rct(dots, bee['characteristic'][work_index]['hull'])
    current_food_fitness = bee['characteristic'][work_index]['weight']
    if (potential_food_fitness < current_food_fitness) or force:
        bee['fitness'] -= (current_food_fitness - potential_food_fitness)
        splice_length = bee['characteristic'][work_index]['length']
        for i in range (0, work_index):
            if not bee['characteristic'][i]['final'] and ((bee['characteristic'][i]['length'] + i) > work_index):
                bee['characteristic'][i]['weight'] -= (current_food_fitness - potential_food_fitness)
        bee['characteristic'] = bee['characteristic'][0:work_index] + get_characteristic() + bee['characteristic'][work_index + splice_length:]
        bee['not_moved'] = 0
    else:
        bee['not_moved'] += (1 if movable else 0)


def calculate_fitness_weight(employed_bees, target_bee):
    return target_bee['fitness'] / sum(bee['fitness'] for bee in employed_bees)


def generate_random_triangulations(dots, hull, quantity, lite=True):
    triangulations = []
    for i in range(quantity):
        weight = get_rct(dots, hull, lite)
        if not any(triangulation['characteristic'] == get_characteristic() for triangulation in triangulations):
            triangulation = {
                'fitness': weight,
                'characteristic': get_characteristic(),
                'not_moved': 0}
            if lite:
                # triangulation['characteristic'] = get_characteristic()
                pass
            else:
                triangulation['edges'] = get_rct_edges(True, dots, hull)
            triangulations.append(triangulation)
        else:
            i -= 1
    return triangulations


def artificial_bee_colony_algorithm(dots, hull, food_sources_no=333):
    employed_bees = generate_random_triangulations(dots, hull, food_sources_no)
    onlooker_bees = []
    for bee in employed_bees:
        onlooker_bees.append(bee['fitness'])
    halt = False
    i = -1
    secured_bees_no = 0
    # while not halt:
    for _ in range(100):
        i += 1
        print(i)
        # Begin of employed bees phase
        for index in range(len(employed_bees)):
            buzz_the_bee(dots, employed_bees[i])
            temp_char = employed_bees[index]['characteristic']
            if any((bee['characteristic'] == temp_char and bee != employed_bees[i]) for bee in employed_bees):
                index -= 1
        # End of employed bees phase
        # Begin of onlooker bees phase
        for bee in employed_bees:
            index, max_value = max(enumerate(onlooker_bees), key=itemgetter(1))
            if bee['fitness'] < max_value:
                onlooker_bees[index] = bee['fitness']
            fitness_weight = calculate_fitness_weight(employed_bees, bee)
            if random() > fitness_weight:
                buzz_the_bee(dots, bee, False, False)
        # End of onlooker bees phase
        # Begin of scout bees phase
        for bee in employed_bees:
            # if bee['not_moved'] == 7:
            #     secured_bees_no += 1
            # if secured_bees_no == 1234:
            #     halt = True
            #     break
            if bee['not_moved'] == 7:
                buzz_the_bee(dots, bee, True)
        # End of scout bees phase
    best_food_source = inf
    for bee in employed_bees:
        best_food_source = bee['fitness'] if bee['fitness'] < best_food_source else best_food_source
    for fitness in onlooker_bees:
        best_food_source = fitness if fitness < best_food_source else best_food_source
    return best_food_source


def climb_the_bee(dots, bee):
    potential_edges = deepcopy(bee['edges'])
    potential_fitness = bee['fitness']
    iterations_no = randint(len(potential_edges), 3 * len(potential_edges))
    for i in range(iterations_no):
        if len(potential_edges[i % len(potential_edges)].incident_dots) == 0:
            continue
        diagonal_diff = diagonal_difference(potential_edges[i % len(potential_edges)])
        if in_convex_square(potential_edges[i % len(potential_edges)]):
            flip_edge(potential_edges, potential_edges[i % len(potential_edges)])
            potential_fitness -= diagonal_diff
    if potential_fitness < bee['fitness']:
        bee['fitness'] = potential_fitness
        bee['edges'] = potential_edges
        bee['not_moved'] = 0
    else:
        bee['not_moved'] += 1


def hybrid_artificial_bee_colony_algorithm(dots, hull, food_sources_no=114):
    employed_bees = generate_random_triangulations(dots, hull, food_sources_no, False)
    onlooker_bees = []
    for bee in employed_bees:
        onlooker_bees.append(bee['fitness'])
    halt = False
    while not halt:
        # Begin of employed bees phase
        for bee in employed_bees:
            climb_the_bee(dots, bee)
        # End of employed bees phase
        # Begin of onlooker bees phase
        for bee in employed_bees:
            fitness_weight = calculate_fitness_weight(employed_bees, bee)
            if random() > fitness_weight:
                climb_the_bee(dots, bee)
                index, max_value = max(enumerate(onlooker_bees), key=itemgetter(1))
                if bee['fitness'] < max_value:
                    onlooker_bees[index] = bee['fitness']
        # End of onlooker bees phase
        # Begin of scout bees phase
        secured_bees_no = 0
        for bee in employed_bees:
            if bee['not_moved'] >= 1:
                secured_bees_no += 1
            if secured_bees_no == 33:
                halt = True
                break
            # if bee['not_moved'] == 19:
            #     work_the_bee(dots, bee, True)
        # End of scout bees phase
    best_food_source = inf
    for bee in employed_bees:
        best_food_source = bee['fitness'] if bee['fitness'] < best_food_source else best_food_source
    return best_food_source


# ---------------------------------------------- NEW GENERATION ABC ---------------------------------------------- #


def spawn_employed_bees(reconstructed_edges, init_weight, food_sources_no):
    bees = []
    for _ in range(food_sources_no):
        bees.append({'fitness': init_weight, 'reconstructed_edges': deepcopy(reconstructed_edges), 'not_moved': 0})
    return bees


def fly_the_bee(bee, wander=False):
    edge_candidates = []
    for edge in bee['reconstructed_edges']:
        if len(edge.incident_dots) == 0:
            continue
        diagonal_diff = diagonal_difference(edge)
        if in_convex_square(edge) and (diagonal_diff >= 0 or wander):
            edge_candidates.append(edge)
    if len(edge_candidates):
        random_valid_edge = choice(edge_candidates)
        bee['fitness'] -= diagonal_difference(random_valid_edge)
        flip_edge(bee['reconstructed_edges'], random_valid_edge)
        bee['not_moved'] = 0
    else:
        bee['not_moved'] += 1


def fly_the_bee_to_the_top(bee):
    while bee['not_moved'] == 0:
        fly_the_bee(bee)


def wander_the_bee(bee, wandering_depth):
    for _ in range(wandering_depth):
        fly_the_bee(bee, True)


def random_wandering_abc_algorithm(reconstructed_edges, init_weight, food_sources_no=13):
    employed_bees = spawn_employed_bees(reconstructed_edges, init_weight, food_sources_no)
    onlooker_bees = []
    for bee in employed_bees:
        onlooker_bees.append(bee['fitness'])
    halt = False
    # while not halt:
    for _ in range(33):
        # Begin of employed bees phase
        for bee in employed_bees:
            fly_the_bee(bee)
        # End of employed bees phase
        # Begin of onlooker bees phase
        for bee in employed_bees:
            fitness_weight = calculate_fitness_weight(employed_bees, bee)
            if random() > fitness_weight:
                fly_the_bee_to_the_top(bee)
            index, max_value = max(enumerate(onlooker_bees), key=itemgetter(1))
            if bee['fitness'] < max_value:
                onlooker_bees[index] = bee['fitness']
        # End of onlooker bees phase
        # Begin of scout bees phase
        for bee in employed_bees:
            # if bee['not_moved'] == 7:
            #     secured_bees_no += 1
            # if secured_bees_no == 1234:
            #     halt = True
            #     break
            if bee['not_moved'] == 7:
                wander_the_bee(bee, food_sources_no)
        # End of scout bees phase
    best_food_source = inf
    for bee in employed_bees:
        best_food_source = bee['fitness'] if bee['fitness'] < best_food_source else best_food_source
    for fitness in onlooker_bees:
        best_food_source = fitness if fitness < best_food_source else best_food_source
    return best_food_source
