with open("inputs/d01") as file:
    data = [l for l in file.read().split("\n")]

DIGIT_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def find_next_digit(s) -> int:
    return next(c for c in s if c.isdigit())


def find_next_digit_words(s, reversed) -> int:
    digits = [d[::-1] for d in DIGIT_MAP] if reversed else DIGIT_MAP
    for index in range(len(s)):
        digit = next((d for d in digits if s[index:].startswith(d)), None)
        if digit:
            return digit[::-1] if reversed else digit


def part_one(lines):
    return sum(
        int(
            f"{DIGIT_MAP[find_next_digit(line)]}{DIGIT_MAP[find_next_digit(line[::-1])]}"
        )
        for line in data
    )


def part_two(lines):
    return sum(
        int(
            f"{DIGIT_MAP[find_next_digit_words(line, False)]}{DIGIT_MAP[find_next_digit_words(line[::-1], True)]}"
        )
        for line in data
    )


print(part_one(data))
print(part_two(data))
