import itertools
import math

with open("input") as file:
    lines = file.read().splitlines()
    moves = lines[0]
    data = {
        line.split(" = ")[0]: line.split(" = ")[1][1:-1].split(", ")
        for line in lines[2:]
    }

position = "AAA"
p1 = 0
for move in itertools.cycle(moves):
    p1 += 1
    position = data[position][move == "R"]
    if position == "ZZZ":
        break
print(p1)


positions = [[key, []] for key in data if key.endswith("A")]

p2 = 0
for i, move in enumerate(itertools.cycle(moves)):
    if all(len(p[1]) >= 1 for p in positions):
        break
    p2 += 1
    for p in positions:
        p[0] = data[p[0]][move == "R"]
        if p[0].endswith("Z"):
            p[1].append(i + 1)
print(math.lcm(*[p[1][0] for p in positions]))
