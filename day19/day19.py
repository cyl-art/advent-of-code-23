"""
Day 19: https://adventofcode.com/2023/day/19

Example input:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}

Part 1: run all parts thorugh the workflows and determine the sum of
ratings of all parts which are ultimately accepted.

Part 2: compute how many distinct combinations of ratings would be accepted by
workflows.
"""

from typing import Dict, List, Tuple

# type aliases
wflow = Dict[str, List[List[str]]]
p = Dict[str, int]

def parse_workflows(workflows: List[str]) -> List[wflow]:
    """
    Parse and format workflows block.

    Args:
        workflows (List[str]): workflows in input format

    Returns:
        List[p]: parsed workflows list
    """
    # {px: [[a<2006, qkq], [m>2090, A], [else, rfg]], ...} - workflow format
    res = {}
    for workflow in workflows:
        workflow = workflow[:-1].split('{')
        conditions = workflow[1].split(',')
        condition_list = []
        for condition in conditions[:-1]:
            condition_info = condition.split(':')
            condition_list.append([condition_info[0], condition_info[1]])
        condition_list.append(["else", conditions[-1]])
        res[workflow[0]] = condition_list

    return res

def parse_parts(parts: List[str]) -> List[p]:
    """
    Parse and format parts block.

    Args:
        parts (List[str]): parts in input format

    Returns:
        List[p]: parsed parts list
    """
    res = []
    for part in parts:
        part = part[1:-1].strip()
        part_dict = {}
        part_info = part.split(',')
        for piece in part_info:
            piece_info = piece.split('=')
            part_dict[piece_info[0]] = int(piece_info[1])
        res.append(part_dict)
    return res

def sort_parts_helper(workflows: List[wflow], curr_name: str, part: p, accepted: List[p]) -> None:
    """
    Record the parts which have been accepted.

    Args:
        workflows (List[wflow]): list of workflows
        curr_name (str): the name of current workflow
        part (p): current part
        accepted (List[p]): record of accepted parts
    """
    curr_workflow = workflows[curr_name]
    for instruction in curr_workflow:
        if instruction[0] == "else":
            if instruction[1] == 'A':
                accepted.append(part)
            elif instruction[1] != 'R':
                sort_parts_helper(workflows, instruction[1], part, accepted)
        elif '>' in instruction[0]:
            instruction_info = instruction[0].split('>')
            ind, num = instruction_info[0], int(instruction_info[1])
            if part[ind] > num:
                if instruction[1] == 'A':
                    accepted.append(part)
                elif instruction[1] != 'R':
                    sort_parts_helper(workflows, instruction[1], part, accepted)
                break
        elif '<' in instruction[0]:
            instruction_info = instruction[0].split('<')
            ind, num = instruction_info[0], int(instruction_info[1])
            if part[ind] < num:
                if instruction[1] == 'A':
                    accepted.append(part)
                elif instruction[1] != 'R':
                    sort_parts_helper(workflows, instruction[1], part, accepted)
                break

def count_accepted_ranges(workflows: List[wflow], ranges: Dict[str, Tuple[int]], curr_name="in") -> int:
    """
    Count the total number of unique combinations of ranges for the current
    parts whcih will be accepted starting from the current workflow.

    Args:
        workflows (List[wflow]): list of workflows
        ranges (Dict[str, Tuple[int]]): current ranges
        curr_name (str, optional): current workflow name. Defaults to "in".

    Returns:
        int: the total number of unique combinations of ranges for the current
        parts whcih will be accepted starting from the current workflow
    """
    if curr_name == 'R':
        return 0
    if curr_name == 'A':
        prod = 1
        for start, finish in ranges.values():
            prod *= (finish - start) + 1
        return prod

    total = 0
    conditions, last_cond = workflows[curr_name][:-1], workflows[curr_name][-1]
    for instruction in conditions:
        if '>' in instruction[0]:
            instruction_info = instruction[0].split('>')
            ind, num = instruction_info[0], int(instruction_info[1])
            lo, hi = ranges[ind]
            true = (max(num + 1, lo), hi)
            false = (lo, min(hi, num))
        elif '<' in instruction[0]:
            instruction_info = instruction[0].split('<')
            ind, num = instruction_info[0], int(instruction_info[1])
            lo, hi = ranges[ind]
            true = (lo, min(hi, num - 1))
            false = (max(num, lo), hi)

        if true[0] <= true[1]: # range contains values
            copy = dict(ranges)
            copy[ind] = true
            total += count_accepted_ranges(workflows, copy, instruction[1])
        if false[0] <= false[1]:
            ranges = dict(ranges)
            ranges[ind] = false
        else: # all ranges have been sent to process in the next workflow
            break

    else:
        total += count_accepted_ranges(workflows, ranges, last_cond[1])

    return total

def part1(workflows: List[wflow], parts: List[Dict[str, int]]) -> int:
    """
    Compute the answer to part 1.

    Args:
        workflows (List[wflow]): list of workflows
        parts (List[Dict[str, int]]): list of parts

    Returns:
        int: answer to part 1
    """
    accepted, res = [], 0
    for part in parts:
        sort_parts_helper(workflows, "in", part, accepted)

    for part in accepted:
        res += sum(part.values())
    return res

def part2(workflows: List[wflow]) -> int:
    """
    Compute the answer to part 2.

    Args:
        workflows (List[wflow]): list of workflows

    Returns:
        int: answer to part 2
    """
    # {x: (1, 4000), m: (1, 4000), a: (1, 4000), s: (1, 4000)} - range format
    return count_accepted_ranges(workflows, {key: (1, 4000) for key in ('x', 'm', 'a', 's')})

def driver():
    """
    A driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    workflows, parts = [], []
    workflows_part = True
    for line in lines:
        if line == '\n':
            workflows_part = False
        else:
            if workflows_part:
                workflows.append(line.strip())
            else:
                parts.append(line.strip())

    workflows = parse_workflows(workflows)
    parts = parse_parts(parts)

    p1, p2 = part1(workflows, parts), part2(workflows)

    print(f"Sum for Part 1 of all indices for accepted parts is {p1}")
    print(f"Sum for Part 2 of all indices for accepted parts is {p2}")

if __name__ == "__main__":
    driver()
