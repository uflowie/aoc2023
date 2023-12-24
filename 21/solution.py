from heapq import heappush, heappop

with open("21/input.txt", "r") as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def get_reachable(puzzle_input, max_distance):
    half_len = len(puzzle_input) // 2
    start = (half_len, half_len)

    heap = [(0, start)]
    visited = set()
    distances = {}

    while heap:
        distance, (row, col) = heappop(heap)

        if ((row, col)) in visited:
            continue

        visited.add((row, col))
        distances[(row, col)] = distance

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < len(puzzle_input) and 0 <= new_col < len(puzzle_input[0]):
                symbol = puzzle_input[new_row][new_col]

                new_distance = distance + 1

                if symbol == "#" or new_distance > max_distance:
                    continue

                heappush(heap, (new_distance, (new_row, new_col)))
    return len(
        [
            position
            for position, distance in distances.items()
            if distance % 2 == max_distance % 2
        ]
    )


def expand(factor):
    factor = 3**factor
    new_puzzle_input = []
    for row in puzzle_input:
        new_puzzle_input.append(row * factor)
    new_puzzle_input = new_puzzle_input * factor
    return new_puzzle_input


def part_1():
    return get_reachable(puzzle_input, 64)


def part_2():
    distance = (26501365 - 65) // 131 - 1
    c0 = get_reachable(expand(3), 65)
    c1 = get_reachable(expand(3), 65 + 131)
    c2 = (get_reachable(expand(3), 65 + 131 * 2) - c1) - (c1 - c0)
    return distance * (c1 - c0) + ((distance**2 + distance) // 2) * c2 + c1


print(part_1())

print(part_2())
