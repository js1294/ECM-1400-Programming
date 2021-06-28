"""This is exercise 3."""
from math import ceil
__author__ = "Jack Shaw"


def five_a_side_selector(names: list) -> list:
    """This will distribute the names list into equal teams. """
    length_names = len(names)
    max_team = 5
    if length_names > 20:
        max_team = 6
    number_teams = ceil(length_names / max_team)  # Always rounds up
    teams = [[] for _ in range(0, number_teams)]
    index = 0

    for iterations in range(0, length_names):
        teams[index].append(names[iterations])
        if index == number_teams - 1:
            index = 0
        else:
            index += 1
    return teams


print(five_a_side_selector([1,2,3,4,5,6,7,8,9]))