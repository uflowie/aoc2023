from functools import reduce

with open("15/input.txt", "r") as f:
    puzzle_input = f.read().strip().split(",")


def hash(str):
    return reduce(lambda acc, char: ((acc + ord(char)) * 17) % 256, str, 0)


boxes = {i: [] for i in range(256)}


def box(label):
    return boxes[hash(label)]


def label_index(label):
    labels = [label for label, _ in box(label)]
    if label in labels:
        return labels.index(label)
    return -1


def add_lense(label, focal_length):
    if label_index(label) != -1:
        box(label)[label_index(label)][1] = focal_length
    else:
        box(label).append([label, focal_length])


def remove_lense(label):
    if label_index(label) != -1:
        box(label).pop(label_index(label))


def process_step(step):
    if "=" in step:
        label, focal_length = step.split("=")
        add_lense(label, int(focal_length))
    else:
        remove_lense(step.replace("-", ""))


def focusing_power():
    return sum(
        (i + 1) * (j + 1) * lens[1]
        for i, box in boxes.items()
        for j, lens in enumerate(box)
    )


def part_1():
    return sum(hash(line) for line in puzzle_input)


def part_2():
    for step in puzzle_input:
        process_step(step)
    return focusing_power()


print(part_1())

print(part_2())
