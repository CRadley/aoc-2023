from collections import defaultdict

with open("inputs/d03") as file:
    lines = [line for line in file.read().split("\n")]
    resolution = len(lines[0])
    data = [c for line in lines for c in line]

def determine_surrounding(indexs, resolution) -> set:
    surrounding = set()
    for i in indexs:
        surrounding.add(i-1)
        surrounding.add(i+1)
        surrounding.add(i - resolution)
        surrounding.add(i-1 - resolution)
        surrounding.add(i+1 - resolution)
        surrounding.add(i + resolution)
        surrounding.add(i-1 + resolution)
        surrounding.add(i+1 + resolution)
    return surrounding

numbers = []
symbols = []
buffer = []
index_buffer = []

for i, v in enumerate(data):
    if v.isdigit():
        buffer.append(v)
        index_buffer.append(i)
    if not v.isdigit() or i % resolution == resolution - 1:
        if len(buffer):
            numbers.append((int("".join(buffer)), index_buffer[:], determine_surrounding(index_buffer, resolution)))
            buffer = []
            index_buffer = []

symbols = [point for point in enumerate(data) if point[1] not in ".0123456789"]

p1 = 0
for value, indexs, surrounding in numbers:
    for i, s in symbols:
        if i in surrounding:
            p1 += value
            break


p2 = defaultdict(list)
for value, indexs, surrounding in numbers:
    for i, s in symbols:
        if s != "*":
            continue
        if i in surrounding:
            p2[i].append(value)
            break


print(p1)
print(sum(v[0] * v[1] for k, v in p2.items() if len(v) == 2))