import re
from collections import defaultdict


PATTERN = re.compile(r"(\w) ([\d]+) \(#([\d\w]+)\)")


with open("inputs/d18") as file:
    dig_plan = [re.match(PATTERN, line).groups() for line in file.read().splitlines()]

DIRECTIONS = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

fixed_dig_plan = [
    (DIRECTIONS[colour[-1]], int(colour[:-1], 16), colour) for _, __, colour in dig_plan
]


def determine_ranges(dig_plan):
    position = (0, 0)
    ranges = []
    for direction, num, _ in dig_plan:
        num = int(num)
        x = position[0] + (num if direction == "R" else -num if direction == "L" else 0)
        y = position[1] + (num if direction == "U" else -num if direction == "D" else 0)
        new_position = (x, y)
        ranges.append((position, new_position))
        position = new_position
    return ranges


def determine_starting_point(ranges):
    starting = [r for r in ranges if (0, 0) in r]
    x = starting[0][1][0]
    y = starting[1][0][1]
    return x // abs(x), y // abs(y)


def is_perimeter(ranges, point):
    for (x1, y1), (x2, y2) in ranges:
        if x1 == x2 == point[0] and min((y1, y2)) <= point[1] <= max((y1, y2)):
            return True
        elif y1 == y2 == point[1] and min((x1, x2)) <= point[0] <= max((x1, x2)):
            return True
    return False


def determine_next_points(point):
    return [
        (point[0] - 1, point[1]),
        (point[0] + 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1),
    ]


def determine_internal_volume(ranges):
    starting_point = determine_starting_point(ranges)
    stack = [starting_point]
    filled = {starting_point: None}
    while stack:
        point = stack.pop()
        n = determine_next_points(point)
        for _n in n:
            if _n in filled or is_perimeter(ranges, _n):
                continue
            filled[_n] = None
            stack.insert(0, _n)
    return len(filled)


def determine_lava_volume(dig_plan):
    ranges = determine_ranges(dig_plan)
    filled = determine_internal_volume(ranges)
    return filled + sum(abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in ranges)


p1 = determine_lava_volume(dig_plan)
print(p1)

# p2 = determine_lava_volume(fixed_dig_plan)
# print(p2)
