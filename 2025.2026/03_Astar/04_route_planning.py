import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location(
    "astar_core",
    Path(__file__).with_name("01_astar.py"),
)
astar_core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(astar_core)

Edge = astar_core.Edge
astar = astar_core.astar


COORDINATES = {
    "Beograd": (0, 0),
    "Novi Sad": (-1, 3),
    "Sabac": (-2, 0),
    "Smederevo": (2, 1),
    "Pozarevac": (4, 1),
    "Jagodina": (6, -1),
    "Kragujevac": (5, -3),
    "Nis": (10, -4),
}


def airline_distance(city_a, city_b):
    ax, ay = COORDINATES[city_a]
    bx, by = COORDINATES[city_b]
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


GRAPH = {
    "Beograd": [
        Edge("Beograd", "Novi Sad", 95),
        Edge("Beograd", "Sabac", 90),
        Edge("Beograd", "Smederevo", 50),
        Edge("Beograd", "Kragujevac", 140),
    ],
    "Novi Sad": [
        Edge("Novi Sad", "Beograd", 95),
        Edge("Novi Sad", "Sabac", 110),
    ],
    "Sabac": [
        Edge("Sabac", "Beograd", 90),
        Edge("Sabac", "Novi Sad", 110),
        Edge("Sabac", "Kragujevac", 160),
    ],
    "Smederevo": [
        Edge("Smederevo", "Beograd", 50),
        Edge("Smederevo", "Pozarevac", 45),
        Edge("Smederevo", "Kragujevac", 95),
    ],
    "Pozarevac": [
        Edge("Pozarevac", "Smederevo", 45),
        Edge("Pozarevac", "Jagodina", 90),
        Edge("Pozarevac", "Nis", 190),
    ],
    "Jagodina": [
        Edge("Jagodina", "Pozarevac", 90),
        Edge("Jagodina", "Kragujevac", 35),
        Edge("Jagodina", "Nis", 110),
    ],
    "Kragujevac": [
        Edge("Kragujevac", "Beograd", 140),
        Edge("Kragujevac", "Sabac", 160),
        Edge("Kragujevac", "Smederevo", 95),
        Edge("Kragujevac", "Jagodina", 35),
        Edge("Kragujevac", "Nis", 150),
    ],
    "Nis": [
        Edge("Nis", "Pozarevac", 190),
        Edge("Nis", "Jagodina", 110),
        Edge("Nis", "Kragujevac", 150),
    ],
}


def path_cost(graph, path):
    total = 0
    for start, end in zip(path, path[1:]):
        for edge in graph[start]:
            if edge.end == end:
                total += edge.weight
                break
    return total


if __name__ == "__main__":
    start = "Beograd"
    goal = "Nis"
    path = astar(GRAPH, start, goal, airline_distance)

    print("Planiranje rute izmedju gradova")
    print("Putanja:", " -> ".join(path))
    print("Ukupna cena:", path_cost(GRAPH, path), "km")
