from copy import deepcopy
from typing import List

from libraries.cg_lib import randomise_solution
from structures.edge import Edge


class PSOParticle:
    """
    Class representing a single PSO particle.
    """

    def __init__(self,
                 reconstructed_edges: List[Edge],
                 initial_weight: int,
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
        self.velocity = 0  # TODO: Check the best practice for setting initial velocity

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


