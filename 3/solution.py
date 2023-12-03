import re

with open("3/input.txt", "r") as f:
    puzzle_input = f.readlines()


def is_adjacent(number_range, number_row, symbol_position):
    return (
        number_range[0] - 1 <= symbol_position[0] <= number_range[1]
        and number_row - 1 <= symbol_position[1] <= number_row + 1
    )


numbers = [
    (int(match.group(0)), match.span(), row)
    for row, line in enumerate(puzzle_input)
    for match in re.finditer(r"\d+", line)
]

symbols = [
    (match.group(0), match.span()[0], row)
    for row, line in enumerate(puzzle_input)
    for match in re.finditer(r"[^0-9\n.]", line)
]


def part_1():
    return sum(
        number[0]
        for number in numbers
        if any(is_adjacent(number[1], number[2], symbol[1:]) for symbol in symbols)
    )


def part_2():
    return sum(
        adjacent_numbers[0] * adjacent_numbers[1]
        for symbol in symbols
        if symbol[0] == "*"
        for adjacent_numbers in [
            [
                number[0]
                for number in numbers
                if is_adjacent(number[1], number[2], symbol[1:])
            ]
        ]
        if len(adjacent_numbers) == 2
    )


print(part_1())

print(part_2())
