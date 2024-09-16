import re
from sympy import Symbol
from sympy.solvers import solve


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
        for _, _h in enumerate(hailstones[i + 1 :]):
            if paths_intersect_in_future(h, _h, 200000000000000, 400000000000000):
                p1 += 1
    return p1


def part_two(hailstones) -> int:
    """
    To solve a system of equations, there must be
    an equal number of equations to the number of
    unknowns.

    There are 6 unknowns for the rock (x, y, z, vx, vy, vz)
    and 1 per hailstone (t)

    We can therefore use a system of 9 equations to solve for x,y,z

    x + (t1 * vx) == H1x + (t1 * H1vx)
    y + (t1 * vy) == H1y + (t1 * H1vy)
    z + (t1 * vz) == H1z + (t1 * H1vz) etc...

    Requires the use of sympy [https://pypi.org/project/sympy/]
    """
    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")
    vx = Symbol("vx")
    vy = Symbol("vy")
    vz = Symbol("vz")
    t1 = Symbol("t1")
    t2 = Symbol("t2")
    t3 = Symbol("t3")
    eq1 = x + (t1 * vx) - hailstones[-3][0] + (hailstones[-3][3] * t1)
    eq2 = y + (t1 * vy) - hailstones[-3][1] + (hailstones[-3][4] * t1)
    eq3 = z + (t1 * vz) - hailstones[-3][2] + (hailstones[-3][5] * t1)
    eq4 = x + (t2 * vx) - hailstones[-2][0] + (hailstones[-2][3] * t2)
    eq5 = y + (t2 * vy) - hailstones[-2][1] + (hailstones[-2][4] * t2)
    eq6 = z + (t2 * vz) - hailstones[-2][2] + (hailstones[-2][5] * t2)
    eq7 = x + (t3 * vx) - hailstones[-1][0] + (hailstones[-1][3] * t3)
    eq8 = y + (t3 * vy) - hailstones[-1][1] + (hailstones[-1][4] * t3)
    eq9 = z + (t3 * vz) - hailstones[-1][2] + (hailstones[-1][5] * t3)
    values = solve(
        [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], x, y, z, vx, vy, vz, t1, t2, t3
    )
    return sum(values[0][:3])


print(part_one(hailstones))
print(part_two(hailstones))
