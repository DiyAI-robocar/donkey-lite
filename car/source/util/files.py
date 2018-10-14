"""
Utilities to manipulate files and directories.
"""

import glob
import os


def expand_path_mask(path: str) -> list:
    """
    ToDo
    :param path: Todo
    :return: ToDo
    """
    matches = []
    path = os.path.expanduser(path)
    for file in glob.glob(path):
        if os.path.isdir(file):
            matches.append(os.path.join(os.path.abspath(file)))
    return matches


def expand_path_arg(path_str: str) -> list:
    """
    ToDo
    :param path_str: ToDo
    :return: ToDo
    """
    path_list = path_str.split(",")
    expanded_paths = []
    for path in path_list:
        paths = expand_path_mask(path)
        expanded_paths += paths
    return expanded_paths
