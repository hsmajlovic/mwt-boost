import math
from copy import deepcopy
from random import random
from typing import List, Tuple

from libraries.cg_lib import randomise_solution, diagonal_difference, in_convex_square
from solutions.hill_climbing import flip_edge
from structures.edge import Edge


class PSOParticle:
    """
    Class representing a single PSO particle.
    """

    def __init__(self,
                 reconstructed_edges: List[Edge],
                 initial_weight: int,
                 learning_factors: Tuple[int, int] = (2, 2),
                 randomise: bool = False
                 ):
        """
        PSOParticle constructor.

        Args:
            initial_weight: - Initial solution weight.
            reconstructed_edges: - List of single solution edges prepared for edge flipping.
            randomise:  - Boolean flag. If True, the initial solution will be randomly placed somewhere
            within the search space.
            Otherwise, it will remain the same.
        """

        self.reconstructed_edges = deepcopy(reconstructed_edges)
        self.solution_weight = randomise_solution(reconstructed_edges, initial_weight) if randomise else initial_weight
        self.personal_best = self.solution_weight
        self.learning_factors = learning_factors

        self.velocity = 0

    def get_reconstructed_edges(self) -> List[Edge]:
        return self.reconstructed_edges

    def get_solution_weight(self) -> int:
        return self.solution_weight

    def get_personal_best(self) -> int:
        return self.personal_best

    def get_velocity(self) -> int:
        return self.velocity

    def set_reconstructed_edges(self, reconstructed_edges):
        self.reconstructed_edges = reconstructed_edges

    def set_solution_weight(self, solution_weight):
        self.solution_weight = solution_weight

    def set_personal_best(self, personal_best):
        self.personal_best = personal_best

    def set_velocity(self, velocity):
        self.velocity = velocity

    def is_personal_best_deprecated(self) -> bool:
        """
        Checks if current solution weight is better than personal best.

        Returns:
            True if current solution weight is better than personal best. False otherwise.
        """

        return self.solution_weight < self.personal_best

    def update_personal_best(self):
        """
        Updates personal best with the current solution weight iff current weight is better then the personal best.
        """

        self.personal_best = self.solution_weight if self.is_personal_best_deprecated() else self.personal_best

    def calculate_velocity(self, global_best: int) -> float:
        """
        Calculates the velocity of a particle.

        Args:
            global_best: - Global best solution weight.

        Returns:
            Updated velocity of a particle.
        """

        return random() * (self.learning_factors[0] * (self.personal_best - self.solution_weight) +
                           self.learning_factors[1] * (global_best - self.solution_weight))

    def update_solution(self):
        """
        Updates current solution by flipping the edge that
            changes the solution weight for as close to velocity as possible.
        """

        offset = math.inf
        diagonal_diff = 0
        selected_edge = None

        for edge in self.reconstructed_edges:
            if len(edge.incident_dots) == 0:
                continue
            temp_diagonal_diff = diagonal_difference(edge)
            if in_convex_square(edge) and abs(temp_diagonal_diff + self.velocity) < offset:
                offset = abs(temp_diagonal_diff - self.velocity)
                diagonal_diff = temp_diagonal_diff
                selected_edge = edge

        if selected_edge:
            flip_edge(self.reconstructed_edges, selected_edge)
            self.solution_weight -= diagonal_diff
