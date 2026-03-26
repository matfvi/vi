from collections import defaultdict


class Edge:
    def __init__(self, start, end, weight: float):
        self.start = start
        self.end = end
        self.weight = weight


BOARD_SIZE = 8


def knight_heuristic(current, target):
    """
    Donja granica za broj poteza skakaca od polja ``current`` do ``target``.

    Ideja heuristike:

    - u jednom potezu skakac menja jednu koordinatu najvise za 2,
    - drugu koordinatu najvise za 1,
    - zbir apsolutnih razlika (`dx + dy`) moze da smanji najvise za 3.

    Zbog toga broj preostalih poteza mora biti bar:

    - ``ceil(dx / 2)`` da bi se nadoknadila veca razlika po x osi,
    - ``ceil(dy / 2)`` da bi se nadoknadila veca razlika po y osi,
    - ``ceil((dx + dy) / 3)`` jer jedan potez ne moze da smanji
      Menhetn rastojanje za vise od 3.

    Maksimum ove tri vrednosti je i dalje donja granica, pa je heuristika
    admisibilna: nikada ne precenjuje stvaran broj poteza do cilja.
    """
    dx = abs(current[0] - target[0])
    dy = abs(current[1] - target[1])
    return max((dx + 1) // 2, (dy + 1) // 2, (dx + dy + 2) // 3)


def iterate_edges(graph, current):
    i, j = current
    neighbours = []
    moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1),
    ]

    for di, dj in moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE:
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


def to_chess_notation(position):
    row, col = position
    return f"{chr(ord('a') + col)}{BOARD_SIZE - row}"


if __name__ == "__main__":
    start = (7, 1)  # b1
    goal = (0, 6)   # g8
    path = astar(None, start, goal, knight_heuristic)

    print("Kretanje skakaca na sahovskoj tabli")
    print("Putanja:", path)
    print("Sahovska notacija:", " -> ".join(to_chess_notation(step) for step in path))
    print("Broj poteza:", len(path) - 1 if path else "nema resenja")
