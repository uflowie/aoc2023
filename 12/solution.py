import re
from functools import cache

with open("12/input.txt", "r") as f:
    puzzle_input = f.readlines()


records_groups = [
    (re.findall(r"[^\s]*", line)[0], [int(x) for x in re.findall(r"\d+", line)])
    for line in puzzle_input
]


@cache
def variations(record, group, record_index, target_group_index, curr_group_length):
    if target_group_index == len(group):
        # we have completed all target groups, if there are damaged wells left, this is not a valid record
        return 1 if "#" not in record[record_index:] else 0

    target_group_length = group[target_group_index]

    if record_index == len(record):
        # we have reached the end of the record, but not all groups have been completed, this is not a valid record
        return (
            1
            if curr_group_length == target_group_length
            and target_group_index == len(group) - 1
            else 0
        )

    if curr_group_length > target_group_length:
        # we have exceeded the length of the current group, this is not a valid record
        return 0

    symbol = record[record_index]

    if symbol == ".":
        if curr_group_length == target_group_length:
            # we have reached the end of the current group, move on to the next group
            return variations(
                record, group, record_index + 1, target_group_index + 1, 0
            )
        if curr_group_length == 0:
            # we are not in a group, move on to the next symbol
            return variations(record, group, record_index + 1, target_group_index, 0)
        # group terminated early, this is not a valid record
        return 0

    if symbol == "#":
        return variations(
            record, group, record_index + 1, target_group_index, curr_group_length + 1
        )

    if symbol == "?":
        num_variations = 0

        # treat as damaged
        num_variations += variations(
            record, group, record_index + 1, target_group_index, curr_group_length + 1
        )

        # treat as operational
        if curr_group_length == target_group_length:
            num_variations += variations(
                record, group, record_index + 1, target_group_index + 1, 0
            )
        if curr_group_length == 0:
            num_variations += variations(
                record, group, record_index + 1, target_group_index, 0
            )
        return num_variations


def part_1():
    return sum(
        variations(record, tuple(group), 0, 0, 0) for record, group in records_groups
    )


def part_2():
    return sum(
        variations("?".join([record] * 5), tuple(group * 5), 0, 0, 0)
        for record, group in records_groups
    )


print(part_1())

print(part_2())
