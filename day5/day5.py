"""
Day 5: https://adventofcode.com/2023/day/5

Given a series of maps with transformation instructions, go from seeds to
locations where they need to be planted.

An example map looks like this (there are more layers in between):

seeds: 79 14 55 13

seed-to-location map:
50 98 2
52 50 48

Part 1: find minimum location from all the locations where seeds need to be
planted

Part 2: same task, but treat "seeds" row as ranges, e.g., 79 14 means a range of
seeds which starts at 79, ends at 92 and has 14 seeds. Brute force solution
does not work becaouse of the size of real test input. Solution implemented
here involves some interval math.
"""
from typing import List, Tuple

DEST_START = 0
SOURCE_START = 1
RANGE = 2

def get_maps(lines: List[str]) -> List[Tuple[int]]:
    """
    Get maps from input lines.

    Args:
        lines (List[str]): input

    Returns:
        List[Tuple[int]]: parsed maps
    """
    maps, curr_map = [], []
    for line in lines[2:]:
        map_start = True
        if not (line[0].isdigit() and map_start):
            maps.append(curr_map)
            curr_map = []
            map_start = True
        elif not line[0].isdigit():
            continue
        else:
            map_start = False
            map_piece = [int(el) for el in line.split(' ') if el]
            map_piece = (map_piece[0], map_piece[1], map_piece[2])
            curr_map.append(map_piece)

    maps.append(curr_map) # append last map
    return maps

def find_locations(sources: List[int], maps: List[Tuple[int]]) -> List[int]:
    """
    Find all possible locations in Part 1, i.e., treating each seed in the
    input as an individual seed.

    Args:
        sources (List[int]): seeds
        maps (List[Tuple[int]]): transfer maps from level to level

    Returns:
        List[int]: destinations obtained after transfering from one level to the
        next
    """
    if not maps:
        return sources

    destinations = set()
    curr_map, *maps = maps
    added = False

    for source in sources:
        for map_piece in curr_map:
            if (source >= map_piece[SOURCE_START] and
                source < map_piece[SOURCE_START] + map_piece[RANGE]):
                destinations.add(map_piece[DEST_START] + (source - map_piece[SOURCE_START]))
                added = True

        if not added:
            destinations.add(source)

        added = False

    return find_locations(destinations, maps)

def find_interval_locs(sources: List[Tuple[int]], maps: List[Tuple[int]]) -> List[Tuple[int]]:
    """
    Find all possible locations in intervals.

    Args:
        sources (List[Tuple[int]]): seed intervals, i.e., [start, end)
        maps (List[Tuple[int]]): transfer maps

    Returns:
        List[Tuple[int]]: destination intervals
    """
    if not maps:
        return sources

    destinations = []
    curr_map, *maps = maps

    for map_piece in curr_map:
        dest_start, map_source_start, map_source_end = (map_piece[DEST_START],
        map_piece[SOURCE_START], map_piece[SOURCE_START] + map_piece[RANGE])
        not_applied = []
        while sources:
            source_start, source_end = sources.pop()
            # either entire range is not applied or a piece of it before map start
            lower_outlier = (source_start, min(source_end, map_source_start))
            middle = (max(source_start, map_source_start), min(map_source_end, source_end))
            # either entire range is not applied or a piece of it after map end
            upper_outlier = (max(map_source_end, source_start), source_end)
            if lower_outlier[1] > lower_outlier[0]: # map start has to be <= source end
                not_applied.append(lower_outlier)
            if middle[1] > middle[0]: # fitted range
                destinations.append((middle[0] - map_source_start + dest_start,
                                     middle[1] - map_source_start + dest_start))
            if upper_outlier[1] > upper_outlier[0]: # map end has to be >= source end
                not_applied.append(upper_outlier)

        sources = not_applied # try to apply these to other map pieces

    destinations += not_applied # whatever could not be applied

    return find_interval_locs(destinations, maps)

def process_input(lines: List[str]) -> Tuple[int]:
    """
    Generate maps and seed intervals for Part 2 and compute final answers.

    Args:
        lines (List[str]): input lines

    Returns:
        Tuple[int]: final answers for Part 1 and Part 2
    """
    seeds = [int(el) for el in lines[0].split(':')[1].split(' ') if el]
    seed_intervals = []
    for i in range(0, len(seeds) - 1, 2):
        # append [start of the range, end of the range)
        seed_intervals.append([seeds[i], seeds[i] + seeds[i+1]])
    maps = get_maps(lines)
    p1 = min(loc for loc in find_locations(seeds, maps))
    p2 = min(loc[0] for loc in find_interval_locs(seed_intervals, maps))

    return p1, p2

def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line != '\n']
    p1, p2 = process_input(lines)

    print(f"Location for part 1 is {p1}")
    print(f"Location for part 2 is {p2}")

if __name__ == "__main__":
    driver()
