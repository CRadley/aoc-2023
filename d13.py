from typing import List


with open("inputs/d13") as file:
    mirror_fields = [
        [list(line) for line in e.splitlines()] for e in file.read().split("\n\n")
    ]


def determine_columns(mirrors: List[str]):
    c = []
    for i in range(len(mirrors[0])):
        c.append([v[i] for _, v in enumerate(mirrors)])
    return c


def is_refelection_point(mirrors: List[str], midpoint):
    hi = midpoint
    lo = midpoint - 1
    while lo >= 0 and hi < len(mirrors):
        if mirrors[lo] != mirrors[hi]:
            return False
        hi += 1
        lo -= 1
    return True


def determine_smudge_mutations(mirror_field):
    fixes = []
    for i, row in enumerate(mirror_field):
        for j, value in enumerate(row):
            new_mirror_field = [row[:] for row in mirror_field]
            new_mirror_field[i][j] = "#" if value == "." else "."
            fixes.append(new_mirror_field)
    return fixes


def determine_reflection(mirror_fields, i, prev):
    for field in mirror_fields:
        columns = determine_columns(field)
        for j, _ in enumerate(field):
            if not j:
                continue
            if is_refelection_point(field, j) and (i, j, "r") not in prev:
                return j * 100, (i, j, "r")
        for j, _ in enumerate(columns):
            if not j:
                continue
            if is_refelection_point(columns, j) and (i, j, "c") not in prev:
                return j, (i, j, "c")


def sum_reflection_points(mirror_fields, prev, fix):
    total = 0
    rp = []
    for i, field in enumerate(mirror_fields):
        mutations = determine_smudge_mutations(field) if fix else [field]
        value, reflection_point = determine_reflection(mutations, i, prev)
        total += value
        rp.append(reflection_point)
    return total, rp


p1, rp = sum_reflection_points(mirror_fields, [], False)
p2, _ = sum_reflection_points(mirror_fields, rp, True)
print(p1, p2)
