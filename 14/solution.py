from collections import Counter

with open("14/input.txt", "r") as f:
    puzzle_input = [list(line.strip()) for line in f.readlines()]


def move(rock_x, rock_y, direction_x, direction_y):
    new_pos = (rock_x + direction_x, rock_y + direction_y)
    if (
        new_pos[0] < 0
        or new_pos[0] >= len(puzzle_input[0])
        or new_pos[1] < 0
        or new_pos[1] >= len(puzzle_input)
    ):
        return

    new_pos_symbol = puzzle_input[new_pos[1]][new_pos[0]]

    if new_pos_symbol in "#O":
        return

    puzzle_input[rock_y][rock_x] = "."
    puzzle_input[new_pos[1]][new_pos[0]] = "O"

    move(new_pos[0], new_pos[1], direction_x, direction_y)


def weight():
    return sum(
        (len(puzzle_input) - i) * Counter(line)["O"]
        for i, line in enumerate(puzzle_input)
    )


def tilt(direction):
    rocks = [
        (x, y)
        for y, line in enumerate(puzzle_input)
        for x, char in enumerate(line)
        if char == "O"
    ]

    x, y = direction
    if x == 1:
        rocks = sorted(rocks, key=lambda rock: rock[0], reverse=True)
    elif x == -1:
        rocks = sorted(rocks, key=lambda rock: rock[0])
    elif y == 1:
        rocks = sorted(rocks, key=lambda rock: rock[1], reverse=True)
    elif y == -1:
        rocks = sorted(rocks, key=lambda rock: rock[1])

    for rock in rocks:
        move(rock[0], rock[1], x, y)


def cycle():
    tilt((0, -1))
    tilt((-1, 0))
    tilt((0, 1))
    tilt((1, 0))


def part_1():
    tilt((0, -1))
    return weight()


def part_2():
    seen = {str(puzzle_input): 0}
    i = 0

    while i < 1000000000:
        cycle()
        i += 1

        if str(puzzle_input) in seen:
            cycle_len = i - seen[str(puzzle_input)]
            i += cycle_len * ((1000000000 - i) // cycle_len)
        seen[str(puzzle_input)] = i

    return weight()


print(part_1())

print(part_2())
