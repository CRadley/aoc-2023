from typing import List
from collections import defaultdict

with open("inputs/d21") as file:
    lines = file.read().splitlines()
    resolution = len(lines[0])
    garden = [c for line in lines for c in line]

starting_point = garden.index("S")


def determine_steps(garden, position, resolution):
    next_steps = []
    if position - resolution >= 0:
        next_steps.append(position - resolution)
    if (position + 1) % resolution:
        next_steps.append(position + 1)
    if position + resolution < len(garden) - 1:
        next_steps.append(position + resolution)
    if (position - 1) % resolution != resolution - 1:
        next_steps.append(position - 1)
    x = []
    for n in next_steps:
        if garden[n] != "#":
            x.append(n)
    return x


def determine_reachable_points(
    garden: List[int],
    starting_point: int,
    resolution: int,
    steps,
) -> int:
    queue = [starting_point]
    visited = set([starting_point])
    data = {0: 1}
    for i in range(steps):
        next_steps = []
        while queue:
            position = queue.pop(0)
            _next = determine_steps(garden, position, resolution)
            for _n in _next:
                if _n in visited:
                    continue
                next_steps.append(_n)
            visited.add(position)
        queue = list(set(next_steps))
        if i == 0:
            data[i + 1] = len(queue)
        else:
            data[i + 1] = data[i - 1] + len(queue)
    return data[steps]


print(determine_reachable_points(garden, starting_point, resolution, 64))
