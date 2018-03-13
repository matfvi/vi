#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random, os, json

output_f = "the_maze.json"

map_FREE = "0"
map_WALL = "1"

def generate_graph_from_map(the_map, n, m):
    """
    Generise graf na osnovu prosledjene liste povezanosti.
    """
    g = {}
    for i in range(n):
        for j in range(m):
            if the_map[i][j] != map_WALL:
                # Trazimo susede cvora (i, j)
                neighbours = []
                if i-1 >= 0 and the_map[i-1][j] != map_WALL:        # gornji sused
                    neighbours.append("%d_%d" % (i-1, j))
                if i+1 < n and the_map[i+1][j] != map_WALL:         # donji sused
                    neighbours.append("%d_%d" % (i+1, j))
                if j-1 >= 0 and the_map[i][j-1] != map_WALL:        # levi sused
                    neighbours.append("%d_%d" % (i, j-1))
                if j+1 < m and the_map[i][j+1] != map_WALL:         # desni sused
                    neighbours.append("%d_%d" % (i, j+1))
                # Susedima dodajemo tezinu grane,
                # pretpostavljamo da je tezina grane 1 radi jednostavnosti.
                 # elegantan nacin da se svim elementima liste dodaju jedinice
                neighbours = list(zip(neighbours, [1]*len(neighbours)))
                g["%d_%d" % (i, j)] = neighbours

    return g

def save_map_as_graph(the_map, n, m):
    """
    Cuva generisani laviring kao .json datoteku.
    Pretpostavlja da lavirint krece iz (0, 0), a da se izlaz nalazi u (n-1, m-1).
    """
    g = generate_graph_from_map(the_map, n, m)

    with open(output_f, "w") as f:
        the_maze = {
            "map": g,
            "start": "0_0",
            "end": "%d_%d" % (n-1, m-1),
            "n": n,
            "m": m,
        }
        json.dump(the_maze, f, indent=4)
        print("Saved to %s" % output_f)

def get_map1():
    return [
        "00000",
        "00110",
        "10010",
        "11000",
    ]

def get_map2():
    return [
        "0000",
        "1110",
        "1110",
        "1110",
    ]

def get_map3():
    return [
        "00010001000100010001000100010001000100011",
        "01000100010001000100010001000100010001000",
        "01111111111111111111111111111111111111110",
        "00000000000000000000000000000000000000000",
    ]

# 0 - free
# 1 - wall
if __name__ == "__main__":
    the_map = get_map3()
    save_map_as_graph(the_map, len(the_map), len(the_map[0]))
