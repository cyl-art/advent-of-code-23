"""
Day 17: https://adventofcode.com/2023/day/17

Given an input grid where each cell indicates heat less when entering the
corresponding block, calculate the minimum heat loss possible starting from (0,0)
and going to (grid_len-1, grid_len-1) according to defined rules of movement in
parts 1 and 2.
Improvement: using Dijkstra's algorithm instead of BFS with checking curr loss
of the path.
"""
from heapq import heappop, heappush
from typing import List, Tuple

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def get_opposite_dir(direction: Tuple[int]) -> Tuple[int]:
    """
    Get the direction opposite to current one.

    Args:
        direction (Tuple[int]): current direction

    Returns:
        Tuple[int]: opposite direction
    """
    if direction == UP:
        return DOWN
    if direction == DOWN:
        return UP
    if direction == RIGHT:
        return LEFT
    if direction == LEFT:
        return RIGHT

def get_possible_dirs(curr_dir: Tuple[int], straight_count: int, p: int) -> List[Tuple[int]]:
    """
    Get all possible directions from the current one considering part and count
    of cells in the same direction.

    Args:
        curr_dir (Tuple[int]): current direction
        straight_count (int): number of cells in the same direction
        p (int): part number, either 1 or 2

    Returns:
        List[Tuple[int]]: all possible directions from the current one
    """
    possible_dirs = [UP, DOWN, LEFT, RIGHT]
    res = []
    if p == 1: # part 1
        for direction in possible_dirs:
            if direction != get_opposite_dir(curr_dir):
                if direction == curr_dir and straight_count < 3:
                    res.append(direction)
                elif direction != curr_dir:
                    res.append(direction)
    else: # part 2
        for direction in possible_dirs:
            if direction != get_opposite_dir(curr_dir):
                if direction == curr_dir and straight_count < 10:
                    res.append(direction)
                elif direction != curr_dir and straight_count >= 4:
                    res.append(direction)
    return res

def is_valid_loc(x: int, y: int, grid: List[List[int]]) -> bool:
    """
    Determine if the given location is on the grid.

    Args:
        x (int): x coordinate
        y (int): y coordinate
        grid (List[List[int]]): grid

    Returns:
        bool: True if the given location is on the grid, False otherwise
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def dijkstra(grid: List[List[int]], start: Tuple[int], finish: Tuple[int], p: int) -> int:
    """
    Use Dijkstra's algorithm to calculate the minimum heat loss when starting from
    a given start location and moving to given finish location, considering different
    rules for Part 1 and Part 2.

    Args:
        grid (List[List[int]]): grid
        start (Tuple[int]): start location
        finish (Tuple[int]): finish location
        p (int): part number, either 1 or 2

    Returns:
        int: minimum heat loss possible
    """

    # each entry in the priority queue has the following format:
    # cost (heat loss), start coords, dir coords, straight count (count of steps
    # in the same direction)
    pr_queue, visited = [], set()
    start1 = (int(grid[start[0]][start[1]+1]), (start[0], start[1]+1), RIGHT, 1)
    start2 = (int(grid[start[0]+1][start[1]]), (start[0]+1, start[1]), DOWN, 1)
    pr_queue.append(start1)
    pr_queue.append(start2)

    while pr_queue:
        curr = heappop(pr_queue)
        heat_loss, curr, curr_dir, straight_count = curr

        if curr == finish:
            if p == 2 and straight_count >= 4: # part 2 exit condition
                return heat_loss
            elif p == 1:
                return heat_loss # part 1

        if (curr, curr_dir, straight_count) in visited:
            continue

        visited.add((curr, curr_dir, straight_count))
        dirs = get_possible_dirs(curr_dir, straight_count, p)
        for direction in dirs:
            nxt = (curr[0]+direction[0], curr[1]+direction[1])
            if not is_valid_loc(nxt[0], nxt[1], grid):
                continue
            nxt_heat_loss = grid[nxt[0]][nxt[1]]
            new_count = straight_count+1 if direction == curr_dir else 1
            heappush(pr_queue, (heat_loss+nxt_heat_loss, nxt, direction, new_count))

def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    grid = [[int(el) for el in line] for line in lines]
    grid_len, row_len = len(grid), len(grid[0])
    start, finish = (0, 0), (grid_len-1, row_len-1)
    p1, p2 = dijkstra(grid, start, finish, p=1), dijkstra(grid, start, finish, p=2)

    print(f"Min loss for Part 1 is {p1}")
    print(f"Min loss for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
