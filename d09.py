with open("inputs/d09") as file:
    sequences = [list(map(int, line.split(" "))) for line in file.read().splitlines()]


expanded = [[] for _ in range(len(sequences))]


for index, sequence in enumerate(sequences):
    current = sequence[:]
    while any(c != 0 for c in current):
        expanded[index].append(current[:])
        current = [current[i] - current[i - 1] for i in range(1, len(current))]
    expanded[index].append(current[:])


for e in expanded:
    r = e[::-1]
    for i, row in enumerate(r):
        if len(set(row)) == 1:
            row.append(row[-1])
            row.insert(0, row[-1])
        else:
            row.append(row[-1] + r[i - 1][-1])
            row.insert(0, row[0] - r[i - 1][0])

print(sum(e[0][-1] for e in expanded))
print(sum(e[0][0] for e in expanded))
