with open("input11") as file:
    galaxy = [list(line) for line in file.read().splitlines()]


def determine_rows_to_expand(galaxy):
    return [i for i, row in enumerate(galaxy) if all(r == "." for r in row)]


def determine_colums_to_expand(galaxy):
    return [i for i in range(len(galaxy[0])) if all(row[i] == "." for row in galaxy)]


def determine_expanded_star_positions(galaxy, rows_to_expand, cols_to_expand, scale=1):
    stars = []
    expansion_scale = scale - 1
    for x, r in enumerate(galaxy):
        for y, c in enumerate(r):
            if c == "#":
                x_expansion = sum(x > r for r in rows_to_expand) * expansion_scale
                y_expansion = sum(y > c for c in cols_to_expand) * expansion_scale
                stars.append((x + x_expansion, y + y_expansion))
    return stars


def calculate_distance(stars):
    total = 0
    added = {}
    for s in stars:
        for _s in stars:
            if s == _s or (s, _s) in added or (_s, s) in added:
                continue
            added[(s, _s)] = None
            added[(_s, s)] = None
            total += abs(s[0] - _s[0]) + abs(s[1] - _s[1])
    return total


rows_to_expand = determine_rows_to_expand(galaxy)
cols_to_expand = determine_colums_to_expand(galaxy)
stars_p1 = determine_expanded_star_positions(galaxy, rows_to_expand, cols_to_expand, 2)
stars_p2 = determine_expanded_star_positions(
    galaxy, rows_to_expand, cols_to_expand, 1000000
)

print(calculate_distance(stars_p1))
print(calculate_distance(stars_p2))
