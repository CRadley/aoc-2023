import re, math


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


def determine_shape(dig_plan):
    position = (0, 0)
    edges = []
    corners = []
    for direction, num, _ in dig_plan:
        num = int(num)
        x = position[0] + (num if direction == "R" else -num if direction == "L" else 0)
        y = position[1] + (num if direction == "U" else -num if direction == "D" else 0)
        new_position = (x, y)
        edges.append((position, new_position))
        position = new_position
        corners.append(new_position)
    return edges, corners


def calculate_area(corners):
    a = 0
    for i, (x, y) in enumerate(corners):
        if i == len(corners) - 1:
            _x = corners[0][0]
            _y = corners[0][1]
        else:
            _x = corners[i + 1][0]
            _y = corners[i + 1][1]
        a += (x * _y) - (y * _x)
    return abs(a) // 2


def calculate_perimeter(edges):
    return sum(abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in edges)


def calculate_internal_points(corners, perimeter):
    a = calculate_area(corners)
    enclosed_points = math.ceil(a + 1 - perimeter / 2)
    return enclosed_points


def determine_lava_volume(dig_plan):
    edges, corners = determine_shape(dig_plan)
    perimeter = calculate_perimeter(edges)
    internal_points = calculate_internal_points(corners, perimeter)
    return internal_points + perimeter


p1 = determine_lava_volume(dig_plan)
print(p1)

p2 = determine_lava_volume(fixed_dig_plan)
print(p2)
