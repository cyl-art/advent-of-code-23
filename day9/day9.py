"""
Day 9: https://adventofcode.com/2023/day/9

Each line of the input represented a history of a single value, e.g.
'0 3 6 9 12 15'.

Part 1: extrapolate next value in the history, trace the history to zeroes
by computing differences between each value, add a zero at the end of the last
trace line, and then extrapolate each next value in a trace line by adding
the last value of the previous line to the last value of the current line.

Part 2: extrapolate previous value in the history, trace the history to zeroes
by computing differences between each value, add a zero at the beginning of the
last trace line, and then extrapolate each previous value in a trace line by
subtracting first value of the previous line from the first value of the current
line.
"""
from typing import List

class Trace:
    """
    A class to represent a trace of a single history line down to zeroes.
    """
    def __init__(self) -> None:
        self.grid = []
        self.grid_offset = 0
        self.levels = 0

    def add_trace(self, trace: List[str]) -> None:
        """
        Add a single trace to the grid (generates offsets for the trace).

        Args:
            trace (List[str]): a trace to add
        """
        if self.grid_offset > 0:
            trace = [' '] * self.grid_offset + trace + [' '] * self.grid_offset
        self.grid.append(trace)
        self.grid_offset += 1
        self.levels += 1

    def trace_history(self) -> None:
        """
        Generates trace for a single history line (from the original values
        to zeroes).
        """
        diff, grid_x, grid_y, offset = [], 0, 0, 0
        while True:
            if grid_x+1 < len(self.grid[grid_y]) - offset:
                diff.append(str(int(self.grid[grid_y][grid_x+1]) - int(self.grid[grid_y][grid_x])))
                grid_x += 1
            else:
                self.add_trace(diff)
                if all(el == '0' for el in diff):
                    break
                diff = []
                grid_y += 1
                offset += 1
                grid_x = offset

    def predict_next(self) -> int:
        """
        Extrapolates one value forward in the history line.

        Returns:
            int: extrapolated value
        """
        self.trace_history()

        self.grid[self.levels-1].insert(-self.grid_offset+1, '0')
        level_count, offset = self.levels-1, self.grid_offset-1
        while level_count > 0:
            ind_to_insert = -offset+1 if offset > 1 else len(self.grid[level_count-1])
            self.grid[level_count-1].insert(ind_to_insert, str(
                int(self.grid[level_count-1][-offset]) + int(self.grid[level_count][-offset-1])))

            level_count -= 1
            offset -= 1

        return int(self.grid[0][-1])

    def predict_previous(self) -> int:
        """
        Extrapolates one value backwards in the history line.

        Returns:
            int: extrapolated value
        """
        self.trace_history()
        self.grid[self.levels-1].insert(self.grid_offset-1, '0')
        level_count, offset = self.levels-1, self.grid_offset-1
        while level_count > 0:
            self.grid[level_count-1].insert(offset-1, str(
                int(self.grid[level_count-1][offset-1]) - int(self.grid[level_count][offset])))

            level_count -= 1
            offset -= 1

        return int(self.grid[0][0])

def part1(lines: List[str]) -> int:
    """
    Calculate the sum of predicted values according to the rules of Part 1.

    Args:
        lines (List[str]): history of all values

    Returns:
        int: sum of the predicted values
    """
    res = 0
    for line in lines:
        trace = Trace()
        trace.add_trace(line)
        res += trace.predict_next()

    return res

def part2(lines: List[str]) -> int:
    """
    Calculate the sum of predicted values according to the rules of Part 2.

    Args:
        lines (List[str]): history of all values

    Returns:
        int: sum of the predicted values
    """
    res = 0
    for line in lines:
        trace = Trace()
        trace.add_trace(line)
        res += trace.predict_previous()

    return res

def driver():
    """
    Driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip().split(' ') for line in lines]
    p1, p2 = part1(lines), part2(lines)

    print(f"Sum for Part 1 is {p1}")
    print(f"Sum for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
