import re


PATTERN = re.compile(r"[#]+")


with open("input") as file:
    data = [
        (line.split(" ")[0], list(map(int, line.split(" ")[1].split(","))))
        for line in file.read().splitlines()
    ]
REPLACE = {"0": "#", "1": "."}

p1 = 0
for i, row in enumerate(data):
    m = 2 ** row[0].count("?")
    for i in range(m):
        o = str(row[0])
        for v in bin(i)[::-1][:-2]:
            o = REPLACE[v].join(o.rsplit("?", 1))
        o = o.replace("?", "#")
        matches = re.findall(PATTERN, o)
        if matches:
            match_lengths = [len(x) for x in matches]
            p1 += match_lengths == row[1]
print(p1)
