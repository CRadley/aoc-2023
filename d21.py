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


queue = determine_steps(garden, starting_point, resolution)
steps = 200
for _ in range(steps - 1):
    next_steps = []
    while queue:
        position = queue.pop(0)
        next_steps.extend(determine_steps(garden, position, resolution))
    queue = list(set(next_steps))


for p in queue:
    garden[p] = "O"

for i in range(0, len(garden), resolution):
    print("".join(garden[i : i + resolution]))
print(len(queue))
