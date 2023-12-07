import re
from functools import reduce
from operator import mul

with open("6/input.txt", "r") as f:
    puzzle_input = f.readlines()


times, records = [[int(x) for x in re.findall("\d+", line)] for line in puzzle_input]


def solve(times, records):
    return reduce(
        mul,
        (
            len([x for x in [i * (time - i) for i in range(time)] if x > record])
            for time, record in zip(times, records)
        ),
        1,
    )


def part_1():
    return solve(times, records)


def part_2():
    return solve(*[[int("".join(str(y) for y in x))] for x in [times, records]])


print(part_1())

print(part_2())
