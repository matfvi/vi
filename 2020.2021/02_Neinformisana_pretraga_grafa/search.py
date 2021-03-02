
# depth first traversal
# depth first search
# breath first traversal
# breath first search
# dijkstra

import json

from queue import Queue # deque
from queue import PriorityQueue # heapq



def depth_first_traversal_recursive(adj_list : dict, start_node: str, traversal: list, visisted = set()):
    if start_node in visisted:
        return
    visisted.add(start_node)
    traversal.append(start_node)
    for (next_node, _) in adj_list[start_node]:
        if next_node not in visisted:
            depth_first_traversal_recursive(adj_list, next_node, traversal, visisted)


def depth_first_traversal_iterative(adj_list, start_node, traversal):
    class StackElement:
        def __init__(self, node, next_neighbour_index):
            self.node = node
            self.next_neighbour_index = next_neighbour_index
        def __str__(self):
            return f'({self.node}, {self.next_neighbour_index})'

    visisted = set()
    node_stack : [StackElement] = [StackElement(start_node, -1)]

    while len(node_stack) > 0:
        current: StackElement = node_stack[-1]
        neighbours = adj_list[current.node]
        if current.next_neighbour_index == -1:
            current.next_neighbour_index += 1
            traversal.append(current.node)
            visisted.add(current.node)
        elif current.next_neighbour_index < len(neighbours):
            unvisisted_neighbour_found = False
            while current.next_neighbour_index < len(neighbours):
                (next_node, _) = neighbours[current.next_neighbour_index]
                current.next_neighbour_index += 1
                if next_node not in visisted:
                    node_stack.append(StackElement(next_node, -1))
                    unvisisted_neighbour_found = True
                    break
            # Svi susedi od current su poseceni
            if unvisisted_neighbour_found == False:
                # izbaci current sa steka jer su svi susedi poseceni
                node_stack.pop()
        else:
            node_stack.pop()
    return traversal

def depth_first_search_recrusive(adj_list, start_node, target_node, path, visisted = set()):
    path.append(start_node)
    if start_node == target_node:
        return path
    visisted.add(start_node)
    for (next_node, _) in adj_list[start_node]:
        if next_node not in visisted:
            result = depth_first_search_recrusive(adj_list, next_node, target_node, path, visisted)
            if result is not None:
                return result
    path.pop()
    return None


def breath_first_traversal(adj_list, start_node):
    visisted = set()
    queue = Queue()
    levels = [[]]
    separator_node = None
    queue.put(start_node)
    visisted.add(start_node)
    queue.put(separator_node) 

    while not queue.empty():
        current_node = queue.get()
        if current_node == separator_node:
            if queue.empty():
                break
            queue.put(separator_node)
            levels.append([])
            continue
        levels[-1].append(current_node)
        for (next_node, _) in adj_list[current_node]:
            if next_node not in visisted:
                queue.put(next_node)
                visisted.add(next_node)
    return levels

def breath_first_search(adj_list, start_node, target_node):
    visited = set()
    queue = Queue()
    queue.put(start_node)
    visited.add(start_node)

    parent = dict()
    parent[start_node] = None

    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for (next_node, _) in adj_list[current_node]:
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)
    

    path = []
    if path_found:
        path.append(target_node)
        while True:
            parent_node = parent[target_node]
            if parent_node is None:
                break
            path.append(parent_node)
            target_node = parent[parent_node]
        path.append(start_node)
        path.reverse()
    return path


def dijkstra(adj_list, start_node, target_node):
    visited = set()
    D = {v:float('inf') for v in adj_list}
    D[start_node] = 0

    pq = PriorityQueue()
    pq.put((0, start_node))
    
    parent = dict()
    parent[start_node] = None

    path_found = False
    while not pq.empty():
        (dist, current_node) = pq.get()
        if current_node == target_node:
            path_found = True
            break
        visited.add(current_node)

        for (neighbour, distance_from_current_node) in adj_list[current_node]:
            if neighbour not in visited:
                old_cost = D[neighbour]
                new_cost = D[current_node] + distance_from_current_node
                if new_cost < old_cost:
                    pq.put((new_cost, neighbour))
                    D[neighbour] = new_cost
                    parent[neighbour] = current_node

    path = []
    if path_found:
        path.append(target_node)
        while True:
            parent_node = parent[target_node]
            if parent_node is None:
                break
            path.append(parent_node)
            target_node = parent_node
        path.reverse()
    return path


def all_shortest_paths_distances(adj_list, start_node):
    distances = {start_node:0}
    queue = Queue()
    queue.put(start_node)
    while not queue.empty():
        current_node = queue.get()
        dist = distances[current_node]
        for (neighbour_node, neighbour_distance) in adj_list[current_node]:
            neighbour_distance += dist
            if neighbour_node not in distances:
                queue.put(neighbour_node)
                distances[neighbour_node] = neighbour_distance
            elif neighbour_distance < distances[neighbour_node]:
                distances[neighbour_node] = neighbour_distance
    return distances



if __name__ == '__main__':
    with open('cities.json', 'r') as f:
        adj_list = dict(json.load(f))
        print('DEPTH FIRST TRAVESRAL')
        traversal = []
        depth_first_traversal_recursive(adj_list, 'Oradea', traversal)
        print(traversal)
        print('----------------------')

        print('DEPTH FIRST TRAVESRAL ITERATIVE')
        traversal = []
        depth_first_traversal_iterative(adj_list, 'Oradea', traversal)
        print(traversal)
        print('----------------------')

        print('DEPTH FIRST SEARCH')
        traversal = []
        depth_first_search_recrusive(adj_list, 'Drobeta', 'Lugoj', traversal)
        print(traversal)
        print('----------------------')

        print('BREATH FIRST TRAVESRAL LEVELS')
        traversal = breath_first_traversal(adj_list, 'Drobeta')
        print(traversal)
        print('----------------------')

        print('BREATH FIRST SERACH')
        traversal = breath_first_search(adj_list, 'Drobeta', 'Lugoj')
        print(traversal)
        print('----------------------')

        print('DIJKSTRA SEARCH')
        path = dijkstra(adj_list, 'Drobeta', 'Fagaras')
        print(path)
        print('------------------------------------')

        print('ALL SHORTEST PATHS DISTANCES')
        print(all_shortest_paths_distances(adj_list, 'Drobeta'))

        