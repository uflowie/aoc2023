with open("11/input.txt", "r") as f:
    puzzle_input = f.readlines()


y_stretches = [
    i
    for i, row in enumerate(puzzle_input)
    if all(cell == "." or cell == "\n" for cell in row)
]

x_stretches = [
    i for i in range(len(puzzle_input[0])) if all(row[i] == "." for row in puzzle_input)
]

galaxies = [
    (i, j)
    for i, row in enumerate(puzzle_input)
    for j, cell in enumerate(row)
    if cell == "#"
]


def stretch(start, end, stretches):
    start, end = min(start, end), max(start, end)
    return len([i for i in stretches if start <= i <= end])


def distance(a, b, factor):
    return (
        abs(a[0] - b[0])
        + abs(a[1] - b[1])
        + stretch(a[0], b[0], y_stretches) * factor
        + stretch(a[1], b[1], x_stretches) * factor
    )


def solve(factor):
    return sum(
        distance(galaxies[i], galaxies[j], factor)
        for i in range(len(galaxies))
        for j in range(i + 1, len(galaxies))
    )


def part_1():
    return solve(1)


def part_2():
    return solve(999999)


print(part_1())

print(part_2())
