"""
Day 7: https://adventofcode.com/2023/day/7

Both parts required to compute the final score of the Camel Cards game. The game
consists of hands, and each hands has 5 cards out of the list of 13 possible
cards. An example input line consists of the hand and its bid and looks like
this: '32T3K 765' (leftmost entry is hand, then bid).

Part 1: the final game score is defined as the sum of all bids multipled by the
rank of the hand, i.e, the weakest hand has rank of 1 and its contribution to
the sum would be bid * 1. If there is a tie, the rank of the hands is determined
by comparing the ranks of individual cards within the hand.

Part 2: rules of Part 1 still hold, but now 'J' card is treated as a wildcard,
i.e., it can become any card which would give the highest possible score to the
current hand. When dealing with a tie, 'J' now has the lowest score possible
amongst the other cards.
"""
from typing import List, Tuple, Dict, Union

HAND = 0
BID = 1

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# type aliases
hand = Tuple[Union[str, int]]

def check_type(hand_count: Dict[str, int]) -> int:
    """
    Returns a type of the hand.

    Args:
        hand_count (Dict[str, int]): a dictionary with cards as keys and the
        number each cards occurs in a hand as values

    Returns:
        int: type of the given hand
    """
    if 5 in hand_count.values():
        return FIVE_OF_A_KIND
    elif 4 in hand_count.values():
        return FOUR_OF_A_KIND
    elif (3 in hand_count.values() and 2 in hand_count.values() and
          len(hand_count.values()) == 2):
        return FULL_HOUSE
    elif (3 in hand_count.values() and 1 in hand_count.values() and
          len(hand_count.values()) == 3):
        return THREE_OF_A_KIND
    elif (2 in hand_count.values() and 1 in hand_count.values() and
          len(hand_count.values()) == 3):
        return TWO_PAIR
    elif (2 in hand_count.values() and 1 in hand_count.values() and
          len(hand_count.values()) == 4):
        return ONE_PAIR
    else:
        return HIGH_CARD

def get_hand_type(hand_count: Dict[str, int], p1: bool) -> int:
    """
    Get current hand type, handling both part 1 and part 2 rules (depending on
    the value of p1)

    Args:
        hand_count (Dict[str, int]): a dictionary with cards as keys and the
        number each cards occurs in a hand as values
        p1 (bool): True if the rules for part 1 are in play, False otherwise

    Returns:
        int: type of the given hand
    """
    if not p1 and 'J' in hand_count.keys():
        highest_val, j_count = HIGH_CARD, hand_count['J']
        for card in CARDS:
            hand_count_copy = hand_count.copy()
            del hand_count_copy['J']
            hand_count_copy[card] = hand_count_copy.get(card, 0) + j_count
            curr_val = check_type(hand_count_copy)
            highest_val = curr_val if curr_val > highest_val else highest_val
        return highest_val

    return check_type(hand_count)

def resolve_tie(hand1: hand, hand2: hand, p1: bool) -> hand:
    """
    Resolves tie between two hands of the same rank.

    Args:
        hand1 (hand): first hand
        hand2 (hand): second hand
        p1 (bool): True if the rules for part 1 are in play, False otherwise

    Returns:
        hand: hand which is ranked lower within the pair
    """
    card_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8,
              '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
    if not p1:
        card_order['J'] = 1

    for card1, card2 in zip(hand1[HAND], hand2[HAND]):
        if card_order[card1] > card_order[card2]:
            return hand2
        if card_order[card2] > card_order[card1]:
            return hand1

def compare(hand1: hand, hand2: hand, p1: bool) -> hand:
    """
    Compares two hands, supporting rules for both Part 1 and Part 2.

    Args:
        hand1 (hand): first hand
        hand2 (hand): second hand
        p1 (bool): True if the rules for part 1 are in play, False otherwise.

    Returns:
        hand: hand which is ranked lower within the pair
    """
    hand1_count, hand2_count = {}, {}
    for i in range(5):
        hand1_count[hand1[HAND][i]] = hand1_count.get(hand1[HAND][i], 0) + 1
        hand2_count[hand2[HAND][i]] = hand2_count.get(hand2[HAND][i], 0) + 1

    # determine the types of the hands
    hand1_type, hand2_type = get_hand_type(hand1_count, p1), get_hand_type(hand2_count, p1)
    if hand1_type > hand2_type:
        return hand2
    elif hand2_type > hand1_type:
        return hand1
    else:
        return resolve_tie(hand1, hand2, p1)

def sort(lines: List[str], p1=True) -> int:
    """
    Sorts all the hands according to Part 1 or Part 2 rules.

    Args:
        lines (List[str]): all lines from the input file
        p1 (bool, optional): True if the rules for part 1 are in play,
        False otherwise. Defaults to True.

    Returns:
        int: final score of current game
    """
    ans = 0
    hands = []
    for line in lines:
        line = line.strip()
        line = line.split(' ')
        curr_hand, bid = line[0], int(line[1])
        if not hands or compare((curr_hand, bid), hands[-1], p1) == hands[-1]:
            hands.append((curr_hand, bid))
        else:
            for idx, el in enumerate(hands):
                if compare((curr_hand, bid), el, p1) == (curr_hand, bid):
                    hands.insert(idx, (curr_hand, bid))
                    break

    for i in range(1, len(hands) + 1):
        ans += i * hands[i-1][BID]

    return ans

def driver():
    """
    Driver function to read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    p1, p2 = sort(lines, p1=True), sort(lines, p1=False)

    print(f"Sum for part 1 is {p1}")
    print(f"Sum for part 2 is {p2}")

if __name__ == "__main__":
    driver()
