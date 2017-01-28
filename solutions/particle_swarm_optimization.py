import math
from typing import List

from structures.edge import Edge
from structures.pso_particle import PSOParticle


def initialize_particles(reconstructed_edges: List[Edge],
                         particles_quantity: int,
                         randomise: bool) -> List[PSOParticle]:
    """
    Initializes provided number of initial random solutions.

    Args:
        reconstructed_edges: - List of single solution edges prepared for edge flipping.
        particles_quantity: - Number of particles that are ought to be instantiated.
        randomise: - Boolean flag. If True, the particles will be scattered around the search space.
            Otherwise, all instantiated particles will be as same as the initial solution,
            provided with reconstructed edges.

    Returns:
        List of initial random solutions.
    """

    return [PSOParticle(reconstructed_edges, randomise) for _ in range(particles_quantity)]


def basic_pso(reconstructed_edges: List[Edge],
              particles_quantity: int,
              number_of_iterations: int,
              randomised: bool):
    """
    Basic PSO implementation.

    Args:
        reconstructed_edges: - List of single solution edges prepared for edge flipping.
        particles_quantity: - Number of particles that are ought to be instantiated.
        number_of_iterations: - Number of iterations before PSO terminates.
        randomised: - Boolean flag. If True, the initial particles will be scattered around the search space.
            Otherwise, all instantiated particles will be as same as the initial solution,
            provided with reconstructed edges.

    Returns:
        Weight of the best found solution.
    """

    particles = initialize_particles(reconstructed_edges=reconstructed_edges,
                                     particles_quantity=particles_quantity,
                                     randomise=randomised)
    global_best = math.inf

    for _ in range(number_of_iterations):
        for particle in particles:
            if particle.is_personal_best_deprecated():
                particle.update_personal_best()
            if particle.get_personal_best() > global_best:
                global_best = particle.get_personal_best()

        for particle in particles:
            particle.set_velocity(global_best)
            particle.update_solution()
