import random

import helpers.draw
import libraries.st_lib
from helpers import benchmark
from helpers.benchmark import output_stats
from libraries.st_lib import get_gct
from libraries.st_lib import get_gct_edges
from solutions.artificial_bee_colony import random_wandering_abc_algorithm
from solutions.exhaustive_search import do_exhaustive_search
from solutions.particle_swarm_optimization import basic_pso
from solutions.simulated_annealing import simulated_annealing
from structures.point import Point

animate = False

dots = [
    Point(x=5, y=275),
    Point(x=-140, y=3),
    Point(x=280, y=-110),
    Point(x=216, y=-116),
    Point(x=-240, y=-258),
    Point(x=286, y=-286),
    Point(x=-27, y=-292)
]

instances_no = 5
number_of_runs = 30
min_dots_quantity = 18
max_dots_quantity = 18

instances = [[Point(x=-299, y=-113), Point(x=-145, y=-149), Point(x=-106, y=41), Point(x=299, y=-255), Point(x=5, y=241), Point(x=-170, y=31), Point(x=-248, y=242), Point(x=9, y=88), Point(x=144, y=75), Point(x=-130, y=-241), Point(x=156, y=-286), Point(x=-22, y=30), Point(x=-308, y=201), Point(x=111, y=164), Point(x=278, y=-130), Point(x=-179, y=38), Point(x=-150, y=-292)]
, [Point(x=83, y=27), Point(x=-51, y=177), Point(x=-271, y=-146), Point(x=-168, y=-217), Point(x=-40, y=-54), Point(x=-316, y=-142), Point(x=74, y=277), Point(x=100, y=-257), Point(x=-299, y=119), Point(x=-60, y=199), Point(x=67, y=41), Point(x=-220, y=-196), Point(x=-42, y=-233), Point(x=-85, y=237), Point(x=261, y=84), Point(x=-40, y=1), Point(x=17, y=22)]
, [Point(x=131, y=-12), Point(x=-290, y=-269), Point(x=57, y=-214), Point(x=-225, y=202), Point(x=191, y=-291), Point(x=145, y=-142), Point(x=237, y=-254), Point(x=-21, y=-326), Point(x=226, y=300), Point(x=20, y=-106), Point(x=120, y=-80), Point(x=-295, y=280), Point(x=-30, y=-260), Point(x=-54, y=42), Point(x=-67, y=245), Point(x=-289, y=0), Point(x=-279, y=109)]
, [Point(x=183, y=-22), Point(x=81, y=-133), Point(x=277, y=-168), Point(x=-251, y=-68), Point(x=-181, y=-222), Point(x=123, y=37), Point(x=-106, y=-149), Point(x=205, y=-330), Point(x=286, y=129), Point(x=-25, y=211), Point(x=-59, y=-160), Point(x=-153, y=208), Point(x=220, y=-17), Point(x=-152, y=322), Point(x=258, y=-209), Point(x=172, y=-231), Point(x=-114, y=-32)]
, [Point(x=-237, y=-63), Point(x=329, y=307), Point(x=207, y=-249), Point(x=263, y=-212), Point(x=315, y=-182), Point(x=-331, y=-200), Point(x=-266, y=-13), Point(x=107, y=199), Point(x=-223, y=9), Point(x=99, y=81), Point(x=33, y=199), Point(x=-163, y=-308), Point(x=109, y=112), Point(x=-298, y=152), Point(x=-125, y=228), Point(x=316, y=133), Point(x=-56, y=-131)]
, [Point(x=125, y=-107), Point(x=-7, y=79), Point(x=-121, y=-165), Point(x=-269, y=-33), Point(x=-169, y=145), Point(x=146, y=-297), Point(x=-209, y=-231), Point(x=-256, y=54), Point(x=-223, y=177), Point(x=202, y=-307), Point(x=-287, y=-185), Point(x=-115, y=67), Point(x=45, y=82), Point(x=-152, y=199), Point(x=318, y=-248), Point(x=-51, y=242), Point(x=-261, y=-276)]
, [Point(x=77, y=-109), Point(x=281, y=-122), Point(x=-58, y=-283), Point(x=58, y=-84), Point(x=-297, y=190), Point(x=276, y=-299), Point(x=-37, y=-172), Point(x=172, y=176), Point(x=289, y=39), Point(x=-308, y=-139), Point(x=62, y=136), Point(x=217, y=43), Point(x=314, y=241), Point(x=-282, y=-245), Point(x=-243, y=-91), Point(x=-35, y=305), Point(x=206, y=19)]
, [Point(x=33, y=-56), Point(x=267, y=-125), Point(x=51, y=-147), Point(x=86, y=-215), Point(x=77, y=-91), Point(x=236, y=140), Point(x=229, y=274), Point(x=-215, y=51), Point(x=-279, y=-9), Point(x=30, y=112), Point(x=57, y=236), Point(x=-151, y=-9), Point(x=-231, y=211), Point(x=331, y=86), Point(x=-287, y=-259), Point(x=285, y=7), Point(x=44, y=-178)]
, [Point(x=98, y=121), Point(x=-223, y=-264), Point(x=-166, y=197), Point(x=306, y=56), Point(x=328, y=261), Point(x=113, y=-89), Point(x=-63, y=-167), Point(x=140, y=297), Point(x=-174, y=-85), Point(x=-81, y=65), Point(x=66, y=9), Point(x=332, y=-71), Point(x=-249, y=-328), Point(x=281, y=14), Point(x=162, y=76), Point(x=-154, y=45), Point(x=204, y=-61)]
, [Point(x=189, y=289), Point(x=-214, y=323), Point(x=-227, y=320), Point(x=56, y=218), Point(x=-238, y=146), Point(x=-247, y=170), Point(x=97, y=121), Point(x=202, y=228), Point(x=-29, y=-135), Point(x=-148, y=112), Point(x=-316, y=156), Point(x=21, y=61), Point(x=-65, y=-2), Point(x=105, y=116), Point(x=280, y=-63), Point(x=224, y=-90), Point(x=-110, y=119)]
, [Point(x=-224, y=127), Point(x=-186, y=-180), Point(x=221, y=-192), Point(x=-152, y=-234), Point(x=-158, y=-264), Point(x=-278, y=-329), Point(x=185, y=59), Point(x=-74, y=-113), Point(x=-298, y=313), Point(x=-110, y=19), Point(x=-101, y=-29), Point(x=-103, y=46), Point(x=188, y=-324), Point(x=144, y=-146), Point(x=-61, y=102), Point(x=24, y=154), Point(x=60, y=46)]]

