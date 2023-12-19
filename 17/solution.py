from heapq import heappush, heappop

with open("17/input.txt", "r") as f:
    map_data = [[int(x) for x in line.strip()] for line in f.readlines()]


def can_move(straight_moves, direction, new_direction):
    if direction == new_direction and straight_moves >= 3:
        return False  # Can't move more than 3 blocks straight
    if direction != (0, 0) and direction == (-new_direction[0], -new_direction[1]):
        return False  # Can't move in opposite direction
    return True


def can_move2(straight_moves, direction, new_direction):
    if direction == new_direction and straight_moves >= 10:
        return False  # Can't move more than 10 blocks straight
    if direction != (0, 0) and direction == (-new_direction[0], -new_direction[1]):
        return False  # Can't move in opposite direction
    if direction != (0, 0) and direction != new_direction and straight_moves < 4:
        return False  # Can't change direction before 4 straight moves
    return True


def minimum_heat_loss(map_data, move_func):
    rows, cols = len(map_data), len(map_data[0])
    heap = [(0, 0, 0, (0, 0), 0)]
    visited = set()
    losses = []

    while heap:
        heat_loss, row, col, direction, straight_moves = heappop(heap)

        # If we reach the bottom-right corner, append loss to losses
        if row == rows - 1 and col == cols - 1:
            losses.append(heat_loss)
            continue

        if (row, col, direction, straight_moves) in visited:
            continue

        visited.add((row, col, direction, straight_moves))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_direction = (dr, dc)

            if not move_func(straight_moves, direction, new_direction):
                continue

            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                new_straight_moves = (
                    straight_moves + 1 if new_direction == direction else 1
                )
                new_heat_loss = heat_loss + map_data[new_row][new_col]
                heappush(
                    heap,
                    (
                        new_heat_loss,
                        new_row,
                        new_col,
                        new_direction,
                        new_straight_moves,
                    ),
                )

    return min(losses)


def part_1():
    return minimum_heat_loss(map_data, can_move)


def part_2():
    return minimum_heat_loss(map_data, can_move2)


print(part_1())

print(part_2())
