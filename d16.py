from enum import Enum, auto


with open("inputs/d16") as file:
    lines = file.read().splitlines()
    resolution = len(lines[0])
    data = [c for l in lines for c in l]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def determine_energised(index, d):
    stack = []
    energised = set()
    stack.append((index, d))

    while stack:
        index, direction = stack.pop()
        if (index, direction) in energised:
            continue
        energised.add((index, direction))
        if direction == Direction.UP:
            if index < resolution:
                continue
            next_index = index - resolution
            if data[next_index] in ("|", "."):
                stack.append((next_index, direction))
            elif data[next_index] == "/":
                stack.append((next_index, Direction.RIGHT))
            elif data[next_index] == "\\":
                stack.append((next_index, Direction.LEFT))
            elif data[next_index] == "-":
                stack.append((next_index, Direction.LEFT))
                stack.append((next_index, Direction.RIGHT))

        elif direction == Direction.DOWN:
            if index > len(data) - resolution - 1:
                continue
            next_index = index + resolution
            if data[next_index] in ("|", "."):
                stack.append((next_index, direction))
            elif data[next_index] == "/":
                stack.append((next_index, Direction.LEFT))
            elif data[next_index] == "\\":
                stack.append((next_index, Direction.RIGHT))
            elif data[next_index] == "-":
                stack.append((next_index, Direction.LEFT))
                stack.append((next_index, Direction.RIGHT))

        elif direction == Direction.LEFT:
            if not index % resolution:
                continue
            next_index = index - 1
            if data[next_index] in ("-", "."):
                stack.append((next_index, direction))
            elif data[next_index] == "/":
                stack.append((next_index, Direction.DOWN))
            elif data[next_index] == "\\":
                stack.append((next_index, Direction.UP))
            elif data[next_index] == "|":
                stack.append((next_index, Direction.UP))
                stack.append((next_index, Direction.DOWN))

        elif direction == Direction.RIGHT:
            if index % resolution == resolution - 1 and 0 <= index:
                continue
            next_index = index + 1
            if data[next_index] in ("-", "."):
                stack.append((next_index, direction))
            elif data[next_index] == "/":
                stack.append((next_index, Direction.UP))
            elif data[next_index] == "\\":
                stack.append((next_index, Direction.DOWN))
            elif data[next_index] == "|":
                stack.append((next_index, Direction.UP))
                stack.append((next_index, Direction.DOWN))
    return len(set([value[0] for value in energised if 0 <= value[0] < len(data)]))


p1 = determine_energised(-1, Direction.RIGHT)

p2_starting_directions = [
    *[(i, Direction.RIGHT) for i in range(-1, len(data), resolution)],
    *[(i, Direction.LEFT) for i in range(resolution, len(data), resolution)],
    *[(i, Direction.UP) for i in range(len(data), len(data) + resolution, 1)],
    *[(i, Direction.DOWN) for i in range(-resolution, 0)],
]
p2 = max([determine_energised(*sp) for sp in p2_starting_directions])
print(p1)
print(p2)
