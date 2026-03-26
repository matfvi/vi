from collections import defaultdict


class Edge:
    def __init__(self, start, end, weight: float):
        self.start = start
        self.end = end
        self.weight = weight


MAZE = [
    "S....#....",
    ".##..#..#.",
    ".#...#..#.",
    ".#.#....#.",
    "...#.##...",
    "##.#..##..",
    "...#...#G.",
]


def find_symbol(symbol):
    for i, row in enumerate(MAZE):
        for j, value in enumerate(row):
            if value == symbol:
                return i, j
    return None


def manhattan(current, target):
    return abs(current[0] - target[0]) + abs(current[1] - target[1])


def iterate_edges(graph, current):
    rows = len(MAZE)
    cols = len(MAZE[0])
    i, j = current
    neighbours = []

    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and MAZE[ni][nj] != "#":
            neighbours.append(Edge(current, (ni, nj), 1))

    return neighbours


def astar(graph, start, end, h):
    open_set, closed_set = {start}, set()
    cheapest_paths = defaultdict(lambda: float("inf"))
    cheapest_paths[start] = 0
    parent = {start: None}

    def get_best():
        result, result_value = None, float("inf")
        for node in open_set:
            value = cheapest_paths[node] + h(node, end)
            if result is None or value < result_value:
                result, result_value = node, value
        return result

    while open_set:
        current = get_best()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for edge in iterate_edges(graph, current):
            neighbour = edge.end
            new_weight = cheapest_paths[current] + edge.weight
            if neighbour not in open_set and neighbour not in closed_set:
                open_set.add(neighbour)
                parent[neighbour] = current
                cheapest_paths[neighbour] = new_weight
            elif new_weight < cheapest_paths[neighbour]:
                parent[neighbour] = current
                cheapest_paths[neighbour] = new_weight
                if neighbour in closed_set:
                    closed_set.remove(neighbour)
                    open_set.add(neighbour)

        open_set.remove(current)
        closed_set.add(current)

    return None


def draw_path(path):
    overlay = [list(row) for row in MAZE]
    for i, j in path:
        if overlay[i][j] not in {"S", "G"}:
            overlay[i][j] = "*"
    return "\n".join("".join(row) for row in overlay)


if __name__ == "__main__":
    start = find_symbol("S")
    goal = find_symbol("G")
    path = astar(None, start, goal, manhattan)

    print("Lavirint:")
    print("\n".join(MAZE))
    print()
    print("Najkraca putanja:", path)
    print("Broj koraka:", len(path) - 1 if path else "nema resenja")
    if path:
        print()
        print(draw_path(path))
