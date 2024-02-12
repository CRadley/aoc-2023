from typing import List, Tuple

with open("inputs/d05") as file:
    lines = [line for line in file.read().splitlines() if line]


def determine_seeds(seed_line):
    return list(map(int, seed_line.split(" ")[1:]))


def determine_seed_ranges(seeds):
    return [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]


def determine_map_ranges(map_lines):
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
                    source_start + length - 1,
                    dest_start - source_start,
                )
            )
    return ranges


def part_one(seeds, ranges):
    p1 = []
    for seed in seeds:
        current = seed
        for _r in ranges:
            for start, end, offset in _r:
                if start <= current <= end:
                    current += offset
                    break
        p1.append(current)
    return min(p1)


def determine_crossovers(r1_min, r1_max, r2_min, r2_max):
    if r1_min >= r2_min and r1_max <= r2_max:
        return (r1_min, r1_max), None, None
    if r1_min < r2_min and r2_min <= r1_max <= r2_max:
        return (r2_min, r1_max), (r1_min, r2_min - 1), None
    if r2_max > r1_min >= r2_min and r1_max > r2_max:
        return (r1_min, r2_max), None, (r2_max + 1, r1_max)
    if r1_min < r2_min and r2_max < r1_max:
        return (r2_min, r2_max), (r1_min, r2_min - 1), (r2_max + 1, r1_max)
    return None, None, None


def part_two(seed_ranges, maps):
    next_queue = seed_ranges[:]
    for m in maps:
        queue = next_queue[:]
        next_queue = []
        while queue:
            current = queue.pop(0)
            for r in m:
                subrange, lower, upper = determine_crossovers(*current, r[0], r[1])
                if not subrange and not lower and not upper and r == m[-1]:
                    next_queue.append(current)
                if lower:
                    queue.append(lower)
                if upper:
                    queue.append(upper)
                if subrange:
                    next_queue.append((subrange[0] + r[2], subrange[1] + r[2]))
                    break
        queue = next_queue[:]
    return min(_p[0] for _p in next_queue)


seeds = determine_seeds(lines[0])
seed_ranges = determine_seed_ranges(seeds)
ranges = determine_map_ranges(lines[2:])
print(part_one(seeds, ranges))
print(part_two(seed_ranges, ranges))
