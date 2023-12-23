"""
Day 23: https://adventofcode.com/2023/day/23

In both parts, the task was to find the longest path from start to finish on the
grid, never stepping on the same cell twice. Cells marked '#' where not allowed
to step on. For part 1, if cell is any of the following - '>', '<', 'v', '^',
the next step can only be in the direction pointed to by the cell. In Part 2,
this rule is removed and these cells are trated as regular path cells ('.').

One thing to notice is that the path is mostly linear, i.e., there is only one
neighboring path cell on which we can step. Thus, getting coordinates of the
cells which have 3 or more neighbors and thus require our choice and then
building a graph form these cells (using adjacency list) allows to run dfs on
this graph to find the longest path.
"""

from typing import List, Tuple, Dict

# type aliases
Graph = Dict[Tuple, Dict[Tuple, int]]

def is_valid_loc(grid: List[str], cell: Tuple[int]) -> bool:
    """
    Determine if the given location is valid.

    Args:
        grid (List[str]): input grid
        cell (Tuple[int]): current location

    Returns:
        bool: True if current location is valid, False otherwise
    """
    return 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0])

def get_start_finish(grid: List[str]) -> Tuple[Tuple[int]]:
    """
    Get the locations of the start and finish cell.

    Args:
        grid (List[str]): input grid

    Returns:
        Tuple[Tuple[int]]: locations of the start and finish cells
    """
    start_y, finish_y = 0, 0
    for idx, i in enumerate(grid[0]):
        if i == '.':
            start_y = idx
            break
    for idx, i in enumerate(grid[-1]):
        if i == '.':
            finish_y = idx
            break
    return (0, start_y), (len(grid)-1, finish_y)

def get_nxt_cells_p1(grid: List[str], cell: Tuple[int]) -> List[Tuple[int]]:
    """
    Get locations of the next cells reachable from the current cell according to
    Part 1 rules.

    Args:
        grid (List[str]): input grid
        cell (Tuple[int]): current cell

    Returns:
        List[Tuple[int]]: locations of the next cells reachable from the current
        cell
    """
    if grid[cell[0]][cell[1]] == '>' and is_valid_loc(grid, (cell[0], cell[1] + 1)):
        return[(cell[0], cell[1] + 1)]
    elif grid[cell[0]][cell[1]] == '<' and is_valid_loc(grid, (cell[0], cell[1] - 1)):
        return[(cell[0], cell[1] - 1)]
    elif grid[cell[0]][cell[1]] == '^' and is_valid_loc(grid, (cell[0] - 1, cell[1])):
        return[(cell[0] - 1, cell[1])]
    elif grid[cell[0]][cell[1]] == 'v' and is_valid_loc(grid, (cell[0] + 1, cell[1])):
        return[(cell[0] + 1, cell[1])]
    else:
        res = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (is_valid_loc(grid, (cell[0] + dx, cell[1]+ dy)) and
            grid[cell[0] + dx][cell[1]+ dy] != '#'):
                res.append((cell[0] + dx, cell[1] + dy))
        return res

def get_nxt_cells_p2(grid: List[str], cell: Tuple[int]) -> List[Tuple[int]]:
    """
    Get locations of the next cells reachable from the current cell according to
    Part 2 rules.

    Args:
        grid (List[str]): input grid
        cell (Tuple[int]): current cell

    Returns:
        List[Tuple[int]]: locations of the next cells reachable from the current
        cell
    """
    res = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if (is_valid_loc(grid, (cell[0] + dx, cell[1]+ dy)) and
        grid[cell[0] + dx][cell[1]+ dy] != '#'):
            res.append((cell[0] + dx, cell[1] + dy))
    return res

def get_option_points(grid: List[str], start: Tuple[int], finish: Tuple[int]) -> List[Tuple[int]]:
    """
    Get all the points fro which there is a choice on where to continue path,
    i.e., they have 3 or more neighbors which are not '#'.

    Args:
        grid (List[str]): input grid
        start (Tuple[int]): start location
        finish (Tuple[int]): finish location

    Returns:
        List[Tuple[int]]: points of interest
    """
    points = [start, finish]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == '#':
                continue

            neighbors = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if is_valid_loc(grid, (x+dx, y+dy)) and grid[x+dx][y+dy] != '#':
                    neighbors += 1
            if neighbors >= 3:
                points.append((x, y))

    return points

def build_graph(grid: list[str], points: List[Tuple[int]], p: int) -> Graph:
    """
    Build graph representingcurrent grid based on the interest points.

    Args:
        grid (List[str]): _description_
        points (List[int]): poitns of interest
        p (int): part, either 1 or 2

    Returns:
        Graph: resultant graph
    """
    graph = {p: {} for p in points}

    # construct adjacency list for graph using dfs
    for sx, sy in points:
        stack = [(0, sx, sy)]
        seen = {(sx, sy)}

        while stack:
            steps, nx, ny = stack.pop()

            if steps != 0 and (nx, ny) in points:
                graph[(sx, sy)][(nx, ny)] = steps
                continue

            for xx, yy in get_nxt_cells_p1(grid, (nx, ny)) if p == 1 else get_nxt_cells_p2(grid, (nx, ny)):
                if (xx, yy) not in seen:
                    stack.append((steps + 1, xx, yy))
                    seen.add((xx, yy))
    return graph

def get_max_steps(graph: Graph, start: Tuple[int], finish:Tuple[int]) -> int:
    """
    Get maximum number of steps in the longest route.

    Args:
        graph (Graph): graph representing current grid
        start (Tuple[int]): start location coordinates
        finish(Tuple[int]): finish location coordinates

    Returns:
        int: maximum number of steps
    """
    def dfs(graph, curr, finish, visited=set()):
        if curr == finish:
            return 0

        max_steps = -float("inf")
        visited.add(curr)
        for nxt in graph[curr]:
            if nxt not in visited:
                max_steps = max(max_steps, dfs(graph, nxt, finish, visited) + graph[curr][nxt])
        visited.remove(curr) # there might be a different path to get here
        return max_steps

    return dfs(graph, start, finish)

def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    start, finish = get_start_finish(lines)
    points = get_option_points(lines, start, finish)
    graph1 = build_graph(lines, points, p=1)
    graph2 = build_graph(lines, points, p=2)
    p1 = get_max_steps(graph1, start, finish)
    p2 = get_max_steps(graph2, start, finish)

    print(f"Max steps for part 1 is {p1}")
    print(f"Max steps for part 2 is {p2}")

if __name__ == "__main__":
    driver()
