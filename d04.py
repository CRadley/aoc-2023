import re
import math

with open("inputs/d04") as file:
    cards = [re.split("\s+", line) for line in file.read().split("\n")]
    pipe_index = cards[0].index("|")

p1 = 0
p2 = {i: 1 for i in range(len(cards))}

for i, card in enumerate(cards):
    numbers = list(map(int, filter(lambda x: all(y.isdigit() for y in x), card)))
    winning = set(numbers[: pipe_index - 2])
    personal = set(numbers[pipe_index - 2 :])
    matches = winning & personal
    if matches:
        p1 += int(math.pow(2, len(matches) - 1))
    for j in range(len(matches)):
        p2[i + j + 1] += p2[i]

print(p1)
print(sum(p2.values()))
