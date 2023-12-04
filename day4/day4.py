"""
Day 4: https://adventofcode.com/2023/day/4

Part 1: given a list of cards, winning numbers (on the left of '|') and numbers
chosen (on the right of '|'), compute the total score gained. For the first
match, a card gets 1 point. Each subsequent match doubles the score. The formula
I came up with is score = 2 ^ (num_matches-1).

Example of a line: "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"

Part 2: deal with different scoring policy. For each match, you win a subsequent
copy of a scratchcard, e.g., if card 1 has one match, you will win one copy of
card 2. Total score equals the total number of cards possesed (both originals
and copies) at the end of the game. Apart from dealing with copies, you still
need to play original cards in the order of lines.
"""
from typing import List, Dict, Tuple

def process_line(line: str, lines: List[str], card_count: Dict[int:int],
                 p1=True) -> int | None:
    """
    Process each line and compute scratchcard scores for part 1 and 2. Uses
    recursion for part 2, potentially could be optimized by using cache.

    Args:
        line (str): card to compute score for
        lines (List[str]): all cards
        card_count (Dict[int:int]): counts of all cards so far
        p1 (bool, optional): True if Part 1, False otherwise. Defaults to True.

    Returns:
        int | None: score if computing Part 1 (writes to dictionary for part 2)
    """
    line = line.strip().split(':')
    num_comb = line[1]
    card_num = int(line[0].split(' ')[-1])
    nums = num_comb.split('|')

    # num = '' for digits due to extra space before, so it needs to be removed
    win_nums = {num for num in nums[0].strip().split(' ') if num}
    played_nums = [num for num in nums[1].strip().split(' ') if num]

    matches = 0
    for num in played_nums:
        if num in win_nums:
            matches += 1

    for i in range(matches):
        card_count[card_num+i+1] = card_count.get(card_num+i+1, 0) + 1
        process_line(lines[card_num+i], lines, card_count, p1=False)

    if p1:
        return int(2 ** (matches - 1))

def process_input(lines: List[str]) -> Tuple[int]:
    """
    Iterates over lines and computes scores for part 1 and part 2.

    Args:
        lines (List[str]): all cards

    Returns:
        Tuple[int]: answers for part 1 and part 2
    """
    p1, p2 = 0, 0
    card_count = {i: 1 for i in range(1, len(lines) + 1)}

    for line in lines:
        p1 += process_line(line, lines, card_count, p1=True)

    for count in card_count.values():
        p2 += count

    return p1, p2

def driver():
    """
    Driver function to open and read input file.
    """
    with open("test.txt" , "r", encoding="utf-8") as f:
        lines = f.readlines()

    p1, p2 = process_input(lines)

    print(f"Sum for Part 1 is {p1}")
    print(f"Sum for Part 2 is {p2}")

if __name__ == "__main__":
    driver()
