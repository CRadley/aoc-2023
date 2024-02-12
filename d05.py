from typing import List
from functools import cache

with open("inputs/d05") as file:
    lines = [line for line in file.read().splitlines() if line]


def determine_seeds(seed_line: str) -> List[int]:
    return list(map(int, seed_line.split(" ")[1:]))


def determine_seed_ranges(seeds: List[int]) -> List[range]:
    return [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]


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
                    source_start,
                    source_start + length,
                    dest_start - source_start,
                )
            )
    return ranges


def part_one(seeds: List[int], ranges) -> int:
    p1 = []
    for seed in seeds:
        current = seed
        for _r in ranges:
            for start, end, offset in _r:
                if start <= current < end:
                    current += offset
                    break
        p1.append(current)
    return min(p1)


def determine_crossovers(r1_min, r1_max, r2_min, r2_max):
    if r1_min >= r2_min and r1_max <= r2_max:
        return (r1_min, r1_max), None, None
    if r1_min < r2_min and r2_min <= r1_max <= r2_max:
        return (r2_min, r1_max), (r1_min, r1_max - 1), None
    if r2_max > r1_min >= r2_min and r1_max > r2_max:
        return (r1_min, r2_max), None, (r2_max, r1_max)
    if r1_min < r2_min and r2_max < r1_max:
        return (r2_min, r2_max), (r1_min, r2_min - 1), (r2_max, r1_max)
    return None, None, None


def part_two(seed_ranges: List[range], maps) -> int:
    current_ranges = seed_ranges[:]
    for i, m in enumerate(maps):
        next_ranges = []
        queue = current_ranges[:]
        while len(queue) > 0:
            current = queue.pop(0)
            for r in m:
                subrange, lower_range, upper_range = determine_crossovers(
                    *current, r[0], r[1]
                )
                if not subrange and not lower_range and not upper_range and r == m[-1]:
                    next_ranges.append(current)
                if subrange:
                    new = (subrange[0] + r[2], subrange[1] + r[2])
                    next_ranges.append(new)
                if lower_range:
                    queue.append(lower_range)
                if upper_range:
                    queue.append(upper_range)
                if subrange or lower_range or upper_range:
                    break
        current_ranges = next_ranges[:]
    return min(min(r) for r in current_ranges)


seeds = determine_seeds(lines[0])
seed_ranges = determine_seed_ranges(seeds)
ranges = determine_map_ranges(lines[2:])
print("P1 Start")
p1 = part_one(seeds, ranges)
print(p1)
print("P2 Start")
p2 = part_two(seed_ranges, ranges)
print(p2)
