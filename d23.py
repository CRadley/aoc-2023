from typing import List, Self, Dict
from heapq import heappush, heappop
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Edge:
    to: Point
    weight: int


def walk_graph(
    graph: Dict[Point, List[Edge]],
    current: Point,
    target: Point,
    paths: List[int],
    path: List[Node],
    depth: int = 0,
):
    if current in path:
        return
    if current == target:
        paths.append(depth)
        return
    path.append(current)
    for edge in graph[current]:
        walk_graph(graph, edge.to, target, paths, path, depth + edge.weight)
    path.pop()


def dfs(forest: List[List[str]], start: Node, target: Node) -> int:
    paths = []
    path = []
    walk_graph(forest, start, target, paths, path)
    return max(paths)


def is_crossroad(forest: List[List[str]], cx: int, cy: int) -> bool:
    if cx == 0 or cx == len(forest[-1]) - 1 or cy == 0 or cy == len(forest) - 1:
        return True
    walls = 0
    for x, y in DIRECTIONS:
        nx = x + cx
        ny = y + cy
        if forest[ny][nx] == "#":
            walls += 1
    return walls <= 1


def determine_crossroads(forest: List[List[str]]):
    c = []
    for y, row in enumerate(forest):
        for x, value in enumerate(row):
            if value != ".":
                continue
            if is_crossroad(forest, x, y):
                c.append(Point(x, y))
    return c


points = determine_crossroads(forest)


def next_points(forest: List[List[str]], current: Point) -> List[Point]:
    nodes = []
    cx, cy = current.x, current.y
    for x, y in DIRECTIONS:
        node = Point(cx + x, cy + y)
        if (
            node.x < 0
            or node.x >= len(forest[-1])
            or node.y < 0
            or node.y >= len(forest)
        ):
            continue
        if forest[node.y][node.x] == "#":
            continue
        if node.y == current.y and node.x == current.x:
            continue
        nodes.append(node)
    return nodes


def determine_edges(
    forest: List[List[str]],
    current: Point,
    points: List[Point],
    edges: List[Edge],
    path: List[Point],
    depth: int = 0,
):
    if current in path:
        return
    if current in points and depth != 0:
        edges.append(Edge(current, depth))
        return
    path.append(current)
    for point in next_points(forest, current):
        determine_edges(forest, point, points, edges, path, depth + 1)
    path.pop()


graph = {}

for point in points:
    edges = []
    path = []
    determine_edges(forest, point, points, edges, path)
    graph[point] = edges[:]

START = Point(1, 0)
END = Point(len(forest[-1]) - 2, len(forest) - 1)

print(dfs(graph, START, END))
