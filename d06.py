import re
import math


with open("input6") as file:
    lines = [re.split(r"\s+", line) for line in file.read().splitlines()]
    races = [
        (int(values[0]), int(values[1]))
        for values in zip(*lines)
        if all(v.isnumeric() for v in values)
    ]
    longer_race = (
        int("".join(str(c[0]) for c in races)),
        int("".join(str(c[1]) for c in races)),
    )


def calculate_winners(time, record):
    winners = 0
    for i in range(0, time + 1):
        if i * (time - i) > record:
            winners += 1
    return winners


print(math.prod(calculate_winners(*race) for race in races))
print(calculate_winners(*longer_race))
