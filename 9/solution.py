import re

with open("9/input.txt", "r") as f:
    puzzle_input = f.readlines()


def subsequence(sequence):
    return [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]


def next_value(sequence, index, sign):
    stack = [sequence]
    while not all(x == 0 for x in stack[-1]):
        stack.append(subsequence(stack[-1]))

    next_val = 0
    while len(stack) != 0:
        next_seq = stack.pop()
        next_val = next_seq[index] + next_val * sign

    return next_val


sequences = [[int(x) for x in re.findall(r"-*\d+", line)] for line in puzzle_input]


def part_1():
    return sum(next_value(sequence, -1, 1) for sequence in sequences)


def part_2():
    return sum(next_value(sequence, 0, -1) for sequence in sequences)


print(part_1())

print(part_2())
