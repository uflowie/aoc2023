with open("10/input.txt", "r") as f:
    puzzle_input = f.readlines()

start = next(
    (
        (i, j)
        for i, row in enumerate(puzzle_input)
        for j, cell in enumerate(row)
        if cell == "S"
    ),
    None,
)


START_DIRECTION = (0, 1)


def move(tile, direction):
    return (tile[0] + direction[0], tile[1] + direction[1])


def get_tile(pos):
    return puzzle_input[pos[0]][pos[1]]


def get_direction(tile, cur_direction):
    if tile == "|" or tile == "-":
        return cur_direction
    if tile == "L" or tile == "7":
        return (cur_direction[1], cur_direction[0])
    if tile == "J" or tile == "F":
        return (-cur_direction[1], -cur_direction[0])


loop_tiles = [start]
cur_direction = (0, 1)
cur_pos = move(start, START_DIRECTION)
moves = 1

while cur_pos != start:
    loop_tiles.append(cur_pos)
    cur_direction = get_direction(get_tile(cur_pos), cur_direction)
    cur_pos = move(cur_pos, cur_direction)
    moves += 1


def part_1():
    return moves // 2


sides = set(
    tuple(sorted([loop_tiles[i - 1], loop_tiles[i % len(loop_tiles)]]))
    for i in range(len(loop_tiles))
    if loop_tiles[i - 1][0] != loop_tiles[i % len(loop_tiles)][0]
)


def get_intersections(row, col):
    intersections = 0
    for start, end in [x for x in sides if x[0][1] > col]:
        if start[0] <= row < end[0]:
            intersections += 1
    return intersections


enclosed_tiles = 0

loop_tiles = set(loop_tiles)

for i in range(len(puzzle_input)):
    for j in range(len(puzzle_input[0])):
        if (i, j) not in loop_tiles and get_intersections(i, j) % 2 == 1:
            enclosed_tiles += 1


def part_2():
    return enclosed_tiles


print(part_1())

print(part_2())
