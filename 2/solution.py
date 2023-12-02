import re
from functools import reduce
import operator

with open("2/input.txt", "r") as f:
    puzzle_input = f.readlines()

max_colors = {"red": 12, "green": 13, "blue": 14}


# find the highest number of cubes drawn in the given color
def min_required_cubes(line: str, color: str):
    return max(int(x) for x in re.findall(rf"(\d+) {color}", line))


# return the sum of all game ids (line numbers +1) where the highest number of cubes drawn in each color is less than or equal to the max number of cubes allowed for that color
def part_1():
    return sum(
        i + 1
        for i, line in enumerate(puzzle_input)
        if all(
            min_required_cubes(line, color) <= max_possible
            for color, max_possible in max_colors.items()
        )
    )


# return the sum of all powers of minimum required cubes for each color
def part_2():
    return sum(
        reduce(operator.mul, (min_required_cubes(line, color) for color in max_colors))
        for line in puzzle_input
    )


print(part_1())

print(part_2())
