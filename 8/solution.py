import re
from itertools import cycle
from math import lcm

with open("8/input.txt", "r") as f:
    puzzle_input = f.readlines()


instructions = puzzle_input[0][:-1]

node_paths = {
    n.group(1): (p.group(1), p.group(2))
    for n, p in [
        (re.search(r"(.*) =", line), re.search(r"\((.*), (.*)\)", line))
        for line in puzzle_input[2:]
    ]
}


def solve(start, target_predicate):
    current = start
    steps = 0
    instruction_cycle = cycle(instructions)

    while not target_predicate(current):
        direction = next(instruction_cycle)
        left, right = node_paths[current]
        current = left if direction == "L" else right
        steps += 1

    return steps


def part_1():
    return solve("AAA", lambda x: x == "ZZZ")


def part_2():
    return lcm(
        *[solve(x, lambda x: x.endswith("Z")) for x in node_paths if x.endswith("A")]
    )


print(part_1())

print(part_2())
