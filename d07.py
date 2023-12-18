from collections import Counter


with open("inputs/d07") as file:
    data = [line.split() for line in file.read().splitlines()]

RANKINGS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
JOKER_RANKINGS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

HAND_VALUES = {
    (5,): 7,
    (4, 1): 6,
    (3, 2): 5,
    (3, 1, 1): 4,
    (2, 2, 1): 3,
    (2, 1, 1, 1): 2,
    (1, 1, 1, 1, 1): 1,
}

UPGRADED_HANDS = {
    (5,): (5,),
    (4, 1): (5,),
    (3, 2): (5,),
    (3, 1, 1): (4, 1),
    (2, 2, 1): [(3, 2), (4, 1)],
    (2, 1, 1, 1): (3, 1, 1),
    (1, 1, 1, 1, 1): (2, 1, 1, 1),
}


def p1_sorter(a):
    return [
        HAND_VALUES[a[3]],
        *[len(RANKINGS) - RANKINGS.index(c) for i, c in enumerate(a[2])],
    ]


def p2_sorter(a):
    return [
        HAND_VALUES[a[3]],
        *[len(JOKER_RANKINGS) - JOKER_RANKINGS.index(c) for i, c in enumerate(a[2])],
    ]


def upgrade(hands):
    upgraded_hands = []
    for h in hands:
        if "J" in h[0]:
            new = UPGRADED_HANDS[h[3]]
            if isinstance(new, list):
                new = new[0] if h[0]["J"] == 1 else new[1]
            upgraded_hands.append((h[0], h[1], h[2], new))
        else:
            upgraded_hands.append(h)
    return upgraded_hands


hands = [
    (
        Counter(r[0]),
        int(r[1]),
        r[0],
        tuple(sorted(Counter(r[0]).values(), reverse=True)),
    )
    for r in data
]

p1 = sorted(hands, key=p1_sorter)
print(sum(h[1] * (i + 1) for i, h in enumerate(p1)))

p2 = sorted(upgrade(hands), key=p2_sorter)
print(sum(h[1] * (i + 1) for i, h in enumerate(p2)))
