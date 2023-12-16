"""
Day 16: https://adventofcode.com/2023/day/16

Input contains the grid where beams of light travel:

|.-.\\.....

'|' is a vertical splitter, '-' is a horizontal splitter, '/',  and '\\' are
mirrors. Mirrors reflect a beam 90 degrees from where it was travelling. Splitters
split the beam if it does not hit them from their ends. A cell is called energized
if at least one beam passed through it.

Part 1: count the number of eneregized cells if the beam starts at top left (0,0)
position and travells right.

Part 2: find the max number of energized cells possible if the beam can start
top row (moving down), bottom row (moving up), first col (moving right), or
last col (moving left).
"""
from typing import List, Tuple, Union

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

class Cell:
    """
    A class to represent cell in the grid.
    """
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.directions_from = []
        self.counted = False

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, label: {self.label}, counted: {self.counted}"

class Grid:
    """
    A class to represent the grid.
    """
    def __init__(self, lines: List[str]):
        self.grid = []
        self.grid_len = 0
        self.row_len = 0
        self.lines = lines
        self.populate()

    def clear_grid(self):
        """
        Clear the grid after starting the beam from different cells.
        """
        self.grid = []
        self.populate()

    def is_valid_loc(self, row_ind: int, col_ind: int) -> bool:
        """
        Determine if the given location is valid.

        Args:
            row_ind (int): row index
            col_ind (int): column index

        Returns:
            bool: True if the given location is valid, False otherwise
        """
        return 0 <= row_ind < self.grid_len and 0 <= col_ind < self.row_len

    def populate(self) -> None:
        """
        Populate the grid with cells.

        Args:
            lines (List[str]): input lines
        """
        for row_ind, row in enumerate(self.lines):
            curr_row = []
            for col_ind, _ in enumerate(row):
                curr_row.append(Cell(row_ind, col_ind, self.lines[row_ind][col_ind]))
            self.grid.extend([curr_row])

        self.grid_len = len(self.grid)
        self.row_len = len(self.grid[0])

    def get_opposite_dir(self, direction: Tuple[int]) -> Tuple[int]:
        """
        Get the direction opposite to the given one.

        Args:
            direction (Tuple[int]): given direction

        Returns:
            Tuple[int]: the opposite direction
        """
        if direction == RIGHT:
            return LEFT
        if direction == LEFT:
            return RIGHT
        if direction == UP:
            return DOWN
        if direction == DOWN:
            return UP

    def update_dir(self, direction: Tuple[int], cell_row: int, cell_col: int) -> Tuple[Union[bool, Tuple[int]]]:
        """
        Update current directin based on the label of the tile and determine if
        the beam is split.

        Args:
            direction (Tuple[int]): current direction
            cell_row (int): row of the current cell
            cell_col (int): column of the current cell

        Returns:
            Tuple[Union[bool, Tuple[int]]]: True if the beam is split, False
            otherwise and an updated direction
        """
        cell = self.grid[cell_row][cell_col]
        if cell.label == '/':
            if direction == RIGHT:
                return False, UP
            elif direction == LEFT:
                return False, DOWN
            elif direction == UP:
                return False, RIGHT
            elif direction == DOWN:
                return False, LEFT
        elif cell.label == '\\':
            if direction == RIGHT:
                return False, DOWN
            elif direction == LEFT:
                return False, UP
            elif direction == UP:
                return False, LEFT
            elif direction == DOWN:
                return False, RIGHT
        elif cell.label == '|' and (direction == RIGHT or direction == LEFT):
            return True, UP
        elif cell.label == '-' and (direction == UP or direction == DOWN):
            return True, RIGHT
        else:
            return False, direction

    def count_energized(self, start_row: int, start_col: int, start_dir: Tuple[int]) -> int:
        """
        Cound energized cells if the beam starts at current start location.

        Args:
            start_row (int): starting row
            start_col (int): starting column
            start_dir (Tuple[int]): starting direction

        Returns:
            int: number of energized cells
        """
        energized, beam_queue = 0, [(start_row, start_col, start_dir)]
        while beam_queue:
            beam = beam_queue.pop()
            curr_row, curr_col, direction = beam[0], beam[1], beam[2]
            while True:
                is_split, new_dir = self.update_dir(direction, curr_row, curr_col)
                if not self.grid[curr_row][curr_col].counted:
                    energized += 1
                    self.grid[curr_row][curr_col].counted = True

                if is_split:
                    beam_queue.append((curr_row, curr_col, self.get_opposite_dir(new_dir)))

                curr_row, curr_col, direction = curr_row + new_dir[0], curr_col + new_dir[1], new_dir
                if (not self.is_valid_loc(curr_row, curr_col) or
                    direction in self.grid[curr_row][curr_col].directions_from):
                    break

                self.grid[curr_row][curr_col].directions_from.append(direction)

        return energized

    def part1(self) -> int:
        """
        Get the answer to Part 1.

        Returns:
            int: number of energized cells if starting from the top left cell
        """
        return self.count_energized(0, 0, RIGHT)

    def part2(self) -> int:
        """
        Get the answer to Part 2.

        Returns:
            int: max possible number of energized cells
        """
        max_energized = -1
        for tile in self.grid[0]:
            max_energized = max(max_energized, self.count_energized(tile.x, tile.y, DOWN))
            self.clear_grid()
        for tile in self.grid[-1]:
            max_energized = max(max_energized, self.count_energized(tile.x, tile.y, UP))
            self.clear_grid()
        for row_ind in range(self.grid_len):
            first_col = self.count_energized(row_ind, 0, RIGHT)
            self.clear_grid()
            last_col = self.count_energized(row_ind, self.row_len-1, LEFT)
            self.clear_grid()
            max_energized = max(max_energized, first_col, last_col)

        return max_energized

def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    grid = Grid(lines)
    p1 = grid.part1()
    p2 = grid.part2()

    print(f"Sum for Part 1 is {p1}")
    print(f"Sum for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
