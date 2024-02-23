import re


with open("inputs/d24") as file:
    hailstones = [
        tuple(map(int, [m.group(1) for m in re.finditer(r"([\-\d]+)", line)]))
        for line in file.read().splitlines()
    ]


def paths_intersect_in_future(h1, h2, t_min, t_max) -> bool:
    g1 = h1[4] / h1[3]
    g2 = h2[4] / h2[3]
    if g1 == g2:
        return False
    c1 = h1[1] - g1 * h1[0]
    c2 = h2[1] - g2 * h2[0]

    x = (c1 - c2) / (g2 - g1)
    y = g1 * x + c1
    # Determine if x, y is in that past for h1
    if h1[0] > x and h1[3] > 0 or h1[1] > y and h1[4] > 0:
        return False
    if h1[0] < x and h1[3] < 0 or h1[1] < y and h1[4] < 0:
        return False
    # Determine if x, y is in that past for h2
    if h2[0] > x and h2[3] > 0 or h2[1] > y and h2[4] > 0:
        return False
    if h2[0] < x and h2[3] < 0 or h2[1] < y and h2[4] < 0:
        return False
    return t_min <= x <= t_max and t_min <= y <= t_max


def part_one(hailstones) -> int:
    p1 = 0
    for i, h in enumerate(hailstones):
        for j, _h in enumerate(hailstones[i + 1 :]):
            if paths_intersect_in_future(h, _h, 200000000000000, 400000000000000):
                p1 += 1
    return p1


print(part_one(hailstones))
