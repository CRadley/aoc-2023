import re, math, copy

ITEM_PATTERN = re.compile(r"[\d]+")


CONDITIONS = {
    "<": lambda i, j: i < j,
    ">": lambda i, j: i > j,
}


def parse_items(raw_items):
    items = []
    for raw_item in raw_items:
        values = list(map(int, re.findall(ITEM_PATTERN, raw_item)))
        items.append({k: v for k, v in zip(("x", "m", "a", "s"), values)})
    return items


def parse_workflows(raw_workflows):
    workflows = {}
    for raw_workflow in raw_workflows:
        parts = raw_workflow.split("{")
        name = parts[0]
        workflows[name] = []
        actions = parts[1][:-1].split(",")
        for action in actions:
            action_parts = action.split(":")
            if len(action_parts) == 1:
                workflows[name].append(action_parts[0])
            else:
                part = action_parts[0][0]
                condition = action_parts[0][1]
                value = int(action_parts[0][2:])
                workflows[name].append([(part, condition, value), action_parts[1]])
    return workflows


with open("inputs/d19") as file:
    parts = file.read().split("\n\n")
    raw_workflows = parts[0].splitlines()
    raw_items = parts[1].splitlines()
    items = parse_items(raw_items)
    workflows = parse_workflows(raw_workflows)


def process_item(item, workflow_name):
    if workflow_name == "A":
        return 1
    if workflow_name == "R":
        return 0
    workflow = workflows[workflow_name]
    for action in workflow:
        if isinstance(action, str):
            return process_item(item, action)
        elif CONDITIONS[action[0][1]](item[action[0][0]], action[0][2]):
            return process_item(item, action[1])


def determine_valid_ranges(current, workflows, workflow_name):
    valid_ranges = []
    if workflow_name == "A":
        return [current]
    elif workflow_name == "R":
        return [None]
    workflow = workflows[workflow_name]
    for action in workflow:
        if isinstance(action, str):
            valid_ranges.extend(determine_valid_ranges(current, workflows, action))
            continue
        part, condition, value = action[0]
        if condition == "<":
            lower = copy.deepcopy(current)
            lower[part] = (current[part][0], value - 1)
            current[part] = (value, current[part][1])
            valid_ranges.extend(determine_valid_ranges(lower, workflows, action[1]))
        else:
            upper = copy.deepcopy(current)
            upper[part] = (value + 1, current[part][1])
            current[part] = (current[part][0], value)
            valid_ranges.extend(determine_valid_ranges(upper, workflows, action[1]))
    return valid_ranges


p1 = 0
for item in items:
    if process_item(item, "in"):
        p1 += sum(v for v in item.values())
print(p1)

starting_ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}


def determine_valid_range_sum(ranges):
    total = 0
    for valid_range in ranges:
        if valid_range is None:
            continue
        total += math.prod(v[1] - v[0] + 1 for v in valid_range.values())
    return total


valid_ranges = determine_valid_ranges(starting_ranges, workflows, "in")
p2 = determine_valid_range_sum(valid_ranges)
print(p2)
