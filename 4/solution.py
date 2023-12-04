import regex as re

with open("4/input.txt", "r") as f:
    puzzle_input = f.readlines()

common_numbers = [
    len(set(winning) & set(ours))
    for line in puzzle_input
    for winning, ours in (
        (
            re.findall(r"(?<=:.*)(\d\d*)(?=.*\|)", line), # between : and |
            re.findall(r"(?<=\|\s.*)(\d\d*)", line), # after |
        ),
    )
]


def part_1():
    return sum(0 if common == 0 else 2 ** (common - 1) for common in common_numbers)


def part_2():
    common_numcards = [[common, 1] for common in common_numbers]
    for i, (common, numcards) in enumerate(common_numcards):
        for j in range(common):
            for _ in range(numcards):
                common_numcards[i + j + 1][1] += 1
    return sum(numcards for _, numcards in common_numcards)


print(part_1())

print(part_2())