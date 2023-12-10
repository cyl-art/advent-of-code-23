"""
Day 6: https://adventofcode.com/2023/day/6

Input file describes allowed time and record distance for races:

Time:      7  15   30
Distance:  9  40  200

Holding a charge button for 1 ms gives a boat speed of 1 mm/ms.

Part 1: compute the product of button hold times which allow to beat the record.

Part 2: treat time and distance entries as single numbers, 71530 and 940200.
Compute the total amount of button hold times which allow to beat the distance
record.
"""
import math

def get_num_of_wins(time: int, record: int) -> int:
    """
    Find the number of winning button hold times for the current time and record.
    Use quadratic formula to compute min and max values of the winning range
    and find its length.

    Args:
        time (int): total time allowed for the race
        record (int): record distance

    Returns:
        int: number of winning button hold times
    """

    # quadratic equation of the form hold_time * (time - hold_time) = record + 1
    # min value needs to be ceiled (e.g., 5.3 has to be 6) and max value has to
    # be floored (7.8 needs to be 7) to stay in the appropriate range
    min_time = math.ceil((time - math.sqrt(time**2 - 4 * (record + 1))) / 2)
    max_time = math.floor((time + math.sqrt(time**2 - 4 * (record + 1))) / 2)
    return max_time - min_time + 1

def process_input(lines: int, part: int) -> int:
    """
    Parse input lines differently depending on the part being solved and compute
    final result.

    Args:
        lines (int): input lines to parse
        part (int): 1 or 2

    Returns:
        int: final answer for given part
    """
    if part == 1:
        time, record = lines[0].split(':')[1], lines[1].split(':')[1]
        time, record = ([int(el) for el in time.strip().split(' ') if el],
        [int(el) for el in record.strip().split(' ') if el])
        info = dict(zip(time, record))
        ans = 1
        for time, dist in info.items():
            ans *= get_num_of_wins(time, dist)
        return ans
    else:
        time, record = (lines[0].split(':')[1].replace(' ', ''),
                        lines[1].split(':')[1].replace(' ', ''))
        time, record = int(time), int(record)
        return get_num_of_wins(time, record)

def driver():
    """
    Driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    p1, p2 = process_input(lines, 1), process_input(lines, 2)
    print(f"Answer for Part 1 is {p1}")
    print(f"Answer for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
