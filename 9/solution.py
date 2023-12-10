import re

with open("9/input.txt", "r") as f:
    puzzle_input = f.readlines()


def next_val(sequence):
    return (
        0
        if len(sequence) == 0
        else sequence[-1]
        + next_val([sequence[i] - sequence[i - 1] for i in range(1, len(sequence))])
    )


sequences = [[int(x) for x in re.findall(r"-*\d+", line)] for line in puzzle_input]


def part_1():
    return sum(map(next_val, sequences))


def part_2():
    return sum(map(next_val, map(lambda x: list(reversed(x)), sequences)))


print(part_1())

print(part_2())