test_char = [{'hull': [Point(x=-159, y=-292), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2400030, 'final': False, 'length': 29}, {'hull': [Point(x=-150, y=-292), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2345788, 'final': False, 'length': 28}, {'hull': [Point(x=-150, y=-292), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2325314, 'final': False, 'length': 27}, {'hull': [Point(x=-150, y=-292), Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2322313, 'final': False, 'length': 26}, {'hull': [Point(x=156, y=-286), Point(x=-150, y=-292), Point(x=-22, y=30)], 'final': True}, {'hull': [Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2108573, 'final': False, 'length': 24}, {'hull': [Point(x=-22, y=30), Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2023468, 'final': False, 'length': 23}, {'hull': [Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1362809, 'final': False, 'length': 11}, {'hull': [Point(x=-22, y=30), Point(x=-248, y=242), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1202779, 'final': False, 'length': 9}, {'hull': [Point(x=5, y=241), Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1185614, 'final': False, 'length': 8}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241)], 'weight': 955421, 'final': False, 'length': 6}, {'hull': [Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 917945, 'final': False, 'length': 4}, {'hull': [Point(x=156, y=-286), Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 786405, 'final': False, 'length': 3}, {'hull': [Point(x=5, y=241), Point(x=278, y=-130), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 653482, 'final': False, 'length': 11}, {'hull': [Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 564693, 'final': False, 'length': 9}, {'hull': [Point(x=-145, y=-149), Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 539681, 'final': False, 'length': 8}, {'hull': [Point(x=-106, y=41), Point(x=-145, y=-149), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 469035, 'final': False, 'length': 6}, {'hull': [Point(x=-170, y=31), Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 431658, 'final': False, 'length': 5}, {'hull': [Point(x=-248, y=242), Point(x=-106, y=41), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 316162, 'final': False, 'length': 3}, {'hull': [Point(x=-248, y=242), Point(x=-179, y=38), Point(x=-299, y=-113)], 'final': True}, {'hull': [Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149)], 'final': True}]
test_char2 = [{'hull': [Point(x=-159, y=-292), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2400030, 'final': False, 'length': 29}, {'hull': [Point(x=-150, y=-292), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2345788, 'final': False, 'length': 28}, {'hull': [Point(x=-150, y=-292), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2325314, 'final': False, 'length': 27}, {'hull': [Point(x=-150, y=-292), Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2322313, 'final': False, 'length': 26}, {'hull': [Point(x=156, y=-286), Point(x=-150, y=-292), Point(x=-22, y=30)], 'final': True}, {'hull': [Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2108573, 'final': False, 'length': 24}, {'hull': [Point(x=-22, y=30), Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2023468, 'final': False, 'length': 23}, {'hull': [Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1362809, 'final': False, 'length': 11}, {'hull': [Point(x=-22, y=30), Point(x=-248, y=242), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1202779, 'final': False, 'length': 9}, {'hull': [Point(x=5, y=241), Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1185614, 'final': False, 'length': 8}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241)], 'weight': 955421, 'final': False, 'length': 6}, {'hull': [Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 917945, 'final': False, 'length': 4}, {'hull': [Point(x=156, y=-286), Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 786405, 'final': False, 'length': 3}, {'hull': [Point(x=5, y=241), Point(x=278, y=-130), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 653482, 'final': False, 'length': 11}, {'hull': [Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 564693, 'final': False, 'length': 9}, {'hull': [Point(x=-145, y=-149), Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 539681, 'final': False, 'length': 8}, {'hull': [Point(x=-106, y=41), Point(x=-145, y=-149), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 469035, 'final': False, 'length': 6}, {'hull': [Point(x=-170, y=31), Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 431658, 'final': False, 'length': 5}, {'hull': [Point(x=-248, y=242), Point(x=-106, y=41), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 316162, 'final': False, 'length': 3}, {'hull': [Point(x=-248, y=242), Point(x=-179, y=38), Point(x=-299, y=-113)], 'final': True}, {'hull': [Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149)], 'final': True}]

# for dots in instances:
for instance_no in range(instances_no):
    dots = []
    dots_quantity = random.randint(min_dots_quantity, max_dots_quantity)

    for i in range(0, dots_quantity):
        dot_to_append = Point(x=random.randint(-333, 333), y=random.randint(-333, 333))
        while dot_to_append in dots:
            dot_to_append = Point(x=random.randint(-333, 333), y=random.randint(-333, 333))
        dots.append(Point(x=random.randint(-333, 333), y=random.randint(-333, 333)))

    convex_hull = libraries.cg_lib.return_convex_hull(dots)

    # if animate:
    #     helpers.draw.draw_dots(dots)
    #     helpers.draw.draw_polygon(convex_hull)

    print(str(instance_no + 1) + '. instance: {0}'.format(len(dots)), dots)
    print('\nTime Complexities (Minimum Weight Triangulation):')

    # # Begin of develop related only
    # seed_triangulations = get_seed_triangulations(dots, convex_hull)
    #
    # # print('\tFCT:', seed_triangulations['first_choice'], calculate_triangulation_weight(get_fct_edges()))
    # # print('\tCollision data: ', len(get_fct_edges()), count_collisions(get_fct_edges()))
    # # if animate:
    # #     helpers.draw.draw_edges(get_fct_edges())
    #
    # print('\tGCT:', seed_triangulations['greedy_choice'], calculate_triangulation_weight(get_gct_edges()))
    # print('\tCollision data: ', len(get_gct_edges()), count_collisions(get_gct_edges()))
    # if animate:
    #     # helpers.draw.turtle.color("red")
    #     # helpers.draw.turtle.clear()
    #     helpers.draw.draw_dots(dots)
    #     helpers.draw.draw_edges(get_gct_edges())
    #
    # libraries.cg_lib.reconstruct_incident_dots(get_gct_edges(), convex_hull)
    # print('\tFCHC:', first_choice_hill_climbing(get_gct_edges(), seed_triangulations['greedy_choice']))
    # # End of develop related only

    # # Begin of FCT seed
    # fct_results = benchmark.evaluate_method(get_fct, dots, convex_hull)
    # print('\tFirst Choice Triangulation:', fct_results[0], 's.',
    #       'Weight:', fct_results[1], '\n')
    #
    # libraries.cg_lib.reconstruct_incident_dots(dots, get_fct_edges(), convex_hull)
    # fchc_edges = deepcopy(get_fct_edges())
    # fchc_results = benchmark.evaluate_method(first_choice_hill_climbing, fchc_edges, fct_results[1])
    # print('\tFirst Choice Hill Climbing Heuristic (Seed: FCT):', fchc_results[0], 's.',
    #       'Weight:', fchc_results[1])
    #
    # gchc_edges = deepcopy(get_fct_edges())
    # gchc_results = benchmark.evaluate_method(greedy_choice_hill_climbing, gchc_edges, fct_results[1])
    # print('\tGreedy Choice Hill Climbing Heuristic (Seed: FCT):', gchc_results[0], 's.',
    #       'Weight:', gchc_results[1])
    #
    # schc_edges = deepcopy(get_fct_edges())
    # schc_results = benchmark.evaluate_method(stochastic_choice_hill_climbing, schc_edges, fct_results[1])
    # print('\tStochastic Choice Hill Climbing Heuristic (Seed: FCT):', schc_results[0], 's.',
    #       'Weight:', schc_results[1])
    #
    # sa_edges = deepcopy(get_fct_edges())
    # sa_results = benchmark.evaluate_method(simulated_annealing, sa_edges, fct_results[1])
    # print('\tSimulated Annealing Metaheuristic (Seed: FCT):', sa_results[0], 's.',
    #       'Weight:', sa_results[1], '\n')
    # # End of FCT seed

    # Begin of GCT seed
    gct_results = benchmark.evaluate_method(get_gct, dots, convex_hull)
    print('\tGreedy Choice Triangulation:', gct_results[0], 's.',
          'Weight:', gct_results[1], '\n')

    libraries.cg_lib.reconstruct_incident_dots(dots, get_gct_edges(), convex_hull)
    # fchc_edges = deepcopy(get_gct_edges())
    # fchc_results = benchmark.evaluate_method(first_choice_hill_climbing, fchc_edges, gct_results[1])
    # print('\tFirst Choice Hill Climbing Heuristic (Seed: GCT):', fchc_results[0], 's.',
    #       'Weight:', fchc_results[1])
    #
    # gchc_edges = deepcopy(get_gct_edges())
    # gchc_results = benchmark.evaluate_method(greedy_choice_hill_climbing, gchc_edges, gct_results[1])
    # print('\tGreedy Choice Hill Climbing Heuristic (Seed: GCT):', gchc_results[0], 's.',
    #       'Weight:', gchc_results[1])
    #
    # schc_edges = deepcopy(get_gct_edges())
    # schc_results = benchmark.evaluate_method(stochastic_choice_hill_climbing, schc_edges, gct_results[1])
    # print('\tStochastic Choice Hill Climbing Heuristic (Seed: GCT):', schc_results[0], 's.',
    #       'Weight:', schc_results[1])
    #
    # sa_edges = deepcopy(get_gct_edges())
    # sa_results = benchmark.evaluate_method(simulated_annealing, sa_edges, gct_results[1])
    # print('\tSimulated Annealing Metaheuristic (Seed: GCT):', sa_results[0], 's.',
    #       'Weight:', sa_results[1], '\n')
    # End of GCT seed

    # Begin of ABC algorithm related
    # abc_edges = deepcopy(get_gct_edges())
    # abc_results = benchmark.evaluate_method(random_wandering_abc_algorithm, abc_edges, gct_results[1])
    # print('\tRandom wandering ABC algorithm (Seed: GCT):', abc_results[0], 's.',
    #       'Weight:', abc_results[1], '\n')

    # artificial_bee_colony_results = benchmark.evaluate_method(artificial_bee_colony_algorithm, dots, convex_hull)
    # print('\tArtificial Bee Colony:', artificial_bee_colony_results[0], 's.',
    #       'Weight:', artificial_bee_colony_results[1])

    # hybrid_artificial_bee_colony_results = benchmark.evaluate_method(
    #                                                                   hybrid_artificial_bee_colony_algorithm,
    #                                                                   dots,
    #                                                                   convex_hull)
    # print('\tHybrid Artificial Bee Colony:', hybrid_artificial_bee_colony_results[0], 's.',
    #       'Weight:', hybrid_artificial_bee_colony_results[1], '\n')
    # End of ABC algorithm related

    # Begin of PSO solution related
    # pso_edges = deepcopy(get_gct_edges())
    # pso_results = benchmark.evaluate_method(basic_pso, pso_edges, gct_results[1], 33, 33, True)
    # print('\tBasic PSO solution (Seed: GCT):', pso_results[0], 's.',
    #       'Weight:', pso_results[1], '\n')
    # End of PSO solution related

    # Begin of Exhaustive Search
    exhaustive_search_results = benchmark.evaluate_method(do_exhaustive_search, dots, convex_hull)
    print('\tExhaustive Search:', exhaustive_search_results[0], 's.',
          'Weight:', exhaustive_search_results[1], '\n')
    # End of Exhaustive Search

    # Begin of debugging related
    # mwt_edges = get_triangulation_from_dots_order(dots, get_testing_dots_order(), convex_hull)
    # print('\tCollision data: ', len(mwt_edges), count_collisions(mwt_edges))
    # # End of debugging related

    # if animate:
    #     helpers.draw.turtle.color("red")
    #     helpers.draw.draw_edges(mwt_edges)

    # # Begin of results export
    with open('evaluations.txt', mode='w' if instance_no == 0 else 'a', encoding='utf-8') as eval_file:
        eval_file.write(str(instance_no + 1) + '.\n')
        # eval_file.write('[' + ''.join(str(e) + ', ' for e in dots) + ']')
        eval_file.write('\tInstance size: ' + str(dots_quantity) + '\n')
        # eval_file.write('\tGCT SE Weight: ' + str(gct_results[1]) + '. ')
        # eval_file.write('Time lapsed: ' + str(gct_results[0]) + 's\n')
        eval_file.write('\tOptimal Weight: ' + str(exhaustive_search_results[1]) + '.\n')
        # eval_file.write('Time lapsed: ' + str(exhaustive_search_results[0]) + 's\n\n')

        # Begin of advanced stats evaluation
        output_stats(get_gct_edges(),
                     simulated_annealing,
                     number_of_runs,
                     'SA',
                     eval_file,
                     gct_results[1])
        output_stats(get_gct_edges(),
                     basic_pso,
                     number_of_runs,
                     'PSO',
                     eval_file,
                     gct_results[1], 33, 33, True)
        output_stats(get_gct_edges(),
                     random_wandering_abc_algorithm,
                     number_of_runs,
                     'ABC',
                     eval_file,
                     gct_results[1])
        # End of advanced stats evaluation

    # # End of results export

if animate:
    helpers.draw.turtle.done()
