"""
Day 11: https://adventofcode.com/2023/day/11

Input is a grid where galaxies are represented as '#' and voids as '.':

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

Part 1 & Part 2: after performing cosmic expansion on the grid (factor of 2
in part 1, factor of 1000000 in part 2), calculate the total number of steps it
takes to get from any one galaxy to another galaxy.
"""
from typing import List, Tuple

# type aliases
Galaxies = List[Tuple[int]]

class Grid:
    """
    A class to represent a grid as a 2D list.
    """
    def __init__(self):
        self.grid = []

    def populate(self, lines: List[List[str]]) -> None:
        """
        Populate a grid from a 2D list.

        Args:
            lines (List[List[str]]): input list
        """
        for line in lines:
            self.grid.append(line)

    def manhattan_dist(self, galaxy1: Tuple[int], galaxy2: Tuple[int]) -> int:
        """
        Calculate the manhattan distance between two points.

        Args:
            galaxy1 (Tuple[int]): point 1
            galaxy2 (Tuple[int]): point 2

        Returns:
            int: the manhattan distance between two points
        """
        return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

    def expanded_before(self, expansions: List[int], coord: int) -> int:
        """
        Count how many rows/cols were expanded before the current row/col.

        Args:
            expansions (List[int]): rows/cols to expand
            coord (int): current row/col

        Returns:
            int: number of rows/cols that were expanded before the current
            row/col
        """
        if coord < expansions[0]:
            return 0
        if coord > expansions[-1]:
            return len(expansions)

        count = 0
        for i in range(len(expansions)-1):
            count += 1
            if expansions[i] < coord < expansions[i+1]:
                return count

    def get_rows_cols_to_expand(self) -> Tuple[List[int]]:
        """
        Determine which rows/cols need to be expanded.

        Returns:
            Tuple[List[int]]: rows/cols that need to be expanded
        """
        rows_to_expand, cols_to_expand = [], []
        has_galaxy = False
        for ind, row in enumerate(self.grid):
            for cell in row:
                if cell == '#':
                    has_galaxy = True

            if not has_galaxy:
                rows_to_expand.append(ind)
            has_galaxy = False

        for col_ind in range(len(self.grid[0])):
            for row_ind in range(len(self.grid)):
                if self.grid[row_ind][col_ind] == '#':
                    has_galaxy = True

            if not has_galaxy:
                cols_to_expand.append(col_ind)
            has_galaxy = False
        return rows_to_expand, cols_to_expand

    def get_coords_after_expansion(self, galaxies: Galaxies, factor: int) -> Galaxies:
        """
        Calculate galaxy coordinates after the expansion.

        Args:
            galaxies (Galaxies): initial galaxy coordinates
            factor (int): factor of expansion

        Returns:
            Galaxies: resultant galaxy coordinates
        """
        rows_to_expand, cols_to_expand = self.get_rows_cols_to_expand()
        new_galaxies = []
        for galaxy_row, galaxy_col in galaxies:
            new_row = galaxy_row + self.expanded_before(
            rows_to_expand, galaxy_row) * (factor - 1)
            new_col = galaxy_col + self.expanded_before(
            cols_to_expand, galaxy_col) * (factor - 1)
            new_galaxies.append((new_row, new_col))
        return new_galaxies

    def find_galaxies(self) -> Galaxies:
        """
        Find galaxy coordinates.

        Returns:
            Galaxies: galaxy coordinates
        """
        galaxies = []
        for row_ind, row in enumerate(self.grid):
            for col_ind, _ in enumerate(row):
                if row[col_ind] == '#':
                    galaxies.append((row_ind, col_ind))
        return galaxies

    def get_steps(self, galaxies: Galaxies) -> int:
        """
        Calculate the total number of steps needed to get from one galaxy
        to a different galaxy (not repeating galaxy 1, galaxy 2 & galaxy 2, galaxy 1)

        Args:
            galaxies (Galaxies): list of galaxies

        Returns:
            int: total number of steps needed to get from one galaxy
            to a different galaxy
        """
        steps = 0
        for i in range(len(galaxies)):
            for j in range(1+i, len(galaxies)):
                steps += self.manhattan_dist(galaxies[i], galaxies[j])
        return steps


def driver():
    """
    Driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [[el for el in line if el != '\n'] for line in lines]

    grid = Grid()
    grid.populate(lines)
    galaxies = grid.find_galaxies()
    galaxies_after_expansion1 = grid.get_coords_after_expansion(galaxies, factor=2)
    galaxies_after_expansion2 = grid.get_coords_after_expansion(galaxies, factor=1000000)
    p1, p2 = grid.get_steps(galaxies_after_expansion1), grid.get_steps(galaxies_after_expansion2)

    print(f"Sum for Part 1 is {p1}")
    print(f"Sum for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
