with open("23/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


start = (1, 0)
end = (len(puzzle_input[0]) - 2, len(puzzle_input) - 1)


def get_neighbors(pos):
    x, y = pos
    return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]


def is_intersection(pos):
    return (
        len(
            [
                n
                for n in (
                    symbol_at((x, y))
                    for x, y in get_neighbors(pos)
                    if 0 <= x < len(puzzle_input[0]) and 0 <= y < len(puzzle_input)
                )
                if n in "<>^v"
            ]
        )
        >= 3
    )


slope_directions = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def in_bounds(pos):
    return 0 <= pos[0] < len(puzzle_input[0]) and 0 <= pos[1] < len(puzzle_input)


def symbol_at(pos):
    return puzzle_input[pos[1]][pos[0]]


def get_direction(pos1, pos2):
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])


def can_move_to_slope(pos, slope_pos):
    direction = get_direction(pos, slope_pos)
    sym = symbol_at(slope_pos)
    return sym != "#" and slope_directions[sym] == direction


def get_intersections():
    return [
        (j, i)
        for i in range(len(puzzle_input))
        for j in range(len(puzzle_input[i]))
        if is_intersection((j, i))
    ]


def find_next_intersection(start, direction, intersections):
    steps = 1
    next = (start[0] + direction[0], start[1] + direction[1])
    visited = set([start, next])
    while True:
        steps += 1
        next = [
            n
            for n in get_neighbors(next)
            if n not in visited and in_bounds(n) and symbol_at(n) != "#"
        ][0]
        if next in intersections or next == end or next == (1, 0):
            return next, steps
        visited.add(next)


def find_connected_intersections(
    intersection, neighbor_func, connections, intersections
):
    for nx, ny in neighbor_func(intersection):
        connections[intersection].append(
            find_next_intersection(
                intersection, get_direction(intersection, (nx, ny)), intersections
            )
        )


def slope_neighbors(pos):
    return [n for n in get_neighbors(pos) if can_move_to_slope(pos, n)]


def any_neighbors(pos):
    return [n for n in get_neighbors(pos) if symbol_at(n) != "#"]


def solve(neighbor_func):
    intersections = get_intersections()
    connections = {i: [] for i in intersections}

    for intersection in intersections:
        find_connected_intersections(
            intersection, neighbor_func, connections, intersections
        )

    connections[start] = [find_next_intersection(start, (0, 1), intersections)]
    return max(get_paths_lengths(start, set(), 0, connections))


def get_paths_lengths(start, visited, length, connections):
    visited.add(start)
    if start == end:
        return [length]
    paths = []
    for next, steps in connections[start]:
        if next not in visited:
            paths += get_paths_lengths(
                next, visited.copy(), length + steps, connections
            )
    return paths


def part_1():
    return solve(slope_neighbors)


def part_2():
    return solve(any_neighbors)


print(part_1())

print(part_2())
