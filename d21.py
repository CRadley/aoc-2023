from typing import List, Tuple

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
            for n in determine_steps(garden, position, resolution):
                if n in visited:
                    continue
                next_steps.append(n)
            visited.add(position)
        queue = list(set(next_steps))
        if i == 0:
            data[i + 1] = len(queue)
        else:
            data[i + 1] = data[i - 1] + len(queue)
    return data[steps]


def part_one(garden: List[int], starting_point: int, resolution: int) -> int:
    return determine_reachable_points(garden, starting_point, resolution, 64)


def determine_cardinal_gardens(steps: int, resolution: int) -> int:
    return ((steps - resolution // 2) // resolution) - 1


def _determine_inner_major_garden_number(cardinal_gardens: int) -> int:
    return (cardinal_gardens + 1) ** 2


def _determine_inner_minor_garden_number(cardinal_gardens: int) -> int:
    return cardinal_gardens**2


def determine_inner_even_odd_garden_number(cardinal_gardens: int) -> Tuple[int, int]:
    """
    odd, even
    """
    return (
        _determine_inner_major_garden_number(cardinal_gardens),
        _determine_inner_minor_garden_number(cardinal_gardens),
    )


def part_two(
    garden: List[int], starting_point: int, resolution: int, steps: int
) -> int:
    cardinal_gardens = determine_cardinal_gardens(steps, resolution)
    odd_gardens, even_gardens = determine_inner_even_odd_garden_number(cardinal_gardens)
    full_odd = determine_reachable_points(garden, starting_point, resolution, 1001)
    full_even = determine_reachable_points(garden, starting_point, resolution, 1000)
    ct = determine_reachable_points(
        garden, starting_point + (resolution // 2) * resolution, resolution, resolution
    )
    cr = determine_reachable_points(
        garden, starting_point - resolution // 2, resolution, resolution
    )
    cb = determine_reachable_points(
        garden, starting_point - (resolution // 2) * resolution, resolution, resolution
    )
    cl = determine_reachable_points(
        garden, starting_point + resolution // 2, resolution, resolution
    )
    _o, _e = determine_inner_even_odd_garden_number(cardinal_gardens + 2)
    even_diff = (abs(even_gardens - _e) - 4) // 4
    odd_diff = (abs(odd_gardens - _o) - 4) // 4
    return (
        (full_even * even_gardens)
        + (full_odd * odd_gardens)
        + ct
        + cb
        + cl
        + cr
        + (
            odd_diff
            * sum(
                [
                    determine_reachable_points(
                        garden, resolution * (resolution - 1), resolution, resolution
                    ),
                    determine_reachable_points(garden, 0, resolution, resolution),
                    determine_reachable_points(
                        garden, resolution - 1, resolution, resolution
                    ),
                    determine_reachable_points(
                        garden, (resolution * resolution) - 1, resolution, resolution
                    ),
                ]
            )
        )
        + (
            even_diff
            * sum(
                [
                    determine_reachable_points(
                        garden, resolution * (resolution - 1), resolution, 65
                    ),
                    determine_reachable_points(garden, 0, resolution, 65),
                    determine_reachable_points(garden, resolution - 1, resolution, 65),
                    determine_reachable_points(
                        garden, (resolution * resolution) - 1, resolution, 65
                    ),
                ]
            )
        )
    )


print(part_one(garden, starting_point, resolution))
print(part_two(garden, starting_point, resolution, 26501365))
# 608191615942056 too low......
# 608193921334414
# 608191615935010
