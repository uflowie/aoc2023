import re
from collections import Counter

with open("7/input.txt", "r") as f:
    puzzle_input = f.readlines()

label_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def hand_type_part_1(hand):
    card_groups = sorted(Counter(hand).values())
    if card_groups == [5]:
        return 6
    if card_groups == [1, 4]:
        return 5
    if card_groups == [2, 3]:
        return 4
    if card_groups == [1, 1, 3]:
        return 3
    if card_groups == [1, 2, 2]:
        return 2
    if card_groups == [1, 1, 1, 2]:
        return 1
    return 0


def card_ordinal(hand):
    return sum(
        (len(hand) - i) ** len(label_order) * label_order.index(card)
        for i, card in enumerate(hand)
    )


def solve(type_func):
    return sum(
        (i + 1) * int(bid)
        for i, (_, _, bid, _) in enumerate(
            sorted(
                (
                    (type_func(hand), card_ordinal(hand), bid, hand)
                    for hand, bid in [
                        re.findall(r"[^\s]+", line) for line in puzzle_input
                    ]
                ),
                key=lambda x: (x[0], x[1]),
            )
        )
    )


def hand_type_part_2(hand):
    card_groups = Counter(hand)
    joker_count = card_groups["J"] if "J" in card_groups else 0
    card_groups = sorted(Counter(hand).values())
    if card_groups == [5]:
        return 6
    if card_groups == [1, 4]:
        return 6 if joker_count > 0 else 5
    if card_groups == [2, 3]:
        return 6 if joker_count > 0 else 4
    if card_groups == [1, 1, 3]:
        return 5 if joker_count > 0 else 3
    if card_groups == [1, 2, 2]:
        return 5 if joker_count == 2 else 4 if joker_count == 1 else 2
    if card_groups == [1, 1, 1, 2]:
        return 3 if joker_count > 0 else 1
    return 1 if joker_count > 0 else 0


def part_1():
    return solve(hand_type_part_1)


def part_2():
    label_order.remove("J")
    label_order.insert(0, "J")
    return solve(hand_type_part_2)


print(part_1())

print(part_2())
