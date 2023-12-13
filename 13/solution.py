import Levenshtein

with open("13/input.txt", "r") as f:
    puzzle_input = f.read()


def rotate(pattern):
    return [list(col) for col in zip(*pattern)]


def score(pattern, target_diff):
    for i in range(1, len(pattern)):
        half_len = min(i, len(pattern) - i)
        top = pattern[i - half_len : i]
        bottom = pattern[i : i + half_len]
        if Levenshtein.distance(str(top), str(list(reversed(bottom)))) == target_diff:
            return i
    return 0


def solve(target_diff):
    return sum(
        score(rotate(pattern), target_diff) + 100 * score(pattern, target_diff)
        for pattern in [x.split("\n") for x in puzzle_input.split("\n\n")]
    )


def part_1():
    return solve(0)


def part_2():
    return solve(1)


print(part_1())

print(part_2())
