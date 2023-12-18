with open("inputs/d05") as file:
    lines = [line for line in file.read().splitlines() if line]

seeds = list(map(int, lines[0].split(" ")[1:]))

maps = []
current_map = []

for line in lines[2:]:
    if "map" in line:
        maps.append(current_map[:])
        current_map = []
    else:
        current_map.append(list(map(int, line.split(" "))))
    if line == lines[-1]:
        maps.append(current_map[:])


ranges = [[] for _ in range(7)]
for i, m in enumerate(maps):
    for dest_start, source_start, length in m:
        ranges[i].append(
            (
                source_start,
                source_start + length,
                dest_start,
                length,
                dest_start + length,
            )
        )

p1 = []
for seed in seeds:
    current = seed
    for _r in ranges:
        for r in _r:
            if r[0] <= current <= r[1]:
                current += r[2] - r[0]
                break
    p1.append(current)


seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
p2 = 0
found = False
while not found:
    current = p2
    for _r in ranges[::-1]:
        for r in _r:
            if r[2] <= current < r[4]:
                current -= r[2] - r[0]
                break
    for sr in seed_ranges:
        if sr[0] <= current <= sr[1]:
            found = True
            break
    if not found:
        p2 += 1
print(p2)
