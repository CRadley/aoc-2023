import re
from typing import List, Tuple
from functools import cache


PATTERN = re.compile(r"[#?]+")


with open("inputs/d12") as file:
    data = [
        (line.split(" ")[0], tuple(map(int, line.split(" ")[1].split(","))))
        for line in file.read().splitlines()
    ]


def unfold(data):
    return [
        (
            "?".join(row[0] for _ in range(5)),
            row[1] * 5,
        )
        for row in data
    ]


@cache
def valid_arrangements(string: str, required: Tuple[int], size: int) -> int:
    total = 0
    if len(string) == 0:
        if len(required) == 1:
            return required[0] == size
        return len(required) == 0
    if len(required) == 0:
        return not "#" in string
    if string[0] in (".", "?"):
        if required[0] == size:
            total += valid_arrangements(string[1:], required[1:], 0)
        elif size == 0:
            total += valid_arrangements(string[1:], required, size)
    if string[0] in ("#", "?"):
        total += valid_arrangements(string[1:], required, size + 1)
    return total


if __name__ == "__main__":
    # This is required as tests have been added for the valid_arrangements function
    p1 = sum(valid_arrangements(*d, 0) for d in data)
    print(p1)
    unfolded = unfold(data)
    p2 = sum(valid_arrangements(*d, 0) for d in unfolded)
    print(p2)
