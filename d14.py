from collections import defaultdict

with open("inputs/d14") as file:
    lines = file.read().splitlines()
    resolution = len(lines[0])
    data = [c for l in lines for c in l]


def vertical(data, r=False):
    _data = data[::-1] if r else data[:]
    for i in range(len(_data)):
        j = 0
        if _data[i] in ("#", ".") or i < resolution:
            continue
        while True:
            j += 1
            start = i - resolution * (j - 1)
            end = i - resolution * j
            if _data[end] in ("O", "#") or end < 0:
                break
            _data[end] = "O"
            _data[start] = "."
    return _data[::-1] if r else _data


def horizontal(data, r=False):
    _data = data[::-1] if r else data[:]
    for i in range(len(_data)):
        j = -1
        if _data[i] in ("#", ".") or not i % resolution:
            continue
        while True:
            j += 1
            start = i - j
            end = i - j - 1
            if _data[end] in ("O", "#") or end % resolution == resolution - 1:
                break
            _data[end] = "O"
            _data[start] = "."
    return _data[::-1] if r else _data


def cycle(data):
    d = data[:]
    d = vertical(d)
    d = horizontal(d)
    d = vertical(d, True)
    d = horizontal(d, True)
    return d


def calculate_load(data):
    load_amount = 0
    for i, v in enumerate(data):
        c = v.count("O")
        load_amount += c * (len(data) // resolution - i // resolution)
    return load_amount


p1_data = vertical(data)
p1 = calculate_load(p1_data)

STATES = defaultdict(list)
p2_data = data[:]
for cycle_index in range(1, 1000000000):
    p2_data = cycle(p2_data)
    STATES[tuple(p2_data)].append(cycle_index)

    y = next((s for s in STATES if len(STATES[s]) == 2), None)
    if y:
        break

diff = STATES[y][1] - STATES[y][0]
new_starting = (1000000000 - STATES[y][0]) % diff

final = next((s for s in STATES if new_starting + STATES[y][0] in STATES[s]), None)
p2 = calculate_load(final)

print(p1)
print(p2)
