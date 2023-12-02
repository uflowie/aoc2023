import re

with open("1/input.txt", "r") as f:
    puzzle_input = f.readlines()


digit_words = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def calibration_value_sum(digit_finder):
    return sum(
        int(digits[0] + digits[-1])
        for digits in [digit_finder(line) for line in puzzle_input]
    )


def part_1():
    return calibration_value_sum(lambda line: re.findall(r"\d", line))


def part_2():
    return calibration_value_sum(
        lambda line: [
            digit if digit.isdigit() else digit_words[digit]
            for digit in re.findall(
                r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line
            )
        ]
    )


print(part_1())

print(part_2())
