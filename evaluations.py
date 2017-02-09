import random

import helpers.draw
import libraries.st_lib
from helpers import benchmark
from helpers.benchmark import output_stats
from helpers.utils import get_random_from_range
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
number_of_runs = 50
min_dots_quantity = 15
max_dots_quantity = 15
lower_value_limit = -500
upper_value_limit = 500
use_ints = False
use_gauss = True

instances = [[Point(x=-211, y=-25),Point(x=-293, y=-268),Point(x=230, y=-262),Point(x=9, y=82),Point(x=-150, y=-125),Point(x=254, y=-137),Point(x=-203, y=-18),Point(x=-102, y=50),Point(x=269, y=-46),Point(x=268, y=255),Point(x=153, y=32),Point(x=-118, y=-250),Point(x=246, y=-225),Point(x=-38, y=-256),Point(x=-133, y=-171),Point(x=213, y=135),Point(x=-329, y=-148),Point(x=159, y=131),Point(x=-318, y=-283),Point(x=142, y=-15),Point(x=-285, y=-299),Point(x=161, y=166),Point(x=125, y=-57)]
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

instances_23 = [
[Point(x=-76, y=182),Point(x=237, y=-76),Point(x=-68, y=249),Point(x=-188, y=73),Point(x=-25, y=263),Point(x=-80, y=100),Point(x=28, y=103),Point(x=263, y=-292),Point(x=-12, y=-152),Point(x=-179, y=166),Point(x=194, y=-100),Point(x=49, y=124),Point(x=162, y=122),Point(x=26, y=-131),Point(x=-126, y=-238),Point(x=80, y=-125),Point(x=266, y=-44),Point(x=-3, y=287),Point(x=-92, y=34),Point(x=-64, y=-108),Point(x=80, y=25),Point(x=-333, y=-227),Point(x=-120, y=-301)],
[Point(x=-218, y=-272),Point(x=-118, y=-236),Point(x=293, y=62),Point(x=-247, y=-273),Point(x=325, y=214),Point(x=-267, y=-132),Point(x=-192, y=301),Point(x=278, y=179),Point(x=-166, y=-132),Point(x=-159, y=-237),Point(x=-73, y=329),Point(x=-129, y=44),Point(x=-328, y=4),Point(x=-65, y=309),Point(x=-283, y=70),Point(x=162, y=187),Point(x=-292, y=281),Point(x=152, y=213),Point(x=215, y=221),Point(x=-266, y=146),Point(x=289, y=255),Point(x=204, y=147),Point(x=-63, y=-239)],
[Point(x=-42, y=276),Point(x=187, y=62),Point(x=238, y=-311),Point(x=329, y=319),Point(x=305, y=188),Point(x=53, y=-179),Point(x=315, y=-240),Point(x=52, y=47),Point(x=-93, y=-141),Point(x=-287, y=97),Point(x=16, y=1),Point(x=104, y=-167),Point(x=280, y=164),Point(x=-243, y=-312),Point(x=238, y=-160),Point(x=-312, y=-130),Point(x=210, y=-215),Point(x=-85, y=-280),Point(x=238, y=19),Point(x=-161, y=-225),Point(x=185, y=28),Point(x=-191, y=-131),Point(x=303, y=-34)],
[Point(x=1, y=22),Point(x=-77, y=203),Point(x=193, y=-76),Point(x=-231, y=-152),Point(x=316, y=-18),Point(x=-320, y=255),Point(x=-208, y=-268),Point(x=-304, y=321),Point(x=-184, y=293),Point(x=-310, y=-232),Point(x=-110, y=-192),Point(x=-228, y=179),Point(x=-140, y=288),Point(x=236, y=-292),Point(x=-7, y=-88),Point(x=-163, y=-59),Point(x=-112, y=194),Point(x=-75, y=114),Point(x=186, y=198),Point(x=-5, y=11),Point(x=306, y=-267),Point(x=-294, y=-274),Point(x=112, y=-171)],
[Point(x=276, y=-103),Point(x=224, y=315),Point(x=-331, y=-310),Point(x=22, y=96),Point(x=236, y=-275),Point(x=323, y=79),Point(x=-260, y=-16),Point(x=-143, y=-305),Point(x=76, y=-207),Point(x=258, y=-57),Point(x=-102, y=-284),Point(x=88, y=-303),Point(x=0, y=220),Point(x=23, y=282),Point(x=141, y=24),Point(x=-59, y=277),Point(x=-291, y=103),Point(x=-160, y=-126),Point(x=-75, y=288),Point(x=188, y=169),Point(x=34, y=196),Point(x=-32, y=61),Point(x=-66, y=34)]
]

instances_22 = [
    [Point(x=41, y=-82), Point(x=-296, y=-191), Point(x=129, y=263), Point(x=171, y=208), Point(x=2, y=-291),
     Point(x=172, y=-112), Point(x=117, y=-22), Point(x=228, y=-325), Point(x=0, y=-94), Point(x=115, y=57),
     Point(x=167, y=-83), Point(x=-224, y=-146), Point(x=-301, y=-267), Point(x=-58, y=-278), Point(x=91, y=207),
     Point(x=-81, y=282), Point(x=35, y=325), Point(x=176, y=-321), Point(x=-312, y=-170), Point(x=316, y=-306),
     Point(x=325, y=-14), Point(x=164, y=277)],
[Point(x=-30, y=-66),Point(x=-115, y=178),Point(x=-157, y=-207),Point(x=64, y=-71),Point(x=13, y=228),Point(x=161, y=208),Point(x=-256, y=102),Point(x=260, y=9),Point(x=-120, y=-187),Point(x=66, y=254),Point(x=50, y=-221),Point(x=-260, y=184),Point(x=-254, y=249),Point(x=-214, y=-304),Point(x=173, y=30),Point(x=17, y=-285),Point(x=153, y=153),Point(x=-329, y=35),Point(x=34, y=-83),Point(x=188, y=-285),Point(x=-324, y=-63),Point(x=-28, y=-127)],
[Point(x=177, y=-152),Point(x=-188, y=21),Point(x=68, y=-306),Point(x=-38, y=-224),Point(x=46, y=-16),Point(x=211, y=-206),Point(x=133, y=-180),Point(x=304, y=64),Point(x=-288, y=-205),Point(x=-177, y=-132),Point(x=-80, y=-259),Point(x=-148, y=-275),Point(x=320, y=-327),Point(x=255, y=217),Point(x=-5, y=-220),Point(x=161, y=79),Point(x=38, y=-314),Point(x=236, y=-102),Point(x=-106, y=-198),Point(x=-327, y=-115),Point(x=139, y=-235),Point(x=-222, y=120)],
[Point(x=-87, y=-19),Point(x=-40, y=164),Point(x=-321, y=179),Point(x=-123, y=-242),Point(x=-36, y=-46),Point(x=110, y=-213),Point(x=253, y=-203),Point(x=-36, y=240),Point(x=-115, y=-105),Point(x=-231, y=-195),Point(x=-241, y=34),Point(x=-260, y=-186),Point(x=-191, y=149),Point(x=112, y=-279),Point(x=-44, y=90),Point(x=-217, y=126),Point(x=225, y=-68),Point(x=-72, y=3),Point(x=139, y=-55),Point(x=-304, y=-292),Point(x=277, y=-251),Point(x=276, y=45)],
[Point(x=-104, y=86),Point(x=-12, y=-246),Point(x=-20, y=246),Point(x=67, y=-172),Point(x=282, y=273),Point(x=146, y=-255),Point(x=26, y=-322),Point(x=236, y=134),Point(x=1, y=-196),Point(x=-275, y=179),Point(x=-172, y=253),Point(x=-112, y=276),Point(x=159, y=-223),Point(x=222, y=-118),Point(x=-307, y=-37),Point(x=163, y=210),Point(x=165, y=-15),Point(x=243, y=-302),Point(x=-254, y=-191),Point(x=-90, y=73),Point(x=150, y=-41),Point(x=261, y=258)],

]

instances_21 = [
[Point(x=-100, y=-319),Point(x=302, y=-223),Point(x=51, y=-194),Point(x=251, y=-52),Point(x=-61, y=71),Point(x=143, y=-68),Point(x=321, y=14),Point(x=-144, y=39),Point(x=-269, y=-180),Point(x=129, y=-225),Point(x=175, y=163),Point(x=-266, y=213),Point(x=98, y=251),Point(x=118, y=-245),Point(x=-240, y=124),Point(x=44, y=293),Point(x=55, y=-73),Point(x=288, y=25),Point(x=2, y=325),Point(x=-229, y=-67),Point(x=-155, y=-7)],
[Point(x=79, y=250),Point(x=240, y=-140),Point(x=322, y=11),Point(x=27, y=-204),Point(x=257, y=-80),Point(x=225, y=322),Point(x=-112, y=-51),Point(x=-175, y=302),Point(x=-232, y=-180),Point(x=130, y=-41),Point(x=283, y=-141),Point(x=-315, y=301),Point(x=-10, y=36),Point(x=-310, y=-29),Point(x=273, y=-312),Point(x=-210, y=-120),Point(x=236, y=171),Point(x=0, y=-160),Point(x=18, y=250),Point(x=137, y=140),Point(x=179, y=-330)],
[Point(x=-226, y=305),Point(x=276, y=233),Point(x=226, y=237),Point(x=71, y=141),Point(x=-216, y=-27),Point(x=-255, y=-143),Point(x=-37, y=-89),Point(x=247, y=234),Point(x=-70, y=99),Point(x=-309, y=50),Point(x=-49, y=-6),Point(x=-66, y=99),Point(x=-72, y=-320),Point(x=214, y=-16),Point(x=-128, y=-9),Point(x=-63, y=-301),Point(x=-215, y=300),Point(x=-23, y=146),Point(x=5, y=-217),Point(x=-22, y=244),Point(x=-258, y=18)],
[Point(x=-79, y=73),Point(x=-186, y=16),Point(x=7, y=-172),Point(x=211, y=-271),Point(x=265, y=210),Point(x=-82, y=283),Point(x=41, y=251),Point(x=-59, y=59),Point(x=34, y=-154),Point(x=161, y=222),Point(x=206, y=-297),Point(x=88, y=14),Point(x=262, y=-93),Point(x=-44, y=157),Point(x=216, y=1),Point(x=-197, y=116),Point(x=182, y=-36),Point(x=-194, y=114),Point(x=283, y=-45),Point(x=213, y=-287),Point(x=241, y=55)],
[Point(x=-146, y=96),Point(x=170, y=-43),Point(x=-229, y=327),Point(x=45, y=-113),Point(x=-65, y=-93),Point(x=297, y=248),Point(x=-223, y=120),Point(x=52, y=-132),Point(x=152, y=-150),Point(x=104, y=-59),Point(x=248, y=-45),Point(x=305, y=-215),Point(x=243, y=-200),Point(x=39, y=19),Point(x=180, y=66),Point(x=-272, y=-75),Point(x=78, y=-258),Point(x=33, y=194),Point(x=-294, y=-266),Point(x=-312, y=217),Point(x=-108, y=-228)],
]

instances_20 = [
[Point(x=-247, y=-18),Point(x=96, y=-228),Point(x=-210, y=-236),Point(x=-183, y=-238),Point(x=35, y=123),Point(x=162, y=316),Point(x=106, y=262),Point(x=81, y=0),Point(x=217, y=149),Point(x=226, y=-153),Point(x=321, y=232),Point(x=146, y=112),Point(x=-292, y=325),Point(x=-143, y=-27),Point(x=-238, y=211),Point(x=-304, y=-191),Point(x=-274, y=-105),Point(x=255, y=280),Point(x=-44, y=-14),Point(x=-188, y=137)],
[Point(x=-220, y=-145),Point(x=118, y=281),Point(x=318, y=-127),Point(x=133, y=225),Point(x=-303, y=-35),Point(x=-40, y=-319),Point(x=-330, y=-284),Point(x=136, y=-149),Point(x=-237, y=-258),Point(x=243, y=-223),Point(x=162, y=101),Point(x=124, y=302),Point(x=104, y=-274),Point(x=294, y=120),Point(x=-232, y=-301),Point(x=0, y=168),Point(x=180, y=295),Point(x=-214, y=131),Point(x=-72, y=296),Point(x=16, y=31)],
[Point(x=-141, y=-123),Point(x=-203, y=-153),Point(x=-182, y=221),Point(x=-140, y=-153),Point(x=66, y=-50),Point(x=-319, y=299),Point(x=4, y=-266),Point(x=-88, y=63),Point(x=218, y=14),Point(x=-14, y=279),Point(x=-51, y=17),Point(x=154, y=58),Point(x=47, y=61),Point(x=211, y=284),Point(x=123, y=245),Point(x=-135, y=208),Point(x=-47, y=-172),Point(x=255, y=53),Point(x=-100, y=-114),Point(x=-17, y=176)],
[Point(x=51, y=-61),Point(x=240, y=-40),Point(x=-57, y=216),Point(x=-35, y=-101),Point(x=-64, y=-105),Point(x=-41, y=318),Point(x=176, y=-284),Point(x=-188, y=75),Point(x=239, y=32),Point(x=228, y=225),Point(x=-23, y=261),Point(x=242, y=-318),Point(x=86, y=91),Point(x=248, y=-198),Point(x=-34, y=-212),Point(x=-71, y=179),Point(x=-39, y=-153),Point(x=183, y=-177),Point(x=311, y=-300),Point(x=-175, y=284)],
[Point(x=-187, y=19),Point(x=2, y=-233),Point(x=145, y=-160),Point(x=190, y=30),Point(x=80, y=131),Point(x=-246, y=168),Point(x=-152, y=17),Point(x=-128, y=82),Point(x=-27, y=182),Point(x=182, y=-262),Point(x=-316, y=240),Point(x=199, y=317),Point(x=-253, y=158),Point(x=133, y=307),Point(x=48, y=263),Point(x=-27, y=246),Point(x=151, y=259),Point(x=49, y=180),Point(x=33, y=-322),Point(x=-223, y=76)]
]

instances_19 = [
[Point(x=-281, y=319),Point(x=-91, y=68),Point(x=-252, y=-50),Point(x=330, y=-234),Point(x=-97, y=-278),Point(x=30, y=235),Point(x=25, y=-41),Point(x=-247, y=287),Point(x=-252, y=283),Point(x=330, y=-193),Point(x=-314, y=-54),Point(x=233, y=-29),Point(x=239, y=-183),Point(x=-36, y=54),Point(x=149, y=189),Point(x=-331, y=-40),Point(x=-312, y=-233),Point(x=83, y=3),Point(x=-328, y=226)],
[Point(x=233, y=-15),Point(x=-93, y=10),Point(x=263, y=305),Point(x=-211, y=-24),Point(x=162, y=157),Point(x=148, y=-161),Point(x=144, y=219),Point(x=10, y=-290),Point(x=-46, y=187),Point(x=73, y=-173),Point(x=163, y=112),Point(x=-128, y=-122),Point(x=225, y=87),Point(x=-276, y=-151),Point(x=-23, y=127),Point(x=-267, y=210),Point(x=-60, y=-186),Point(x=301, y=39),Point(x=38, y=-7)],
[Point(x=-44, y=9),Point(x=291, y=136),Point(x=-2, y=157),Point(x=177, y=183),Point(x=216, y=148),Point(x=157, y=127),Point(x=47, y=-207),Point(x=-179, y=237),Point(x=50, y=23),Point(x=167, y=285),Point(x=-140, y=-210),Point(x=-200, y=-31),Point(x=231, y=-327),Point(x=-327, y=53),Point(x=266, y=-139),Point(x=195, y=69),Point(x=118, y=155),Point(x=-139, y=-304),Point(x=242, y=-155)],
[Point(x=-179, y=238),Point(x=-194, y=-275),Point(x=12, y=198),Point(x=244, y=-18),Point(x=103, y=113),Point(x=148, y=-296),Point(x=-266, y=164),Point(x=107, y=168),Point(x=-218, y=100),Point(x=-140, y=83),Point(x=-187, y=165),Point(x=-196, y=242),Point(x=41, y=76),Point(x=-157, y=3),Point(x=123, y=-127),Point(x=-197, y=-49),Point(x=275, y=-330),Point(x=7, y=-313),Point(x=39, y=257)],
[Point(x=243, y=79),Point(x=-31, y=184),Point(x=103, y=-301),Point(x=-56, y=-40),Point(x=119, y=-7),Point(x=-202, y=18),Point(x=45, y=-234),Point(x=146, y=78),Point(x=-1, y=24),Point(x=-296, y=62),Point(x=-314, y=268),Point(x=276, y=53),Point(x=168, y=-187),Point(x=-307, y=43),Point(x=230, y=160),Point(x=62, y=-18),Point(x=-228, y=-186),Point(x=39, y=57),Point(x=203, y=239)]
]

instances_18 = [
[Point(x=260, y=-54),Point(x=294, y=82),Point(x=2, y=10),Point(x=273, y=-160),Point(x=185, y=138),Point(x=327, y=164),Point(x=-311, y=-319),Point(x=-124, y=158),Point(x=146, y=164),Point(x=54, y=189),Point(x=267, y=70),Point(x=-279, y=122),Point(x=35, y=-301),Point(x=-112, y=281),Point(x=-173, y=84),Point(x=268, y=-242),Point(x=39, y=108),Point(x=-127, y=-238)],
[Point(x=27, y=229),Point(x=-11, y=-211),Point(x=-129, y=209),Point(x=-131, y=-312),Point(x=-301, y=196),Point(x=179, y=-318),Point(x=138, y=153),Point(x=62, y=-83),Point(x=171, y=-178),Point(x=315, y=252),Point(x=199, y=107),Point(x=202, y=-327),Point(x=181, y=-254),Point(x=62, y=230),Point(x=141, y=-314),Point(x=-217, y=281),Point(x=-205, y=323),Point(x=189, y=250)],
[Point(x=96, y=-128),Point(x=253, y=-213),Point(x=308, y=19),Point(x=-246, y=-25),Point(x=-230, y=-45),Point(x=312, y=-132),Point(x=118, y=-102),Point(x=243, y=-12),Point(x=-147, y=-72),Point(x=-79, y=-58),Point(x=300, y=326),Point(x=-1, y=-68),Point(x=-240, y=-211),Point(x=131, y=99),Point(x=-148, y=-202),Point(x=-7, y=-204),Point(x=-213, y=-280),Point(x=-129, y=-153)],
[Point(x=175, y=-199),Point(x=44, y=304),Point(x=-11, y=-43),Point(x=307, y=-276),Point(x=49, y=153),Point(x=110, y=-94),Point(x=-191, y=42),Point(x=-325, y=54),Point(x=-140, y=-129),Point(x=122, y=-169),Point(x=227, y=81),Point(x=52, y=-236),Point(x=103, y=-200),Point(x=212, y=-232),Point(x=-9, y=-52),Point(x=301, y=-328),Point(x=-83, y=155),Point(x=-160, y=-197)],
[Point(x=287, y=-133),Point(x=273, y=-29),Point(x=134, y=-98),Point(x=-42, y=-102),Point(x=114, y=-56),Point(x=-243, y=-177),Point(x=172, y=-120),Point(x=70, y=272),Point(x=-227, y=79),Point(x=55, y=-96),Point(x=173, y=-127),Point(x=-230, y=-115),Point(x=-120, y=91),Point(x=-214, y=-53),Point(x=199, y=259),Point(x=236, y=115),Point(x=190, y=-137),Point(x=-285, y=96)]
]

instances_17 = [
[Point(x=-215, y=331),Point(x=-114, y=265),Point(x=-186, y=75),Point(x=-207, y=206),Point(x=282, y=-107),Point(x=278, y=-275),Point(x=124, y=-305),Point(x=57, y=-60),Point(x=82, y=-46),Point(x=177, y=-97),Point(x=-150, y=-232),Point(x=-53, y=35),Point(x=-194, y=-219),Point(x=-2, y=-220),Point(x=-175, y=-74),Point(x=-277, y=172),Point(x=-213, y=247)],
[Point(x=-110, y=-275),Point(x=50, y=-5),Point(x=330, y=-140),Point(x=90, y=-290),Point(x=-33, y=-177),Point(x=34, y=153),Point(x=20, y=-171),Point(x=54, y=129),Point(x=-151, y=45),Point(x=-222, y=-160),Point(x=17, y=-13),Point(x=-220, y=104),Point(x=63, y=255),Point(x=-9, y=-157),Point(x=-39, y=-192),Point(x=148, y=-151),Point(x=-50, y=319)],
[Point(x=240, y=91),Point(x=266, y=-318),Point(x=-186, y=-321),Point(x=-14, y=111),Point(x=70, y=-44),Point(x=-328, y=-33),Point(x=330, y=241),Point(x=184, y=-240),Point(x=-40, y=288),Point(x=-78, y=-95),Point(x=-54, y=246),Point(x=54, y=143),Point(x=-234, y=189),Point(x=-314, y=-274),Point(x=-109, y=142),Point(x=-170, y=-37),Point(x=-77, y=115)],
[Point(x=211, y=-2),Point(x=-286, y=-324),Point(x=144, y=269),Point(x=-258, y=-29),Point(x=193, y=58),Point(x=-136, y=92),Point(x=284, y=-35),Point(x=198, y=112),Point(x=64, y=-57),Point(x=45, y=-146),Point(x=-158, y=-276),Point(x=122, y=-32),Point(x=236, y=321),Point(x=186, y=-199),Point(x=205, y=-274),Point(x=-174, y=-6),Point(x=312, y=121)],
[Point(x=-156, y=45),Point(x=95, y=86),Point(x=-185, y=-64),Point(x=-176, y=97),Point(x=131, y=165),Point(x=-285, y=-124),Point(x=-270, y=57),Point(x=321, y=9),Point(x=-61, y=-330),Point(x=26, y=-240),Point(x=83, y=-196),Point(x=-311, y=114),Point(x=160, y=160),Point(x=230, y=-166),Point(x=140, y=-251),Point(x=293, y=-51),Point(x=202, y=87)]
]

instances_16 = [
[Point(x=96, y=65),Point(x=53, y=14),Point(x=178, y=249),Point(x=293, y=-16),Point(x=305, y=46),Point(x=162, y=-317),Point(x=271, y=122),Point(x=281, y=-43),Point(x=319, y=-45),Point(x=251, y=-246),Point(x=-251, y=192),Point(x=-204, y=-264),Point(x=-285, y=-149),Point(x=199, y=97),Point(x=-50, y=-151),Point(x=133, y=-16)],
[Point(x=332, y=30),Point(x=-78, y=101),Point(x=105, y=215),Point(x=-311, y=125),Point(x=312, y=257),Point(x=313, y=-228),Point(x=-118, y=-206),Point(x=168, y=173),Point(x=191, y=-89),Point(x=-243, y=91),Point(x=59, y=-148),Point(x=-7, y=82),Point(x=-216, y=106),Point(x=-29, y=-299),Point(x=-175, y=59),Point(x=-36, y=-279)],
[Point(x=-172, y=23),Point(x=177, y=301),Point(x=-67, y=-77),Point(x=61, y=-37),Point(x=55, y=328),Point(x=-155, y=-134),Point(x=122, y=73),Point(x=-22, y=290),Point(x=-240, y=-286),Point(x=-22, y=-319),Point(x=-119, y=11),Point(x=54, y=-18),Point(x=-277, y=17),Point(x=308, y=-183),Point(x=327, y=60),Point(x=273, y=64)],
[Point(x=-159, y=184),Point(x=-270, y=318),Point(x=-49, y=115),Point(x=-306, y=185),Point(x=-85, y=-95),Point(x=314, y=-42),Point(x=84, y=-132),Point(x=-139, y=310),Point(x=96, y=-45),Point(x=186, y=252),Point(x=-312, y=269),Point(x=-317, y=106),Point(x=114, y=46),Point(x=186, y=323),Point(x=109, y=4),Point(x=283, y=115)],
[Point(x=-95, y=-262),Point(x=27, y=314),Point(x=-15, y=-171),Point(x=-6, y=-205),Point(x=90, y=-138),Point(x=288, y=44),Point(x=69, y=90),Point(x=310, y=273),Point(x=52, y=204),Point(x=160, y=-273),Point(x=2, y=-260),Point(x=327, y=-128),Point(x=-272, y=116),Point(x=164, y=97),Point(x=-293, y=-291),Point(x=91, y=273)]
]

instances_15 = [
[Point(x=281, y=-108),Point(x=-132, y=1),Point(x=132, y=1),Point(x=3, y=-100),Point(x=312, y=19),Point(x=-173, y=200),Point(x=-20, y=-4),Point(x=-276, y=327),Point(x=-100, y=-169),Point(x=-166, y=-323),Point(x=-209, y=186),Point(x=1, y=-66),Point(x=-90, y=283),Point(x=-23, y=-83),Point(x=326, y=65)],
[Point(x=-3, y=166),Point(x=-31, y=129),Point(x=-106, y=198),Point(x=-88, y=-195),Point(x=-239, y=-266),Point(x=-154, y=-323),Point(x=-174, y=82),Point(x=-101, y=-314),Point(x=240, y=-106),Point(x=60, y=-120),Point(x=-243, y=140),Point(x=287, y=-84),Point(x=-21, y=-252),Point(x=-124, y=-276),Point(x=83, y=298)],
[Point(x=228, y=-123),Point(x=25, y=122),Point(x=159, y=-121),Point(x=-205, y=181),Point(x=-36, y=221),Point(x=-291, y=100),Point(x=-170, y=277),Point(x=-291, y=196),Point(x=189, y=-82),Point(x=218, y=220),Point(x=224, y=-294),Point(x=-291, y=304),Point(x=39, y=12),Point(x=-313, y=12),Point(x=-79, y=109)],
[Point(x=-93, y=-267),Point(x=-170, y=-143),Point(x=1, y=-187),Point(x=-202, y=-143),Point(x=-274, y=-188),Point(x=-81, y=36),Point(x=70, y=-168),Point(x=-63, y=19),Point(x=247, y=157),Point(x=274, y=-158),Point(x=-108, y=142),Point(x=-102, y=-211),Point(x=98, y=-324),Point(x=144, y=-225),Point(x=-299, y=-273)],
[Point(x=231, y=-129),Point(x=207, y=186),Point(x=226, y=-7),Point(x=251, y=181),Point(x=-85, y=297),Point(x=230, y=17),Point(x=43, y=-122),Point(x=328, y=151),Point(x=121, y=-328),Point(x=-226, y=316),Point(x=-168, y=-268),Point(x=217, y=50),Point(x=176, y=284),Point(x=-99, y=65),Point(x=218, y=-191)]
]

test_char = [{'hull': [Point(x=-159, y=-292), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2400030, 'final': False, 'length': 29}, {'hull': [Point(x=-150, y=-292), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2345788, 'final': False, 'length': 28}, {'hull': [Point(x=-150, y=-292), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2325314, 'final': False, 'length': 27}, {'hull': [Point(x=-150, y=-292), Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2322313, 'final': False, 'length': 26}, {'hull': [Point(x=156, y=-286), Point(x=-150, y=-292), Point(x=-22, y=30)], 'final': True}, {'hull': [Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2108573, 'final': False, 'length': 24}, {'hull': [Point(x=-22, y=30), Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2023468, 'final': False, 'length': 23}, {'hull': [Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1362809, 'final': False, 'length': 11}, {'hull': [Point(x=-22, y=30), Point(x=-248, y=242), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1202779, 'final': False, 'length': 9}, {'hull': [Point(x=5, y=241), Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1185614, 'final': False, 'length': 8}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241)], 'weight': 955421, 'final': False, 'length': 6}, {'hull': [Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 917945, 'final': False, 'length': 4}, {'hull': [Point(x=156, y=-286), Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 786405, 'final': False, 'length': 3}, {'hull': [Point(x=5, y=241), Point(x=278, y=-130), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 653482, 'final': False, 'length': 11}, {'hull': [Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 564693, 'final': False, 'length': 9}, {'hull': [Point(x=-145, y=-149), Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 539681, 'final': False, 'length': 8}, {'hull': [Point(x=-106, y=41), Point(x=-145, y=-149), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 469035, 'final': False, 'length': 6}, {'hull': [Point(x=-170, y=31), Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 431658, 'final': False, 'length': 5}, {'hull': [Point(x=-248, y=242), Point(x=-106, y=41), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 316162, 'final': False, 'length': 3}, {'hull': [Point(x=-248, y=242), Point(x=-179, y=38), Point(x=-299, y=-113)], 'final': True}, {'hull': [Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149)], 'final': True}]
test_char2 = [{'hull': [Point(x=-159, y=-292), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2400030, 'final': False, 'length': 29}, {'hull': [Point(x=-150, y=-292), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2345788, 'final': False, 'length': 28}, {'hull': [Point(x=-150, y=-292), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2325314, 'final': False, 'length': 27}, {'hull': [Point(x=-150, y=-292), Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2322313, 'final': False, 'length': 26}, {'hull': [Point(x=156, y=-286), Point(x=-150, y=-292), Point(x=-22, y=30)], 'final': True}, {'hull': [Point(x=-22, y=30), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2108573, 'final': False, 'length': 24}, {'hull': [Point(x=-22, y=30), Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'weight': 2023468, 'final': False, 'length': 23}, {'hull': [Point(x=-248, y=242), Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1362809, 'final': False, 'length': 11}, {'hull': [Point(x=-22, y=30), Point(x=-248, y=242), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=5, y=241), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1202779, 'final': False, 'length': 9}, {'hull': [Point(x=5, y=241), Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30)], 'weight': 1185614, 'final': False, 'length': 8}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241)], 'weight': 955421, 'final': False, 'length': 6}, {'hull': [Point(x=156, y=-286), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 917945, 'final': False, 'length': 4}, {'hull': [Point(x=156, y=-286), Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241), Point(x=278, y=-130)], 'weight': 786405, 'final': False, 'length': 3}, {'hull': [Point(x=5, y=241), Point(x=278, y=-130), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=9, y=88), Point(x=-22, y=30), Point(x=5, y=241)], 'final': True}, {'hull': [Point(x=278, y=-130), Point(x=299, y=-255), Point(x=156, y=-286)], 'final': True}, {'hull': [Point(x=144, y=75), Point(x=111, y=164), Point(x=278, y=-130)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 653482, 'final': False, 'length': 11}, {'hull': [Point(x=-145, y=-149), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 564693, 'final': False, 'length': 9}, {'hull': [Point(x=-145, y=-149), Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 539681, 'final': False, 'length': 8}, {'hull': [Point(x=-106, y=41), Point(x=-145, y=-149), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-170, y=31), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 469035, 'final': False, 'length': 6}, {'hull': [Point(x=-170, y=31), Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242), Point(x=-106, y=41)], 'weight': 431658, 'final': False, 'length': 5}, {'hull': [Point(x=-248, y=242), Point(x=-106, y=41), Point(x=-170, y=31)], 'final': True}, {'hull': [Point(x=-179, y=38), Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'weight': 316162, 'final': False, 'length': 3}, {'hull': [Point(x=-248, y=242), Point(x=-179, y=38), Point(x=-299, y=-113)], 'final': True}, {'hull': [Point(x=-299, y=-113), Point(x=-308, y=201), Point(x=-248, y=242)], 'final': True}, {'hull': [Point(x=-106, y=41), Point(x=-130, y=-241), Point(x=-145, y=-149)], 'final': True}]

# for instance_no, dots in enumerate(instances_23 + instances_22 + instances_21 + instances_20 + instances_19 + instances_18 + instances_17 + instances_16 + instances_15):
for instance_no in range(instances_no):
    dots = []
    dots_quantity = random.randint(min_dots_quantity, max_dots_quantity)

    for i in range(0, dots_quantity):
        dot_to_append = Point(x=get_random_from_range(lower_value_limit, upper_value_limit, use_ints, use_gauss), y=get_random_from_range(lower_value_limit, upper_value_limit, use_ints, use_gauss))
        while dot_to_append in dots:
            dot_to_append = Point(x=get_random_from_range(lower_value_limit, upper_value_limit, use_ints, use_gauss), y=get_random_from_range(lower_value_limit, upper_value_limit, use_ints, use_gauss))
        dots.append(dot_to_append)

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
    with open(
            'data/evaluations/evaluations_abc_sa_limited_to_1000_floats_gauss.txt',
            mode='w' if instance_no == 0 else 'a',
            encoding='utf-8') as eval_file:
        eval_file.write(str(instance_no + 1) + '. ')
        eval_file.write('[' + ','.join(str(e) for e in dots) + ']\n')
        eval_file.write('\tInstance size: ' + str(len(dots)) + '\n')
        eval_file.write('\tNumber of runs: ' + str(number_of_runs) + '\n')
        # eval_file.write('\tGCT SE Weight: ' + str(gct_results[1]) + '. ')
        # eval_file.write('Time lapsed: ' + str(gct_results[0]) + 's\n')
        eval_file.write('\tOptimal Weight: ' + str(exhaustive_search_results[1]) + '.\n')
        eval_file.write('\tTime lapsed for exhaustive search: ' + str(exhaustive_search_results[0]) + 's\n\n')

        # Begin of advanced stats evaluation
        try:
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
        except Exception as e:
            print(e)
        # End of advanced stats evaluation

    # # End of results export

if animate:
    helpers.draw.turtle.done()
