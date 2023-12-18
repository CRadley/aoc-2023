from collections import defaultdict

with open("inputs/d15") as file:
    data = file.read().strip().split(",")


def aoc_hash(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


def parse_instruction(instruction):
    if "=" in instruction:
        _i = instruction.split("=")
        return _i[0], "=", int(_i[1])
    return instruction[:-1], "-", None


boxes = defaultdict(list)

print(sum(aoc_hash(value) for value in data))
for value in data:
    label, operation, focal_length = parse_instruction(value)
    hash_value = aoc_hash(label)
    current_labels = [v[0] for v in boxes[hash_value]]
    if operation == "-":
        if label in current_labels:
            index = next(
                (i for i, v in enumerate(boxes[hash_value]) if v[0] == label), None
            )
            if index is None:
                continue
            boxes[hash_value].pop(index)
    else:
        if label in current_labels:
            index = next(
                (i for i, v in enumerate(boxes[hash_value]) if v[0] == label), None
            )
            boxes[hash_value][index][1] = focal_length
        else:
            boxes[hash_value].append([label, focal_length])

p2 = 0
for box in boxes:
    box_value = box + 1
    for j, lens in enumerate(boxes[box]):
        lens_value = j + 1
        p2 += box_value * lens_value * lens[1]
print(p2)
