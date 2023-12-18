"""
Day 18: https://adventofcode.com/2023/day/18

Given digging instructions for the lagoon, compute its capacity (sum of
boundary points of the lagoon and its interior points.)

Example input line: R 6 (#70c710)

Part 1: letter is the direction, number is the number of steps in that direction.
Part 2: last digit of the hex number maps to direction, all other digits specify
number of steps.

Used shoelace formula to compute the area of pologon given x and y coords of its
vertices and Pick's theorem to calculate the number of interior points out of the
boundary length and area. Capacity then is the sum of interior points and boundary
length.
"""

from typing import List, Union, Tuple
import numpy as np

DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

def shoelace_formula(x_vertices: List[int], y_vertices: List[int]) -> float:
    """
    Shoelace formula to calculate the area of the polygon given x and y coordinates
    of its vertices. Credit to https://stackoverflow.com/a/30408825.

    Args:
        x_vertices (List[int]): x-coordinates of polygon vertices
        y_vertices (List[int]): corresponding y-coords of polygon vertices

    Returns:
        float: polygon area
    """
    return 0.5 * np.abs(np.dot(x_vertices,np.roll(y_vertices,1))
                        - np.dot(y_vertices,np.roll(x_vertices,1)))

def compute_capacity(instructions: List[List[Union[str, int]]]) -> int:
    """
    Compute the capacity of the specified in the instructions lagoon.

    Args:
        instructions (List[List[Union[str, int]]]): instructions for digging

    Returns:
        int: capacity of the specified lagoon
    """
    boundary_len, x_vertices, y_vertices = generate_boundary(instructions)
    # Use shoelace formula to calculate the area of the polygon with given x and y
    # coordinates of its vertices
    interior_area = shoelace_formula(x_vertices, y_vertices)
    # Use Pick's theorem to calculate the number of interior points:
    # Area = interior_points + boundary_points//2 - 1
    interior_points = interior_area + 1 - boundary_len // 2
    # the entire capacity is the sum of boundary and interior points
    return int(boundary_len + interior_points)

def generate_boundary(instructions: List[List[Union[str, int]]]) -> Tuple[Union[int, list[int]]]:
    """
    Generate boundary for the specified lagoon, find its vertices and length.

    Args:
        instructions (List[List[Union[str, int]]]): instructions for digging

    Returns:
        Tuple[Union[int, list[int]]]: boundary length, x-coords of vertices,
        y-coords of vertices
    """
    boundary, boundary_len = [(0, 0)], 1
    x_vertices, y_vertices = [], []
    for instruction in instructions:
        direction, step_num = instruction[0], instruction[1]
        curr = boundary[-1]
        while step_num > 0:
            curr = (curr[0]+DIRECTIONS[direction][0], curr[1]+DIRECTIONS[direction][1])
            boundary.append(curr)
            boundary_len += 1
            step_num -= 1

        x_vertices.append(boundary[-1][0] + step_num*DIRECTIONS[direction][0])
        y_vertices.append(boundary[-1][1] + step_num*DIRECTIONS[direction][1])

    # exclude repeating start point at the end
    return boundary_len-1, x_vertices, y_vertices

def part1(lines: List[str]) -> int:
    """
    Process digging instructions for Part 1 and compute lagoon capacity.

    Args:
        lines (List[str]): input linex

    Returns:
        int: lagoon capacity
    """
    instructions = []
    for line in lines:
        line_info = line.split(' ')
        instruction = [line_info[0], int(line_info[1])]
        instructions.append(instruction)

    return compute_capacity(instructions)


def part2(lines: List[str]) -> int:
    """
    Process digging instructions for Part 2 and compute lagoon capacity.

    Args:
        lines (List[str]): input linex

    Returns:
        int: lagoon capacity
    """
    dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    instructions = []
    for line in lines:
        line_info = line.split(' ')[2]
        steps = int(line_info[2:7], 16)
        direction = dir_map[line_info[7]]
        instruction = [direction, steps]
        instructions.append(instruction)

    return compute_capacity(instructions)


def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    p1, p2 = part1(lines), part2(lines)

    print(f"Lagoon capacity for Part 1 is {p1}")
    print(f"Lagoon capacity for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
