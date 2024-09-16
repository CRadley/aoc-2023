from collections import deque, defaultdict


def parse_input_file(filepath: str) -> dict[str, set]:
    with open(filepath) as file:
        raw = [line.strip() for line in file.readlines()]
    graph = defaultdict(set)
    for line in raw:
        k = line.split(":")[0]
        vs = line.split(":")[1].strip().split(" ")
        for v in vs:
            graph[v].add(k)
            graph[k].add(v)
    return graph


def create_connections(graph: dict[str, set]) -> set[tuple[str, str]]:
    connections = set()
    for s in graph.keys():
        for d in graph.keys():
            if s == d or d in graph[s]:
                continue
            if (d, s) not in connections:
                connections.add((s, d))
    return connections


def bfs(source: str, previous_paths: set[str], graph: dict[str, set]):
    queue = deque()
    distances = {n: float("inf") for n in graph.keys()}
    distances[source] = 0
    parents = {n: -1 for n in graph.keys()}
    queue.append(source)
    while queue:
        node = queue.popleft()
        for n in graph[node]:
            if n in previous_paths:
                continue
            if distances[n] == float("inf"):
                parents[n] = node
                distances[n] = distances[node] + 1
                queue.append(n)
    return parents, distances


def flood(start: str, graph):
    queue = deque()
    visited = set()
    queue.append(start)
    while queue:
        current = queue.popleft()
        for n in graph[current]:
            if n not in visited:
                visited.add(n)
                queue.append(n)
    return len(visited)


def determine_overall_paths(
    graph: dict[str, set], connections: set[tuple[str, str]]
) -> list[list[str]]:
    overall_paths = []
    for start_node, dest_node in connections:
        previous_paths = set()
        paths = []
        while True:
            parents, distances = bfs(start_node, previous_paths, graph)
            if distances[dest_node] == float("inf"):
                break  # no path found...
            current_path = []
            current_node = dest_node
            while current_node != -1:
                current_path.append(current_node)
                if current_node != start_node and current_node != dest_node:
                    previous_paths.add(current_node)
                current_node = parents[current_node]
            paths.append(current_path[:])
        if len(paths) == 3:
            for path in paths:
                overall_paths.append(path[:])
            if len(overall_paths) == 30:
                return overall_paths
    return overall_paths


def part_one(filepath: str) -> None:
    graph = parse_input_file(filepath)
    connections = create_connections(graph)
    overall_paths = determine_overall_paths(graph, connections)
    l = defaultdict(int)
    for path in overall_paths:
        for i in range(len(path) - 1):
            l[tuple(sorted([path[i], path[i + 1]]))] += 1

    ordered_connections = sorted(
        [(*k, v) for k, v in l.items()], key=lambda x: x[2], reverse=True
    )
    for connection in ordered_connections[:3]:
        graph[connection[0]].remove(connection[1])
        graph[connection[1]].remove(connection[0])
    flood_start = ordered_connections[0][0]
    size = flood(flood_start, graph)
    print(size * (len(graph) - size))


part_one("inputs/d25")
