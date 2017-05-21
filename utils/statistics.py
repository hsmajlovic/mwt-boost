""" Module containing statistics eval tools """
from typing import List, Union

import numpy as np


def theil_index(l: List[Union[int, float]]) -> float:
    """
    Args:
        l: List of ints/floats.

    Returns:
        Theil index (https://en.wikipedia.org/wiki/Theil_index) of input list.

    """
    mean = np.mean(l)
    return sum(elem / mean * np.log(elem / mean) for elem in l) / len(l)
