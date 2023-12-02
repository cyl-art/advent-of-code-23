"""
Day 1: https://adventofcode.com/2023/day/1

The first part required finding first and last digits in the string and
combining them into a number. The second part extended to identifying
digits spelled as words. This approach looks only for the first and
last digits.
"""

def process_line(line: str) -> int:
    """
    Given a string, extract the digits from it and find the calibration
    value, which is a two-digit number composed of the first and last digit

    Args:
        line (str): string to process

    Returns:
        int: calibration value
    """
    res = 0
    start, end  = 0, len(line) - 1
    check_start, check_end = True, True
    first_digit, last_digit = 0, 0
    while (end >= 0):
        if line[start].isdigit() and check_start:
            first_digit = int(line[start])
            check_start = False
        if line[end].isdigit() and check_end:
            last_digit = int(line[end])
            check_end = False
        if not check_start and not check_end:
            break

        start += 1
        end -= 1

    res = first_digit * 10 + last_digit
    return res

def process_line2(line: str) -> int:
    """
    Same task as in the process_line(), but also is able to process digits
    spelled as words, e.g., "one".

    Args:
        line (str): string to process

    Returns:
        int: calibration value
    """
    possible_digits = {"one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    first_digit, last_digit = 0, 0
    check_start, check_end = True, True
    start = 0
    end = len(line)-1
    curr_digit_start = ""
    curr_digit_end = ""
    while (end >= 0):
        if line[start].isdigit() and check_start:
            first_digit = int(line[start])
            check_start = False
        elif line[start].isalpha() and check_start:
            curr_digit_start += line[start]
            for digit_name, digit in possible_digits.items():
                if digit_name in curr_digit_start:
                    first_digit = int(digit)
                    check_start = False
                    break
        if line[end].isdigit() and check_end:
            last_digit = int(line[end])
            check_end = False
        elif line[end].isalpha() and check_end:
            curr_digit_end += line[end]
            for digit_name, digit in possible_digits.items():
                if digit_name in curr_digit_end[::-1]:
                    last_digit = int(possible_digits[digit_name])
                    check_end = False
                    break
        if not check_start and not check_end:
            break

        start += 1
        end -= 1

    res = first_digit * 10 + last_digit
    return res

def driver():
    """
    Main driver function to open the file and get the final sum. Use
    test_short.txt for a shorter version of input.
    """
    res1, res2 = 0, 0
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        res1 += process_line(line)
        res2 += process_line2(line)

    print(f"Sum for Part 1 is: {res1}, sum for Part 2 is: {res2}")

if __name__ == "__main__":
    driver()
