with open("16/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def get_energized(start_pos, start_direction):
    energized = set()
    visited = set()

    def shoot_beam(pos, direction):
        while (
            pos[0] >= 0
            and pos[1] >= 0
            and pos[0] < len(puzzle_input)
            and pos[1] < len(puzzle_input[0])
        ):
            if (pos, direction) in visited:
                return

            energized.add(pos)
            visited.add((pos, direction))

            tile = puzzle_input[pos[0]][pos[1]]
            if tile == "/":
                direction = (-direction[1], -direction[0])
            if tile == "\\":
                direction = (direction[1], direction[0])
            if tile == "|":
                if direction[0] == 0:
                    shoot_beam((pos[0] - 1, pos[1]), (-1, 0))
                    shoot_beam((pos[0] + 1, pos[1]), (1, 0))
                    return
            if tile == "-":
                if direction[1] == 0:
                    shoot_beam((pos[0], pos[1] - 1), (0, -1))
                    shoot_beam((pos[0], pos[1] + 1), (0, 1))
                    return
            pos = (pos[0] + direction[0], pos[1] + direction[1])

    shoot_beam(start_pos, start_direction)
    return len(energized)


def part_1():
    return get_energized((0, 0), (0, 1))


def part_2():
    energized_values = []

    for i in range(len(puzzle_input)):
        energized_values.append(get_energized((0, i), (1, 0)))
        energized_values.append(get_energized((len(puzzle_input) - 1, i), (-1, 0)))
        energized_values.append(get_energized((i, 0), (0, 1)))
        energized_values.append(get_energized((i, len(puzzle_input[0]) - 1), (0, -1)))

    return max(energized_values)


print(part_1())

print(part_2())
