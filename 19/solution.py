import re
from functools import reduce
from operator import mul

with open("19/input.txt", "r") as f:
    puzzle_input = f.read().strip()

workflows, items = puzzle_input.split("\n\n")

workflows = workflows.split("\n")
items = items.split("\n")

items = [[int(x) for x in re.findall(r"\d+", item)] for item in items]


def make_workflow(workflow: str):
    name = re.search(r"(.*)\{", workflow).group(1)
    rules = re.search(r"\{(.*)\}", workflow).group(1).split(",")

    return name, rules


workflows = {
    name: rules for name, rules in [make_workflow(workflow) for workflow in workflows]
}


category_indices = {"x": 0, "m": 1, "a": 2, "s": 3}

accepted_ranges = []


def get_overlap(range_1, range_2):
    min_1, max_1 = range_1
    min_2, max_2 = range_2

    if max_1 < min_2 or max_2 < min_1:
        return 0, 0

    return max(min_1, min_2), min(max_1, max_2)


def find_accepted_ranges(rules, curr_range):
    for rule in rules:
        if rule == "R":
            return
        if rule == "A":
            accepted_ranges.append(curr_range)
            return
        if ":" not in rule:
            find_accepted_ranges(workflows[rule], curr_range)
            return

        pred, target = rule.split(":")

        category, value = re.split(r"<|>", pred)

        value = int(value)
        index = category_indices[category]

        if "<" in pred:
            left = curr_range.copy()
            left[index] = get_overlap(left[index], (1, value))
            right = curr_range.copy()
            right[index] = get_overlap(right[index], (value, 4001))
            find_accepted_ranges([target], left)
            curr_range = right
        elif ">" in pred:
            left = curr_range.copy()
            left[index] = get_overlap(left[index], (1, value + 1))
            right = curr_range.copy()
            right[index] = get_overlap(right[index], (value + 1, 4001))
            find_accepted_ranges([target], right)
            curr_range = left


find_accepted_ranges(workflows["in"], [(1, 4001), (1, 4001), (1, 4001), (1, 4001)])


def part_1():
    return sum(
        sum(item)
        for item in items
        for range in accepted_ranges
        if all(min_ <= value <= max_ for (min_, max_), value in zip(range, item))
    )


def part_2():
    return sum(reduce(mul, (a[1] - a[0] for a in range)) for range in accepted_ranges)


print(part_1())

print(part_2())
