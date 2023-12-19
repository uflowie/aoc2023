from shapely.geometry import Polygon
import re

with open("18/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]

dir_map = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

instructions = [
    (dir_map[direction], int(distance), color)
    for direction, distance, color in [line.split() for line in puzzle_input]
]


def solve(instructions):
    vertices = [(0, 0)]
    circumference = 0

    for direction, distance, _ in instructions:
        last_vertex = vertices[-1]
        vertices.append(
            (
                last_vertex[0] + direction[0] * distance,
                last_vertex[1] + direction[1] * distance,
            )
        )
        circumference += distance

    vertices.pop()

    poly = Polygon(vertices)
    return int(poly.area) + circumference / 2 + 1


def hex_to_distance(hex):
    return int(re.sub(r"[()#]", "", hex[0 : len(hex) - 2]), 16)


def hex_to_direction(hex):
    last_digit = int(hex[-2])
    if last_digit == 0:
        return (0, 1)
    elif last_digit == 1:
        return (1, 0)
    elif last_digit == 2:
        return (0, -1)
    elif last_digit == 3:
        return (-1, 0)


def part_1():
    return solve(instructions)


def part_2():
    return solve(
        (hex_to_direction(color), hex_to_distance(color), _)
        for _, _, color in instructions
    )


print(part_1())

print(part_2())
