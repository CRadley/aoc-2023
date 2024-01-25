from typing import List, Self
from heapq import heappush, heappop
from dataclasses import dataclass
import sys

sys.setrecursionlimit(10000)

with open("inputs/d23") as file:
    forest = [list(line) for line in file.read().splitlines()]

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


@dataclass
class Node:
    x: int
    y: int
    prev: Self | None = None
    distance: int = 0

    def __gt__(self, other: Self) -> bool:
        return self.distance < other.distance

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y


def determine_next_moves(forest: List[List[str]], current: Node) -> List[Node]:
    nodes = []
    cx, cy = current.x, current.y
    if forest[cy][cx] == "^":
        return [Node(cx, cy - 1, current, current.distance + 1)]
    if forest[cy][cx] == ">":
        return [Node(cx + 1, cy, current, current.distance + 1)]
    if forest[cy][cx] == "v":
        return [Node(cx, cy + 1, current, current.distance + 1)]
    if forest[cy][cx] == "<":
        return [Node(cx - 1, cy, current, current.distance + 1)]
    for x, y in DIRECTIONS:
        node = Node(cx + x, cy + y, current, current.distance + 1)
        if (
            node.x < 0
            or node.x >= len(forest[-1])
            or node.y < 0
            or node.y >= len(forest)
        ):
            continue
        if forest[node.y][node.x] == "#":
            continue
        if (
            current.prev is not None
            and node.y == current.prev.y
            and node.x == current.prev.x
        ):
            continue
        if x == 1 and forest[node.y][node.x] == "<":
            continue
        if x == -1 and forest[node.y][node.x] == ">":
            continue
        if y == 1 and forest[node.y][node.x] == "^":
            continue
        if y == -1 and forest[node.y][node.x] == "v":
            continue
        nodes.append(node)
    return nodes


def longest_path(forest: List[List[str]], start: Node, target: Node) -> Node:
    queue = []
    heappush(queue, start)
    seen = {}
    paths = []
    while queue:
        current = heappop(queue)
        if current.x == target.x and target.y == current.y:
            paths.append(current)
            continue
        seen[(current.x, current.y, current.distance)] = True
        for node in determine_next_moves(forest, current):
            if (node.x, node.y, current.distance) in seen:
                continue
            heappush(queue, node)
    return paths


start = Node(1, 0, None)
end = Node(len(forest[-1]) - 2, len(forest) - 1)

path = longest_path(forest, start, end)
print(max(p.distance for p in path))


def determine_next_moves_2(forest: List[List[str]], current: Node) -> List[Node]:
    nodes = []
    cx, cy = current.x, current.y
    for x, y in DIRECTIONS:
        node = Node(cx + x, cy + y, current, current.distance + 1)
        if (
            node.x < 0
            or node.x >= len(forest[-1])
            or node.y < 0
            or node.y >= len(forest)
        ):
            continue
        if forest[node.y][node.x] == "#":
            continue
        if (
            current.prev is not None
            and node.y == current.prev.y
            and node.x == current.prev.x
        ):
            continue
        nodes.append(node)
    return nodes


def walk_forest(
    forest: List[List[str]],
    current: Node,
    target: Node,
    paths: List[int],
    path: List[Node],
    depth: int = 0,
):
    if current.x == target.x and current.y == target.y:
        paths.append({(path[i].x, path[i].y): i + 1 for i in range(depth)})
        return
    if current in path:
        return
    path.append(current)
    for node in determine_next_moves_2(forest, current):
        walk_forest(forest, node, target, paths, path, depth + 1)
    path.pop()


def dfs(forest: List[List[str]], start: Node, target: Node) -> int:
    paths = []
    path = []
    walk_forest(forest, start, target, paths, path, 0)
    lengths = [max(p.values()) for p in paths]
    return max(lengths)


print(dfs(forest, start, end))
