import numpy as np
from z3 import Ints, Solver, Int

with open("24/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def find_intersection(hailstone_1, hailstone_2):
    start1, d1 = hailstone_1
    start2, d2 = hailstone_2
    start1 = np.array(start1)
    d1 = np.array(d1)
    start2 = np.array(start2)
    d2 = np.array(d2)

    matrix = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
    vector = np.array([start2[0] - start1[0], start2[1] - start1[1]])

    try:
        t, s = np.linalg.solve(matrix, vector)

        if t < 0 or s < 0:
            return None

        intersection = start1 + t * d1
        return intersection
    except np.linalg.LinAlgError:
        return None


def to_hailstone(line):
    pos, dir = line.split(" @ ")
    pos = tuple(map(int, pos.split(",")))
    dir = tuple(map(int, dir.split(",")))
    return pos, dir


def disregard_z(hailstone):
    pos, dir = hailstone
    return (pos[0], pos[1]), (dir[0], dir[1])


def intersects_in_test_area(intersection):
    min = 200000000000000
    max = 400000000000000
    return min <= intersection[0] <= max and min <= intersection[1] <= max


hailstones = [to_hailstone(line) for line in puzzle_input]


def part_1():
    intersections = [
        intersection
        for intersection in [
            find_intersection(disregard_z(hailstones[i]), disregard_z(hailstones[j]))
            for i in range(len(hailstones))
            for j in range(i + 1, len(hailstones))
        ]
        if intersection is not None and intersects_in_test_area(intersection)
    ]

    return len(intersections)


def part_2():
    x, y, z, dx, dy, dz = Ints("x y z dx dy dz")

    solver = Solver()

    for i, hailstone in enumerate(hailstones):
        (hx, hy, hz), (hdx, hdy, hdz) = hailstone
        t = Int(f"t{i}")
        solver.add(x + t * dx == hx + t * hdx)
        solver.add(y + t * dy == hy + t * hdy)
        solver.add(z + t * dz == hz + t * hdz)
        solver.add(t >= 0)

    solver.check()
    model = solver.model()
    return model[x].as_long() + model[y].as_long() + model[z].as_long()


print(part_1())

print(part_2())
