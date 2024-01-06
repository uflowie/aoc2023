from collections import Counter

with open("22/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def descend(brick):
    (x1, y1, z1), (x2, y2, z2) = brick
    return (x1, y1, z1 - 1), (x2, y2, z2 - 1)


def cubes(brick):
    (x1, y1, z1), (x2, y2, z2) = brick
    if y2 > y1:
        return [(x1, y, z1) for y in range(y1, y2 + 1)]
    if z2 > z1:
        return [(x1, y1, z) for z in range(z1, z2 + 1)]
    else:
        return [(x, y1, z1) for x in range(x1, x2 + 1)]


def coords(a):
    return tuple(int(x) for x in a.split(","))


def supporting_brick(cube, i, cubes_at_rest):
    x, y, z = cube
    if z != 1:
        cube = (x, y, z - 1)
        if cube in cubes_at_rest and cubes_at_rest[cube] != i:
            return cubes_at_rest[cube]
        return None
    return -1


def supporting_bricks(brick, i, cubes_at_rest):
    return {supporting_brick(cube, i, cubes_at_rest) for cube in cubes(brick)} - {None}


def get_bricks():
    return list(
        enumerate(
            sorted(
                [
                    (coords(left), coords(right))
                    for left, right in [line.split("~") for line in puzzle_input]
                ],
                key=lambda x: x[0][2],
            )
        )
    )


def drop_bricks():
    bricks = get_bricks()
    cubes_at_rest = {}
    bricks_at_rest = set()

    while bricks:
        i, brick = bricks.pop(0)
        if brick[0][2] == 1:
            bricks_at_rest.add((i, brick))
            cubes_at_rest.update({cube: i for cube in cubes(brick)})
        else:
            descended_cubes = cubes(descend(brick))
            if any(cube in cubes_at_rest for cube in descended_cubes):
                bricks_at_rest.add((i, brick))
                cubes_at_rest.update({cube: i for cube in cubes(brick)})
                continue
            bricks.insert(0, (i, descend(brick)))
    return bricks_at_rest, cubes_at_rest


def get_supports(bricks_at_rest, cubes_at_rest):
    supports = {}

    for i, brick in bricks_at_rest:
        supporting_cubes = supporting_bricks(brick, i, cubes_at_rest)
        for supporter in supporting_cubes:
            supports.setdefault(supporter, set()).add(i)
    return supports


def disintegrate(i, supports):
    support_counts = Counter([item for subset in supports.values() for item in subset])
    num_disintegrated = 0
    disintegrated = [i]
    while disintegrated:
        el = disintegrated.pop()
        if el not in supports:
            continue
        for s in supports[el]:
            support_counts[s] -= 1
            if support_counts[s] == 0:
                disintegrated.append(s)
                num_disintegrated += 1
    return num_disintegrated


bricks_at_rest, cubes_at_rest = drop_bricks()
supports = get_supports(bricks_at_rest, cubes_at_rest)


def part_1():
    disintegratable = 0
    support_counts = Counter([item for subset in supports.values() for item in subset])

    for i, _ in bricks_at_rest:
        if i not in supports:
            disintegratable += 1
            continue
        s = supports[i]
        if all(support_counts[supported] > 1 for supported in s):
            disintegratable += 1

    return disintegratable


def part_2():
    return sum(disintegrate(i, supports) for i in range(len(bricks_at_rest) - 1))


print(part_1())

print(part_2())
