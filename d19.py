import re


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
    print(workflow_name)
    for action in workflow:
        if isinstance(action, str):
            if len(action) == 1:
                if action == "A":
                    return 1
                else:
                    return 0
            return process_item(item, action)
        elif CONDITIONS[action[0][1]](item[action[0][0]], action[0][2]):
            return process_item(item, action[1])


p1 = 0
for item in items:
    if process_item(item, "in"):
        p1 += sum(v for v in item.values())
print(p1)
