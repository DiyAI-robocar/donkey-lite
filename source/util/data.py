"""
Assorted functions for manipulating data.
"""
import numpy as np
import itertools


def linear_bin(a: float) -> list:
    """
    Convert a value to a categorical array.

    :param a: Value between -1 and 1
    :return: List of length 15 with one item set to 1, which represents the linear value,
             and all other items set to 0
    """
    a = a + 1
    b = round(a / (2 / 14))
    arr = [0]*15
    arr[int(b)] = 1
    return arr


def linear_unbin(arr: list) -> list:
    """
    Convert a categorical array to value.

    :param arr: Categorical array
    :return: Value array
    """
    if not len(arr) == 15:
        raise ValueError('Illegal array length, must be 15')
    b = np.argmax(arr)
    a = b * (2 / 14) - 1
    return list(a)


def bin_Y(Y: list) -> []:
    """
    Convert a list of values to a list of categorical arrays.

    :param Y: Iterable of int with values between -1 and 1
    :return: A two dimensional array of int
    """
    d = [ linear_bin(y) for y in Y ]
    return np.array(d)


def unbin_Y(y: list) -> list:
    """
    Convert a list of categorical arrays to a list of values.

    :param y: List of categorical arrays
    :return: List of values
    """
    d = [linear_unbin(element) for element in y]
    return list(np.array(d))


def map_range(x: int, x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    """
    Linear mapping between two ranges of values

    :param x: Value from the range x
    :param x_min: Minimum values of the range x
    :param x_max: Maximum values of the range x
    :param y_min: Minimum values of the range y
    :param y_max: Maximum values of the range y
    :return: Linear mapping between two ranges of values
    """
    x_range = x_max - x_min
    y_range = y_max - y_min
    xy_ratio = x_range / y_range

    y = ((x - x_min) / xy_ratio + y_min) // 1

    return int(y)


def merge_two_dicts(x:dict, y:dict) -> dict:
    """
    Given two dicts, merge them into a new dict as a shallow copy

    :param x: First dictionary to merge
    :param y: Second dictionary to merge
    :return: Merged dictionary
    """
    z = x.copy()
    z.update(y)
    return z


def param_gen(params: dict) -> list:
    """
    Accepts a dictionary of parameter options and returns
    a list of dictionary with the permutations of the parameters.

    :param params: Dictionary of parameter options
    :return: List of dictionary with the permutations of the parameters
    """
    for p in itertools.product(*params.values()):
        yield dict(zip(params.keys(), p ))
