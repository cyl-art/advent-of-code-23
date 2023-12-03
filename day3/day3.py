"""
Day 3: https://adventofcode.com/2023/day/3

Given an input grid consisting of numbers and symbols, e.g., a line looks like
this: "617*.....", which represents engine schematic.

For Part 1, calculate the sum of numbers which are parts of the engine. A number
is a part of the engine if it has at least one adjacent symbol (even diagonal).
Dots ('.') are not symbols.

For Part 2, calculate the sum of gear ratios. A gear ratio is the product of two
numbers which are adjacent to the same gear ('*'). Star ('*') is a gear only if
it has exactly two adjacent numbers.
"""

from typing import List, Tuple

def process_input(grid: List[str]) -> Tuple(int):
    """
    Function to process each line and calculate sum of the numbers which are
    parts of the engine and sum of gear ratios.

    Args:
        grid (List[str]): input grid

    Returns:
        Tuple(int): p1 - sum of numbers which are parts of the engine (part 1),
        p2 - sum of gear ratios (part 2)
    """
    grid = [row.strip() for row in grid]
    len_grid, len_row = len(grid), len(grid[0])
    p1, p2 = 0, 0
    gear_nums = {}

    for row in range(len_grid):
        gears = set()
        curr_num = 0
        is_part = False
        for col in range(len(grid[row])+1):
            if col < len_row and grid[row][col].isdigit():
                curr_num = curr_num * 10 + int(grid[row][col])
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= row + dr < len_grid and 0 <= col + dc < len_row:
                            char = grid[row+dr][col+dc]
                            if not char.isdigit() and char != '.':
                                is_part = True
                                if char == '*':
                                    gears.add((row+dr, col+dc))
            elif curr_num > 0:
                for gear in gears:
                    gear_nums[gear] = gear_nums.get(gear, []) + [curr_num]
                if is_part:
                    p1 += curr_num
                curr_num = 0
                is_part = False
                gears = set()

    for gear, nums in gear_nums.items():
        if len(nums) == 2:
            p2 += nums[0] * nums[1]

    return p1, p2

def driver():
    """
    Driver function to open and read input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    p1, p2 = process_input(lines)

    print(f"Sum for Part 1 is: {p1}")
    print(f"Sum for Part 2 is: {p2}")

if __name__ == "__main__":
    driver()
