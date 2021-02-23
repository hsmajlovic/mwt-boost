import time
from copy import deepcopy
from typing import List, Callable, Any, Tuple, Union

from numpy import std, ndarray

from helpers.utils import mean
from structures.edge import Edge


def evaluate_method(exe_method, *args):
    start = time.time()
    solution = exe_method(*args)
    end = time.time()
    return end - start, solution


def single_run(edges: List[Edge], algorithm: Callable, message: str, *algorithm_args) -> Tuple[float, int]:
    """
    Single run evaluator.

    Args:
        edges: - List of single solution edges prepared for edge flipping.
        algorithm: - Method to be evaluated on top of the list of edges.
        *algorithm_args: - Arguments that the algorithm method is ought to receive.
        message: - Info message to display while processing.

    Returns:
        Achieved solution weight and time taken to find it.
    """

    algorithm_edges = deepcopy(edges)
    algorithm_results = evaluate_method(algorithm, algorithm_edges, *algorithm_args)
    print('\t{0}:'.format(message), algorithm_results[0], 's.',
          'Weight:', algorithm_results[1], '\n')

    return algorithm_results


def get_worst_solution_weight(solution_weights: List[Union[int, float]]) -> int:
    """
    Args:
        solution_weights: - List of solution weights

    Returns:
        The worst weight among provided solution weights.
    """

    return max(solution_weights)


def get_best_solution_weight(solution_weights: List[Union[int, float]]) -> int:
    """
    Args:
        solution_weights: - List of solution weights

    Returns:
        The best weight among provided solution weights.
    """

    return min(solution_weights)


def get_mean_solution_weight(solution_weights: List[Union[int, float]]) -> int:
    """
    Args:
        solution_weights: - List of solution weights

    Returns:
        The mean weight among provided solution weights.
    """

    return mean(solution_weights)


def calculate_standard_deviation(solution_weights: List[Union[int, float]]) -> ndarray:
    """
    Args:
        solution_weights: - List of solution weights

    Returns:
        The standard deviation evaluated on top ofprovided solution weights.
    """

    return std(solution_weights)


def output_stats(edges: List[Edge],
                 algorithm: Callable,
                 number_of_runs: int,
                 message: str,
                 eval_file: Any,
                 *algorithm_args
                 ):
    """
    Runs provided algorithm on top of provided edges for a provided number of times and returns writes worst,
        best and mean solution together with standard deviation to provided file.

    Args:
        edges: - List of single solution edges prepared for edge flipping.
        algorithm: - Method to be evaluated on top of the list of edges.
        message: - Info message to display while processing.
        number_of_runs: - Number of times the provided algorithm is ought to be performed.
        eval_file: - File to store the stats to.
        *algorithm_args: - Arguments that the algorithm method is ought to receive.
    """

    all_results = [
        single_run(edges, algorithm, '{0}. {1}'.format(i + 1, message), *algorithm_args)
        for i in range(number_of_runs)
        ]
    all_times = [result[0] for result in all_results]
    all_weights = [result[1] for result in all_results]

    weight_worst = get_worst_solution_weight(all_weights)
    weight_best = get_best_solution_weight(all_weights)
    weight_mean_value = get_mean_solution_weight(all_weights)
    weight_standard_deviation = calculate_standard_deviation(all_weights)

    time_mean_value = get_mean_solution_weight(all_times)

    eval_file.write('\t{0} worst: {1}\n'.format(message, weight_worst))
    eval_file.write('\t{0} mean: {1}\n'.format(message, weight_mean_value))
    eval_file.write('\t{0} best: {1}\n'.format(message, weight_best))
    eval_file.write('\t{0} standard deviation: {1}\n'.format(message, weight_standard_deviation))
    eval_file.write('\t{0} average time: {1}s \n\n'.format(message, time_mean_value))
