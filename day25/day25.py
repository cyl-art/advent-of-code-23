"""
Day 25: https://adventofcode.com/2023/day/25

Using the given graph, find three adges cutting which would divide a graph into
two components. Compute the product of number of nodes in these components.
"""

from typing import List
import networkx as nx

def part1(graph: nx.Graph) -> int:
    """
    Use networkx module to compute the answer to Part 1.

    Args:
        graph (nx.Graph): graph

    Returns:
        int: product of number of nodes of two graph components
    """
    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    comp1, comp2 = nx.connected_components(graph)
    return len(comp1) * len(comp2)

def parse_input(lines: List[str]) -> nx.Graph:
    """
    Parse the input file and construct a bidirectional graph.

    Args:
        lines (List[str]): input file

    Returns:
        nx.Graph: resultant graph
    """
    graph = nx.Graph()
    for line in lines:
        left, right = line.split(':')
        for node in right.strip().split():
            graph.add_edge(left, node)
            graph.add_edge(node, left)

    return graph

def driver():
    """
    Driver function to open and read an input file.
    """
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    graph = parse_input(lines)
    p1 = part1(graph)

    print(f"Answer for Part 1 is {p1}")

if __name__ == "__main__":
    driver()
