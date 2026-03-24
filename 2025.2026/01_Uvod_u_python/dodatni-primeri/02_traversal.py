from collections import deque


def dfs(graph, start):
    if start not in graph:
        return []

    visited = set()
    order = []
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue

        visited.add(vertex)
        order.append(vertex)

        for neighbor in reversed(graph.get(vertex, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def bfs(graph, start):
    if start not in graph:
        return []

    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        vertex = queue.popleft()
        order.append(vertex)

        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


EXAMPLE_GRAPH = {
    "Subotica": ["Novi Sad", "Beograd"],
    "Novi Sad": ["Beograd"],
    "Beograd": ["Kragujevac", "Cacak", "Nis"],
    "Kragujevac": ["Nis"],
    "Cacak": ["Nis"],
    "Nis": ["Pirot"],
    "Pirot": [],
}


if __name__ == "__main__":
    print("DFS traversal order:", dfs(EXAMPLE_GRAPH, "Subotica"))
    print("BFS traversal order:", bfs(EXAMPLE_GRAPH, "Subotica"))
