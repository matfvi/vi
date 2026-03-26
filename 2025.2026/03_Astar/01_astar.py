from typing import List
from collections import defaultdict

class Edge:
    def __init__(self, start, end, weight: float):
        self.start = start
        self.end = end
        self.weight = weight


def iterate_edges(adj_list, current):
    '''https://refactoring.guru/design-patterns/iterator'''
    return adj_list[current]


def astar(graph: List[List[Edge]], start, end, h):

    open_set, closed_set = set([start]), set()

    cheapest_paths = defaultdict(lambda: float('inf'))
    cheapest_paths[start] = 0

    parent = {start: None}
    
    # O(k) gde je k=len(open_set)
    # Može biti implementirano u O(log k) pomoću IndexedPriorityQueue
    def get_best():
        result, result_value = None, float('inf')
        for node in open_set:
            new_value = cheapest_paths[node] + h(node, end)
            if not result or new_value < result_value:
                result, result_value = node, new_value
        return result
    
    path_found = False
    while len(open_set) > 0:
        current = get_best()
        if current == end:
            path_found = True
            break
        for edge in iterate_edges(graph, current):
            neighbour = edge.end
            new_path_to_neighbour_weight = cheapest_paths[current] + edge.weight
            if neighbour not in open_set and neighbour not in closed_set:
                open_set.add(neighbour)
                parent[neighbour] = current
                cheapest_paths[neighbour] = new_path_to_neighbour_weight
            elif new_path_to_neighbour_weight < cheapest_paths[neighbour]:
                parent[neighbour] = current
                cheapest_paths[neighbour] = new_path_to_neighbour_weight
                if neighbour in closed_set:
                    closed_set.remove(neighbour)
                    open_set.add(neighbour)
        open_set.remove(current)
        closed_set.add(current)

    if path_found:
        path = []
        while end is not None:
            path.append(end)
            end = parent[end]
        path.reverse()
        return path
    else:
        return None