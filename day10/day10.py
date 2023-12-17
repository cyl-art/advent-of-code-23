"""
Day 10: https://adventofcode.com/2023/day/10

There is an animal running in the pipe maze. Example input (structure of the maze):

.....
.S-7.
.|.|.
.L-J.
.....

'S' indicates the start point of the maze. All the symbols except dots indicate
connecting components of pipes.

Part 1: calculate the number of steps it would take to get to furthest from start
point in the maze (regardless of direction). My solution uses BFS.

Part 2: calculate the number of points which are "within" the maze, i.e., are
bounded by the maze. Credit to https://www.youtube.com/watch?v=ObIshEUQmVE for
introducing Point in Poligon algorithm and explaining the reasoning in the
cases where an animal can "squeeze between" the pipes.
"""
import math
from collections import deque
from typing import List, Tuple, Set

class Cell:
    """
    A class to represent individual cell on a grid.
    """
    def __init__(self, x: int, y: int, label: str):
        self.x = x
        self.y = y
        self.label = label
        self.in_loop = False

    def __eq__(self, other):
        return self.label == other.label and self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x + self.y) * 23

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, label: {self.label}"

class Grid:
    """
    A class to represent the entire grid.
    """
    def __init__(self, rows: int):
        self.grid = [[] for _ in range(rows)]
        self.grid_len = 0
        self.row_len = 0

    def populate(self, lines: List[str]) -> None:
        """
        Populate the grid with input.

        Args:
            lines (List[str]): input lines
        """
        rows, cols = len(lines), len(lines[0])
        for x in range(rows):
            for y in range(cols):
                self.grid[x].append(Cell(x, y, lines[x][y]))

        self.grid_len = len(self.grid)
        self.row_len = len(self.grid[0])

    def is_valid_loc(self, x: int, y: int) -> bool:
        """
        Determine if the given location is on the grid.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            bool: True if the location is on the grid, False otherwise
        """
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return True
        return False

    def find_start(self) -> Tuple[int]:
        """
        Find coordinates of the start position.

        Returns:
            Tuple[int]: coordinates of the start position
        """
        rows, cols = len(self.grid), len(self.grid[0])
        for x in range(rows):
            for y in range(cols):
                if self.grid[x][y].label == 'S':
                    return x, y

    def does_piece_fit(self, curr: Cell, nxt: Cell, possible_starts: Set[str]) -> bool:
        """
        Determine if the piece of the pipe on the grid fits in between the curr
        and nxt cells, i.e., determine if we can get to the next cell from this
        curr cell. Warning: this method modifies possible_starts set to determine
        the type of the start pipe.

        Args:
            curr (Cell): current cell
            nxt (Cell): nect cell
            possible_starts (Set[str]): possible pipe labels for the start pipe

        Returns:
            bool: True if the piece of grid fits, False otherwise
        """
        north, south, west, east = (-1, 0), (1, 0), (0, -1), (0, 1)
        if (curr.label in "S|JL" and (nxt.x == curr.x + north[0]) and
            (nxt.y == curr.y + north[1]) and nxt.label in "|F7"):
            if curr.label == 'S':
                possible_starts &= {'|', 'J', 'L'}
            return True
        if (curr.label in "S|F7" and (nxt.x == curr.x + south[0]) and
            (nxt.y == curr.y + south[1]) and nxt.label in "|JL"):
            if curr.label == 'S':
                possible_starts &= {'|', 'F', '7'}
            return True
        if (curr.label in "S-7J" and (nxt.x == curr.x + west[0]) and
            (nxt.y == curr.y + west[1]) and nxt.label in "-FL"):
            if curr.label == 'S':
                possible_starts &= {'-', '7', 'J'}
            return True
        if (curr.label in "S-FL" and (nxt.x == curr.x + east[0]) and
            (nxt.y == curr.y + east[1]) and nxt.label in "-7J"):
            if curr.label == 'S':
                possible_starts &= {'-', 'F', 'L'}
            return True

        return False

    def traverse(self, start: Cell) -> List[Cell]:
        """
        Traverse the grid from the start position using BFS. Warning: this method
        replaces 'S' label with the actual pipe label at the start position.

        Args:
            start (Cell): start position

        Returns:
            List[Cell]: list of seen nodes, i.e., nodes which are part of the loop
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        possible_starts = {'|', '-', 'L', 'J', 'F', '7'}
        seen = [start]
        start.in_loop = True
        queue = deque([start])

        while queue:
            curr = queue.popleft()
            for dx, dy in directions:
                if self.is_valid_loc(dx + curr.x, dy + curr.y):
                    nxt = self.grid[curr.x+dx][curr.y+dy]
                    if self.does_piece_fit(curr, nxt, possible_starts) and not (nxt in seen):
                        nxt.in_loop = True
                        seen.append(nxt)
                        queue.append(nxt)

        # replace 'S' with the actual label
        start_val = possible_starts.pop()
        start.label = start_val

        return seen

    def count_pipes_to_the_left(self, row_ind: int, col_ind: int) -> int:
        """
        Implement Ray in Poligon algorithm to determine if a point is inside or
        outside the bounds - inside if the count is odd, outside otherwise.
        See comment in the code for reasoning in cases when animal can "squeeze
        between" the pipes.

        Args:
            row_ind (int): row index of the cell in question
            col_ind (int): column index of the cell in question

        Returns:
            int: the number of times a ray shot from a point outside of a polygon
            crosses its boundaries
        """
        count = 0
        for j in range(col_ind+1):
            cell = self.grid[row_ind][j]
            # we need to track only "up" or "down" cells to make sure we are
            # actually crossing the boundary and not "squeezing through it",
            # I chose to track "up". If we track all cells, animal can "squeeze
            # between the pipes" - both ends of the pipe fragment can point
            # in the same direction and the animal will not cross the boundary
            if cell.label in ('|', 'J', 'L') and cell.in_loop:
                count += 1
        return count

    def get_max_steps(self, path: List[Cell]) -> int:
        """
        Get the number of steps to the furthest location from the start.

        Args:
            path (List[Cell]): all cells in the loop

        Returns:
            int: the number of steps to the furthest location from the start
        """
        return math.ceil(len(path) / 2)

    def part2(self) -> int:
        """
        Compute the answer for Part 2 - calculate how many cells are within the
        maze.

        Returns:
            int: the number of cells within the maze
        """
        cells_inside = 0
        for row_ind in range(self.grid_len):
            for col_ind in range(self.row_len):
                cell = self.grid[row_ind][col_ind]
                if not cell.in_loop:
                    is_odd = self.count_pipes_to_the_left(row_ind, col_ind) % 2 == 1
                    cells_inside += 1 if is_odd else 0
        return cells_inside


def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    grid = Grid(len(lines))
    grid.populate(lines)

    start_x, start_y = grid.find_start()
    path = grid.traverse(grid.grid[start_x][start_y])

    p1 = grid.get_max_steps(path)
    p2 = grid.part2()

    print(f"Answer for Part 1 is {p1}")
    print(f"Answer for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
