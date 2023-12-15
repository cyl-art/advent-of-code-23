"""
Day 15: https://adventofcode.com/2023/day/15

The input file contains a single line with strings separated by commas:

rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7

Part 1: calculate the sum of hash values of these strings according
to the HASH (Holiday ASCII String Helper) algorithm.

Part 2: calculate the sum of focusing power of the lenses in boxes.
A lens needs to be added to a box if '=' was present in the string and deleted
if '-' was present. Box number is calculated by hashing the lens label.
"""

from typing import List, Tuple, Union

def hashing(string: str) -> int:
    """
    Compute hash value of the string according to the HASH
    algorithm.

    Args:
        string (str): string to hash

    Returns:
        int: hash value of the string
    """
    res = 0
    for ch in string:
        res += ord(ch)
        res *= 17
        res %= 256
    return res

def find_el(lenses: List[Tuple[str]], given_lens: str) -> Tuple[Union[bool, int]]:
    """
    Check if a given lens is in the box and return its index if found.

    Args:
        lenses (List[Tuple[str]]): lenses in the box
        given_lens (str): lens to look for

    Returns:
        Tuple[Union[bool, int]]: return True and lens index if found, False and
        -1 as index otherwise
    """
    if lenses:
        for idx, lens in enumerate(lenses):
            if lens[0] == given_lens:
                return True, idx

    return False, -1

def focusing_power(box_num: int, lenses: List[Tuple[str]]) -> int:
    """
    Calculate the focusing power of the lenses in the current box.

    Args:
        box_num (int): the number of the box
        lenses (List[Tuple[str]]): lenses in this box

    Returns:
        int: resultant focusing power
    """
    res = 0
    for idx, lens in enumerate(lenses):
        res += (1 + box_num) * (idx+1) * int(lens[1]) # focal length
    return res

def part1(line: str) -> int:
    """
    Calculate answer for Part 1 - the sum of hash values of all strings from the
    line.

    Args:
        line (str): line with strings

    Returns:
        int: sum of hash values of strings
    """
    strings = line.split(',')
    res = 0
    for string in strings:
        res += hashing(string)
    return res

def part2(line: str) -> int:
    """
    Calculate the answer for Part 2 - the sum of focusing powers of lenses
    in all boxes.

    Args:
        line (str): line with strings

    Returns:
        int: the sum of focusing powers of lenses in all boxes
    """
    strings = line.split(',')
    boxes = {}
    # boxes[box_num] = [(lens_name, focal_len)]
    for string in strings:
        if '-' in string:
            lens = string[:-1]
            box_num = hashing(lens)
            is_in_box, idx = find_el(boxes.get(box_num, None), lens)
            if boxes.get(box_num, None) and is_in_box:
                boxes[box_num].pop(idx)
        elif '=' in string:
            lens, focal_len = string.split('=')
            box_num = hashing(lens)
            lens_in, lens_idx = find_el(boxes.get(box_num, None), lens)
            # lens already in the box, replace it
            if boxes.get(box_num, None) and lens_in:
                lens_label = boxes[box_num][lens_idx][0]
                boxes[box_num][lens_idx] = (lens_label, focal_len)
            # add the lens to the box
            else:
                boxes[box_num] =  boxes.get(box_num, []) + [(lens, focal_len)]

    # calculate final focusing power
    res = 0
    for box_num, lenses in boxes.items():
        res += focusing_power(box_num, lenses)

    return res


def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        line = f.readlines()[0] # input contains only one line

    line = line.strip()
    p1, p2 = part1(line), part2(line)
    print(f"Sum for Part 1 is {p1}")
    print(f"Sum for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
