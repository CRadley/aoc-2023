from typing import List


with open("inputs/d05") as file:
    lines = [line for line in file.read().splitlines() if line]


def determine_seeds(seed_line: str) -> List[int]:
    return list(map(int, seed_line.split(" ")[1:]))


def determine_seed_ranges(seeds: List[int]) -> List[range]:
    return [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]


def determine_map_ranges(map_lines: List[str]):
    maps = []
    current_map = []
    for line in map_lines:
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
                    range(source_start, source_start + length),
                    range(dest_start, dest_start + length),
                    dest_start - source_start,
                )
            )
    return ranges


def part_one(seeds: List[int], ranges) -> int:
    p1 = []
    for seed in seeds:
        current = seed
        for _r in ranges:
            for source, _, offset in _r:
                if current in source:
                    current += offset
                    break
        p1.append(current)
    return min(p1)


def determine_crossover(prev_range: range, next_range: range) -> range:
    return range(
        max(prev_range[0], next_range[0]), min(prev_range[-1], next_range[-1]) + 1
    )


def part_two(seed_ranges: List[range], maps) -> int:
    current_ranges = seed_ranges[:]
    for i, m in enumerate(maps):
        print(i)
        next_ranges = []
        queue = current_ranges[:]
        while queue:
            current = queue.pop(0)
            print(current)
            for r in m:
                crossover = determine_crossover(current, r[0])
                if len(crossover) == 0:
                    if r == m[-1]:
                        next_ranges.append(current)
                    continue
                elif crossover == current:
                    next_ranges.append(range(current[0] + r[2], current[-1] + r[2] + 1))
                    break
                else:
                    if min(current) == min(crossover):
                        queue.append(range(max(crossover) + 1, max(current) + 1))
                    else:
                        queue.append(range(min(current), min(crossover)))
        current_ranges = next_ranges[:]
    return min(min(r) for r in current_ranges)


seeds = determine_seeds(lines[0])
seed_ranges = determine_seed_ranges(seeds)
ranges = determine_map_ranges(lines[2:])
print("P1 Start")
p1 = part_one(seeds, ranges)
print("P1 Finish")
print("P2 Start")
p2 = part_two(seed_ranges, ranges)
print("P2 Finish")

assert p1 == 551761867, p1
assert p2 == 57451709, p2
