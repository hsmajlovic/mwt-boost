from typing import List

from libraries.cg_lib import randomise_solution
from structures.edge import Edge


class PSOParticle:
    """
    Class representing a single PSO particle.
    """

    def __init__(self,
                 reconstructed_edges: List[Edge],
                 randomise: bool = False
                 ):
        """
        PSOParticle constructor.

        Args:
            reconstructed_edges: - List of single solution edges prepared for edge flipping.
            randomise:  - Boolean flag. If True, the initial solution will be randomly placed somewhere
            within the search space.
            Otherwise, it will remain the same.
        """

        self.reconstructed_edges = randomise_solution(reconstructed_edges) if randomise else reconstructed_edges
