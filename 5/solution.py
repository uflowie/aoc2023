import regex as re
from itertools import batched

with open("5/input.txt", "r") as f:
    puzzle_input = f.read()

mapping_ranges = [
    [
        (source_start, source_start + range - 1, dest_start, dest_start + range - 1)
        for dest_start, source_start, range in batched(block, 3)
    ]
    for block in (
        [int(x) for x in re.findall(r"\d+", line)]
        for line in re.findall(
            r":\n((?:\d+ \d+ \d+\n*)+)", puzzle_input, re.MULTILINE | re.DOTALL
        )
    )
]

seeds = [int(x) for x in re.findall(r"(?<=:.*)\d+", puzzle_input)]


def map_range(range, mapping_ranges):
    sorted_mapping_ranges = sorted(mapping_ranges, key=lambda x: x[0])
    mapped_ranges = []
    range_start, range_end = range
    fully_consumed = False
    for source_start, source_end, dest_start, dest_end in sorted_mapping_ranges:
        if source_end < range_start:
            continue
        if range_end > source_end:
            mapped_ranges.append((dest_start + (range_start - source_start), dest_end))
            range_start = source_end + 1
        else:
            mapped_ranges.append(
                (
                    dest_start + (range_start - source_start),
                    dest_start + (range_end - source_start),
                )
            )
            fully_consumed = True
            break

    if not fully_consumed:
        mapped_ranges.append((range_start, range_end))

    return mapped_ranges


def solve(initial_ranges):
    min_locations = []

    for initial_range in initial_ranges:
        current_ranges = [initial_range]

        for layer_range in mapping_ranges:
            next_ranges = []
            for _range in current_ranges:
                next_ranges.extend(map_range(_range, layer_range))
            current_ranges = next_ranges

        min_locations.append(min(x[0] for x in current_ranges))

    return min(min_locations)


def part_1():
    return solve((seed, seed) for seed in seeds)


def part_2():
    return solve(
        (seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)
    )


print(part_1())

print(part_2())
