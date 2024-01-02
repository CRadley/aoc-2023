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


def determine_coordinates(dig_plan):
    x = 0
    y = 0
    coordinates = {(x, y)}
    for direction, num, _ in dig_plan:
        num = int(num)
        for _ in range(num):
            x += 1 if direction == "R" else -1 if direction == "L" else 0
            y += 1 if direction == "U" else -1 if direction == "D" else 0
            coordinates.add((x, y))
    return coordinates


def determine_internal_volume(coordinates):
    groups = defaultdict(set)
    for x, y in coordinates:
        groups[x].add(y)
    starting_group = next((g for g in groups.items() if len(g[1]) == 2), None)
    starting_point = sum(starting_group[1]) // 2
    stack = [(starting_group[0], starting_point)]

    filled = {}
    while stack:
        point = stack.pop()
        n = [
            (point[0] - 1, point[1]),
            (point[0] + 1, point[1]),
            (point[0], point[1] - 1),
            (point[0], point[1] + 1),
        ]
        for _n in n:
            if _n in filled or _n in coordinates:
                continue
            filled[_n] = None
            stack.insert(0, _n)
    return filled


def determine_lava_volume(dig_plan):
    coordinates = determine_coordinates(dig_plan)
    filled = determine_internal_volume(coordinates)
    return len(filled) + len(coordinates)


p1 = determine_lava_volume(dig_plan)
print(p1)
