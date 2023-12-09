"""
Day 8: https://adventofcode.com/2023/day/8

According to the transfer rules between nodes provided and the directions,
calculate the number of steps it takes to get from start node to the end node.

Part 1: start node is "AAA", end node is "ZZZ"

Part 2: start nodes must end with an 'A', end nodes must end with a 'Z'.
transfer between all start and end nodes is conducted in parallel.
Note: brute-force approach needed to be optimized by calculating number of
steps required to reach end position from each start node and then computing
lowest common multiple (LCM).
"""
from typing import Dict, List, Tuple
import math

LEFT = 0
RIGHT = 1

# type aliases
Grid = Dict[str, Tuple[str]]

def part1(directions: List[str], network: Grid, curr_loc="AAA") -> int:
    """
    Calculate the number of steps required to reach "ZZZ" location according to
    Part 1 rules.

    Args:
        directions (List[str]): list of directions
        network (Grid): transfer rules between nodes
        curr_loc (str, optional): start location in the grid. Defaults to "AAA".

    Returns:
        int: number of steps required to reach destination
    """
    step_count, dir_idx, dir_len = 0, 0, len(directions)

    while curr_loc != "ZZZ":
        if dir_idx >= dir_len:
            dir_idx = 0

        curr_dir = directions[dir_idx]
        if curr_dir == 'L':
            curr_loc = network[curr_loc][LEFT]
        if curr_dir == 'R':
            curr_loc = network[curr_loc][RIGHT]

        step_count += 1
        dir_idx += 1

    return step_count

def part2(directions: List[str], network: Grid, curr_locs: List[str]) -> int:
    """
    Calculate the number of steps required to reach a position ending with 'Z'
    starting from all start locations simultaneously according to Part 2 rules.

    Args:
        directions (List[str]): list of directions
        network (Grid): transfer rules between nodes
        curr_locs (List[str]): list of start locations in the grid

    Returns:
        int: number of steps required to reach all destinations
    """
    loc_counts, dir_idx, dir_len = {}, 0, len(directions)
    for loc in curr_locs:
        step_count = 0
        while loc[-1] != 'Z':
            if dir_idx >= dir_len:
                dir_idx = 0

            curr_dir = directions[dir_idx]
            if curr_dir == 'L':
                loc = network[loc][LEFT]
            if curr_dir == 'R':
                loc = network[loc][RIGHT]

            step_count += 1
            dir_idx += 1

        loc_counts[loc] = step_count

    return math.lcm(*loc_counts.values())

def process_input(lines: List[str]) -> Tuple[int]:
    """
    Extract network transfer rules and compute answers for Part 1 and Part 2.

    Args:
        lines (List[str]): lines with direction and grid information

    Returns:
        Tuple[int]: answers for Part 1 and Part 2
    """
    directions = lines[0]
    network = {}
    for line in lines[2:]:
        # extract node and connection info
        node = line[:3]
        left, right = line[7:10], line[12:15]
        network[node] = (left, right)

    curr_locs = [key for key in network if key[-1] == 'A']
    p1 = part1(directions, network)
    p2 = part2(directions, network, curr_locs)
    return p1, p2

def driver():
    """
    Driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    p1, p2 = process_input(lines)
    print(f"Number of steps required in Part 1 is {p1}")
    print(f"Number of steps required in Part 2 is {p2}")

if __name__ == "__main__":
    driver()
