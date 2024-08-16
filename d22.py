from dataclasses import dataclass
from re import findall


@dataclass
class Brick:
    x: tuple
    y: tuple
    z: tuple


bricks = []
with open("inputs/d22") as bricks_file:
    for line in bricks_file:
        values = list(
            map(int, findall(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)[0])
        )
        bricks.append(
            Brick(
                range(values[0], values[3] + 1),
                range(values[1], values[4] + 1),
                range(values[2], values[5] + 1),
            )
        )


def is_collision(b1, b2) -> bool:
    if len(b1.x) == 1:
        b1c = set((min(b1.x), y) for y in b1.y)
    else:
        b1c = set((x, min(b1.y)) for x in b1.x)
    if len(b2.x) == 1:
        b2c = set((min(b2.x), y) for y in b2.y)
    else:
        b2c = set((x, min(b2.y)) for x in b2.x)
    return bool(b1c & b2c)


is_collision(bricks[0], bricks[1])

bricks.sort(key=lambda brick: min(brick.z))
# falling....
for brick in bricks:
    if min(brick.z) == 1:
        continue
    stable = False
    while True:
        if stable or min(brick.z) == 1:
            break
        _bricks = [_brick for _brick in bricks if max(_brick.z) == min(brick.z) - 1]
        brick.z = range(min(brick.z) - 1, max(brick.z))
        for _brick in _bricks:
            if is_collision(brick, _brick) and max(_brick.z) == min(brick.z):
                brick.z = range(min(brick.z) + 1, max(brick.z) + 2)
                stable = True
                break


p1 = 0
for i in range(len(bricks)):
    new_bricks = bricks[0:i] + bricks[i + 1 : len(bricks)]
    for n_b in new_bricks:
        if min(n_b.z) == 1:
            continue
        _bricks = []
        for _brick in new_bricks:
            if max(_brick.z) == min(n_b.z) - 1:
                _bricks.append(_brick)
        if (
            any(not is_collision(n_b, _brick) for _brick in _bricks)
            or len(_bricks) == 0
        ):
            break
    else:
        p1 += 1
print(p1)
