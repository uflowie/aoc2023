import networkx as nx
from functools import reduce

with open('25/input.txt', 'r') as f:
    puzzle_input = [line.strip() for line in f.readlines()]

def part_1():
    G = nx.Graph()

    for line in puzzle_input:
        source, targets = line.split(': ')
        targets = targets.split(' ')
        for target in targets:
            G.add_edge(source, target)

    min_cut = nx.minimum_edge_cut(G)
    G.remove_edges_from(min_cut)
    left, right = nx.connected_components(G)
    return len(left) * len(right)

print(part_1())
