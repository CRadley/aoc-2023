from typing import List


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
                    dest_start,
                    length,
                    dest_start + length,
                )
            )
    return ranges


def part_one(seeds: List[int], ranges) -> int:
    p1 = []
    for seed in seeds:
        current = seed
        for _r in ranges:
            for r in _r:
                if r[0] <= current <= r[1]:
                    current += r[2] - r[0]
                    break
        p1.append(current)
    return min(p1)


def part_two(seed_ranges: List[range], ranges) -> int:
    p2 = 0
    while True:
        current = p2
        for _r in ranges[::-1]:
            for r in _r:
                if r[2] <= current < r[4]:
                    current -= r[2] - r[0]
                    break
        for sr in seed_ranges:
            if sr[0] <= current <= sr[1]:
                return p2
        p2 += 1


seeds = determine_seeds(lines[0])
seed_ranges = determine_seed_ranges(seeds)
ranges = determine_map_ranges(lines[2:])
assert part_one(seeds, ranges) == 35
assert part_two(seed_ranges, ranges) == 46
