from dataclasses import dataclass
from re import findall


@dataclass
class Brick:
    coords: set[tuple[int, int]]
    z: int
    _z: int


def create_coords(x, _x, y, _y) -> set[tuple[int, int]]:
    if x == _x:
        return set((x, y) for y in range(y, _y + 1))
    else:
        return set((x, y) for x in range(x, _x + 1))


bricks = []
with open("inputs/d22") as bricks_file:
    for line in bricks_file:
        values = list(
            map(int, findall(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)[0])
        )
        bricks.append(
            Brick(
                create_coords(values[0], values[3], values[1], values[4]),
                values[2],
                values[5],
            )
        )


bricks.sort(key=lambda brick: brick.z)
print("execute falling")


# falling....
def fall(bricks: list[Brick]):
    for brick in bricks:
        if brick.z == 1:
            continue
        stable = False
        while True:
            if stable or brick.z == 1:
                break
            _bricks = [_brick for _brick in bricks if _brick._z == brick.z - 1]
            brick.z -= 1
            brick._z -= 1
            for _brick in _bricks:
                if bool(brick.coords & _brick.coords):
                    brick.z += 1
                    brick._z += 1
                    stable = True
                    break


print("Part 1...")
bricks.sort(key=lambda brick: brick.z)
fall(bricks)
p1 = 0
for i in range(len(bricks)):
    print(i)
    new_bricks = bricks[0:i] + bricks[i + 1 : len(bricks)]
    for n_b in new_bricks:
        if n_b.z == 1:
            continue
        _bricks = []
        for _brick in new_bricks:
            if _brick._z == n_b.z - 1 and n_b.coords & _brick.coords:
                _bricks.append(_brick)
        if len(_bricks) == 0:
            break
    else:
        p1 += 1
print("Value:", p1)
p2 = 0
print("Part 2...")
for i in range(len(bricks)):
    new_bricks = bricks[0:i] + bricks[i + 1 : len(bricks)]
    new_bricks = [Brick(b.coords, b.z, b._z) for b in new_bricks]
    backup = [Brick(b.coords, b.z, b._z) for b in new_bricks]
    for brick in new_bricks:
        if brick.z == 1:
            continue
        stable = False
        while True:
            if stable or brick.z == 1:
                break
            _bricks = [_brick for _brick in new_bricks if _brick._z == brick.z - 1]
            brick.z -= 1
            brick._z -= 1
            for _brick in _bricks:
                if bool(brick.coords & _brick.coords):
                    brick.z += 1
                    brick._z += 1
                    stable = True
                    break
    x = sum(a != b for a, b in zip(new_bricks, backup))
    print(i, x)
    p2 += x
print("Value:", p2)
