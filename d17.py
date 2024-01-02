from typing import Self, List
from heapq import heappop, heappush
from enum import Enum


with open("inputs/d17") as file:
    lines = file.read().splitlines()
    resolution = len(lines[0])
    city_blocks = [int(c) for line in lines for c in line]


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Node:
    def __init__(
        self,
        index: int,
        prev: Self = None,
        heat_loss: int = 0,
        steps_in_direction: int = 0,
        direction: Direction = None,
    ) -> None:
        self.index = index
        self.prev: Self = prev
        self.heat_loss = heat_loss
        self.steps_in_direction = steps_in_direction
        self.direction = direction

    def determine_next_moves(
        self, city: List[str], resolution: int, min_moves: int, max_moves: int
    ) -> List[Self]:
        if not self.direction:
            return [
                Node(1, self, self.heat_loss, 1, Direction.RIGHT),
                Node(
                    resolution,
                    self,
                    self.heat_loss,
                    1,
                    Direction.DOWN,
                ),
            ]
        up_node = Node(
            self.index - resolution,
            self,
            self.heat_loss,
            self.steps_in_direction * (self.direction == Direction.UP) + 1,
            Direction.UP,
        )
        right_node = Node(
            self.index + 1,
            self,
            self.heat_loss,
            self.steps_in_direction * (self.direction == Direction.RIGHT) + 1,
            Direction.RIGHT,
        )
        down_node = Node(
            self.index + resolution,
            self,
            self.heat_loss,
            self.steps_in_direction * (self.direction == Direction.DOWN) + 1,
            Direction.DOWN,
        )
        left_node = Node(
            self.index - 1,
            self,
            self.heat_loss,
            self.steps_in_direction * (self.direction == Direction.LEFT) + 1,
            Direction.LEFT,
        )
        candidate = []
        if self.direction == Direction.UP:
            if self.steps_in_direction >= min_moves:
                candidate.extend([left_node, right_node])
            if self.steps_in_direction < max_moves:
                candidate.append(up_node)
        elif self.direction == Direction.RIGHT:
            if self.steps_in_direction >= min_moves:
                candidate.extend([up_node, down_node])
            if self.steps_in_direction < max_moves:
                candidate.append(right_node)
        elif self.direction == Direction.DOWN:
            if self.steps_in_direction >= min_moves:
                candidate.extend([left_node, right_node])
            if self.steps_in_direction < max_moves:
                candidate.append(down_node)
        elif self.direction == Direction.LEFT:
            if self.steps_in_direction >= min_moves:
                candidate.extend([up_node, down_node])
            if self.steps_in_direction < max_moves:
                candidate.append(left_node)
        actual = []
        for c in candidate:
            if c.direction == Direction.UP and c.index >= 0:
                actual.append(c)
            elif c.direction == Direction.RIGHT and c.index % resolution:
                actual.append(c)
            elif c.direction == Direction.DOWN and c.index < len(city):
                actual.append(c)
            elif (
                c.direction == Direction.LEFT and c.index % resolution != resolution - 1
            ):
                actual.append(c)
        return actual

    def __lt__(self, other: Self):
        return self.heat_loss < other.heat_loss

    def __eq__(self, other: Self) -> bool:
        return (
            self.index == other.index
            and self.direction == other.direction
            and self.steps_in_direction == other.steps_in_direction
        )

    def __str__(self) -> str:
        return f"{self.index}, {self.direction}, {self.heat_loss}"


def determine_lowest_heat_loss(
    city: List[int], resolution: int, min_moves: int, max_moves: int
) -> Node:
    start_node = Node(0)
    end_index = len(city) - 1
    open_nodes = []
    closed_nodes = {}
    _open_nodes = {}
    heappush(open_nodes, start_node)
    while open_nodes:
        current_node = heappop(open_nodes)
        if (
            current_node.index == end_index
            and min_moves <= current_node.steps_in_direction
        ):
            return current_node
        for node in current_node.determine_next_moves(
            city, resolution, min_moves, max_moves
        ):
            if (
                node.index,
                node.direction,
                node.steps_in_direction,
            ) in closed_nodes or (
                node.index,
                node.direction,
                node.steps_in_direction,
            ) in _open_nodes:
                continue
            node.heat_loss = node.prev.heat_loss + city[node.index]
            heappush(open_nodes, node)
            _open_nodes[
                (
                    node.index,
                    node.direction,
                    node.steps_in_direction,
                )
            ] = None

        closed_nodes[
            (
                current_node.index,
                current_node.direction,
                current_node.steps_in_direction,
            )
        ] = None
    return start_node


p1 = determine_lowest_heat_loss(city_blocks, resolution, 0, 3)
print(p1.heat_loss)
p2 = determine_lowest_heat_loss(city_blocks, resolution, 4, 10)
print(p2.heat_loss)
