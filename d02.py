with open("inputs/d02") as file:
    data = [line for line in file.read().split("\n")]


MAX_NUMBER = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def parse_game(game):
    game = game.replace(":", "")
    game = game.replace(";", "")
    game = game.replace(",", "")
    split = game.split(" ")
    game_id = int(split[1])
    for index, element in enumerate(split):
        if element not in MAX_NUMBER:
            continue
        if int(split[index - 1]) > MAX_NUMBER[element]:
            return 0
    return game_id


def parse_game_2(game):
    game = game.replace(":", "")
    game = game.replace(";", "")
    game = game.replace(",", "")
    split = game.split(" ")
    red = []
    green = []
    blue = []
    for index, element in enumerate(split):
        if element not in MAX_NUMBER:
            continue
        if element == "red":
            red.append(int(split[index - 1]))
        elif element == "blue":
            blue.append(int(split[index - 1]))
        elif element == "green":
            green.append(int(split[index - 1]))
    return max(red) * max(green) * max(blue)


p1 = sum(parse_game(line) for line in data)
print(p1)



p2 = sum(parse_game_2(line) for line in data)
print(p2)