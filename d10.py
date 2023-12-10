from string import ascii_lowercase
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Any
import math


@dataclass
class Node:
    index: int
    prev: Any
    steps: int = 0
    pipe: str = "S"

    def prev_direction(self):
        if not self.prev:
            return None
        if self.prev.index > self.index:
            if self.prev.index - 1 == self.index:
                return "W"
            return "N"
        else:
            if self.prev.index + 1 == self.index:
                return "E"
            return "S"

    def determine_neighbours(self, pipe_map, resolution):
        neighbours = []
        pd = self.prev_direction()
        if not pd:
            if self.index % resolution:
                neighbours.append(
                    Node(self.index - 1, self, self.steps, pipe_map[self.index - 1])
                )
            if self.index % resolution < resolution - 1:
                neighbours.append(
                    Node(self.index + 1, self, self.steps, pipe_map[self.index + 1])
                )
            if self.index > resolution:
                neighbours.append(
                    Node(
                        self.index - resolution,
                        self,
                        self.steps,
                        pipe_map[self.index - resolution],
                    )
                )
            if self.index < len(pipe_map) - resolution:
                neighbours.append(
                    Node(
                        self.index + resolution,
                        self,
                        self.steps,
                        pipe_map[self.index + resolution],
                    )
                )
            valid = []
            for v in neighbours:
                if v.pipe == ".":
                    continue
                valid.append(v)
            return valid
        else:
            try:
                nd = NEXT_DIRECTIONS[(pipe_map[self.index], pd)]
            except KeyError:
                return []
            next_node = Node(
                self.index + ND[nd], self, self.steps, pipe_map[self.index + ND[nd]]
            )
            if next_node.pipe == ".":
                return []
            return [next_node]

    def _determine_points(self):
        points = []
        node = self
        while node.prev:
            points.append(node.index)
            node = node.prev
        return points

    def determine_path_length(self):
        return len(self._determine_points())

    def determine_enclosed_space(self):
        points = self._determine_points()
        points.append(points[0])
        buffer = []
        lines = []
        for p in points:
            buffer.append(p)
            if len(buffer) <= 1:
                continue
            if buffer[1] - buffer[0] != buffer[-1] - buffer[-2]:
                buffer.pop()
                lines.append(buffer[:])
                if len(buffer) == 2:
                    buffer = [buffer[1], p]
                else:
                    buffer = [buffer[-1], p]
        lines.append(buffer[:])

        # Gauss's Area Formula (Shoelace formula) + Rearranged
        z = [(line[-1] % resolution, line[-1] // resolution) for line in lines]
        area = 0
        for i, v in enumerate(z):
            if i == len(z) - 1:
                next_x = z[0][0]
                next_y = z[0][1]
            else:
                next_x = z[i + 1][0]
                next_y = z[i + 1][1]
            area += (v[0] * next_y) - (v[1] * next_x)
        area = abs(area) // 2
        enclosed_points = area + 1 - len(points) / 2
        return math.ceil(enclosed_points)

    def __eq__(self, node):
        return self.index == node.index

    def __lt__(self, other):
        return self.steps < other.steps


def find_starting_index(height_map):
    return height_map.index("S")


def determine_loop(pipe_map, resolution):
    starting_index = find_starting_index(pipe_map)
    start_node = Node(starting_index, None)
    end_node = Node(starting_index, None)
    open_nodes = []
    closed_nodes = {}
    heappush(open_nodes, start_node)
    while open_nodes:
        current_node = heappop(open_nodes)
        if current_node == end_node and current_node.prev:
            return current_node
        for node in current_node.determine_neighbours(pipe_map, resolution):
            if node.index in closed_nodes:
                continue
            node.steps += 1
            if node in open_nodes:
                continue
            heappush(open_nodes, node)


CONNECTIONS = {
    ("|", "S"): ("L", "J", "|", "S"),
    ("|", "N"): ("F", "7", "|", "S"),
    ("-", "W"): ("L", "-", "F", "S"),
    ("-", "E"): ("-", "J", "7", "S"),
    ("L", "E"): ("J", "7", "S", "-"),
    ("L", "N"): ("F", "7", "S", "|"),
    ("J", "W"): ("L", "F", "S", "-"),
    ("J", "N"): ("7", "F", "S", "|"),
    ("7", "W"): ("L", "F", "S", "-"),
    ("7", "S"): ("L", "J", "S", "|"),
    ("F", "S"): ("L", "J", "S", "|"),
    ("F", "E"): ("J", "7", "S", "-"),
    "S": ("L", "J", "7", "F", "|", "-"),
}

NEXT_DIRECTIONS = {
    ("|", "S"): "S",
    ("|", "N"): "N",
    ("-", "W"): "W",
    ("-", "E"): "E",
    ("L", "W"): "N",
    ("L", "S"): "E",
    ("J", "E"): "N",
    ("J", "S"): "W",
    ("7", "E"): "S",
    ("7", "N"): "W",
    ("F", "N"): "E",
    ("F", "W"): "S",
}


with open("10") as file:
    file_input = file.read().splitlines()
pipe_map = [c for line in file_input for c in line]
resolution = len(file_input[0])
ND = {"S": resolution, "N": -resolution, "E": 1, "W": -1}
loop = determine_loop(pipe_map, resolution)
print(loop.determine_path_length() // 2)  # Part 1 Solution
print(loop.determine_enclosed_space())
