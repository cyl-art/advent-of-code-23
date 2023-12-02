"""
Day 2: https://adventofcode.com/2023/day/2

A box has some cubes which are either red, green, or blue. Cubes are put back in
the box after each subset of the game. For each subset of each game, a random
number of cubes is taken out of the box and count of cubes of each color is
recorded per subset in the following example format where subsets are separated
by semicolons:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

The first part required checking whether each subset of a game can be played
given initial constraints on the number of cubes available - 12 red, 13 green,
and 14 blue.
The second part required checking minimum number of cubes needed for each game.
"""

from typing import Tuple, List, Union

def process_game(line: str) -> Tuple[int, List[List[Union[int, str]]]]:
    """
    Process each game line: extract game id and information about each subset of
    the game.

    Args:
        line (str): game line

    Returns:
        Tuple[int, List[List[int, str]]]: game id and subset info in the
        following format: [[number_of_cubes, color, ... ], ...]
    """
    game_info = line.split(":")
    game_id, game_info = game_info[0], game_info[1]

    game_id = int(game_id.split(' ')[1])
    subsets = game_info.split(';')
    res = []
    for subset in subsets:
        info = subset.split(' ')
        # first el in info is an empty string from initial space char, remove it
        info = [el.replace(',', '') for el in info[1:]]
        res.append(info)
    return game_id, res

def game_id_possible(line: str) -> int:
    """
    Return game id if this game is possible given constraints or 0 otherwise.

    Args:
        line (str): game line

    Returns:
        int: game id or 0
    """
    game_id, subsets = process_game(line)
    for info in subsets:
        for i in range(0, len(info)-1, 2):
            if ((info[i+1] == "red" and int(info[i]) > 12) or
                (info[i+1] == "green" and int(info[i]) > 13) or
                (info[i+1] == "blue" and int(info[i]) > 14)):
                return 0

    return game_id

def game_power(line: str) -> int:
    """
    Return game power for the current game. Game power is the product of max
    number of red, green, and blue cubes in all subsets of the game.

    Args:
        line (str): game line

    Returns:
        int: game power
    """
    _, subsets = process_game(line)
    red_max, green_max, blue_max = 0, 0, 0
    for info in subsets:
        for i in range(0, len(info)-1, 2):
            if info[i+1] == "red":
                red_max = max(int(info[i]), red_max)
            elif info[i+1] == "green":
                green_max = max(int(info[i]), green_max)
            elif info[i+1] == "blue":
                blue_max = max(int(info[i]), blue_max)
    return red_max * green_max * blue_max


def driver():
    """
    Driver function for reading the input file and printing output. Use
    test_short.txt for a shorter version of input.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    res1, res2 = 0, 0
    for line in lines:
        line = line.strip('\n')
        # for Part 1
        res1 += game_id_possible(line)

        # for Part 2
        res2 += game_power(line)

    print(f"Sum for Part 1 is {res1}, sum for Part 2 is: {res2}")

if __name__ == "__main__":
    driver()
