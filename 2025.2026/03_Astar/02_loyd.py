import math
import json
from typing import List
from collections import defaultdict
import copy

def serialize(matrix):
    return json.dumps(matrix)

def deserialize(value:str):
    return json.loads(value)

def find_in_matrix(value, matrix):
    n = len(matrix)
    m = len(matrix[0])
    for i in range(n):
        for j in range(m):
            if value == matrix[i][j]:
                return i, j
    return None, None


def manhattan_sum(current_node, target_node):
    '''
        Suma menhetn rastojanja izmedju elemenata iz current_matrix i target_matrix
           1|3|2         1|2|3
        A= 4|6|5     B=  4|7|5
           7|8|0         0|8|6
        
        Suma menhetn rastojanja za elemente iz prve matrice u odnosu na elemente iz druge matrice
        H = d(A,B,1) + d(A,B,3) + d(A,B,2) + d(A,B,4) + d(A,B,6)...
        H = 0 + 1 + 1 + 0 + 2 + 0 + 2 + 0 + 2
    '''
    A = deserialize(current_node)
    B = deserialize(target_node)
    n = len(A)
    H = 0
    for i in range(n):
        for j in range(n):
            value = A[i][j]
            target_i, target_j = find_in_matrix(value, B)
            H += abs(i - target_i) + abs(j - target_j)
    return H


class Edge:
    def __init__(self, start, end, weight: float):
        self.start = start
        self.end = end
        self.weight = weight


def iterate_edges(graph, state:str):
    matrix = deserialize(state)
    blank_i, blank_j = -1, -1
    
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0:
                blank_i, blank_j = i, j
                break
    
    neighbours = []
    if blank_i > 0:
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i - 1][blank_j]
        new_matrix[blank_i - 1][blank_j] = 0
        neighbours.append(Edge(matrix, serialize(new_matrix), 1))
    
    if blank_i < (n-1):
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i + 1][blank_j]
        new_matrix[blank_i + 1][blank_j] = 0
        neighbours.append(Edge(matrix, serialize(new_matrix), 1))
    
    if blank_j > 0:
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i][blank_j - 1]
        new_matrix[blank_i][blank_j - 1] = 0
        neighbours.append(Edge(matrix, serialize(new_matrix), 1))
    
    if blank_j < (n-1):
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i][blank_j + 1]
        new_matrix[blank_i][blank_j + 1] = 0
        neighbours.append(Edge(matrix, serialize(new_matrix), 1))
    
    return neighbours


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



if __name__ == '__main__':
    start = [
        [4,1,3],
        [0,2,5],
        [7,8,6]
    ]
    target = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]
    path = astar(None, serialize(start), serialize(target), manhattan_sum)
    print(path)