import re
from typing import List

PATTERN = re.compile(r"[#]+")


with open("input") as file:
    data = [
        (line.split(" ")[0], list(map(int, line.split(" ")[1].split(","))))
        for line in file.read().splitlines()
    ]

unfolded = [
    (
        "?".join(row[0] for _ in range(5)),
        row[1] * 5,
    )
    for _ in range(5)
    for row in data
]


def validate_string(string: str, requirements: List[int]) -> bool:
    matches = re.findall(PATTERN, string)
    if matches:
        match_lengths = [len(x) for x in matches]
        return match_lengths == requirements
    return 0


def valid_arrangements(string: str, requirements: List[int]) -> int:
    total = 0
    if "?" not in string:
        return validate_string(string, requirements)
    index = string.index("?")
    left = f"{string[:index]}#{string[index + 1:]}"
    right = f"{string[:index]}.{string[index + 1:]}"
    total += valid_arrangements(left, requirements)
    total += valid_arrangements(right, requirements)
    return total


p1 = sum(valid_arrangements(*d) for d in data)
print(p1)
