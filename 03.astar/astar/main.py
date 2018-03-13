#! /usr/bin/env python
# -*- coding: utf-8 -*-

from graph import MazeGraph
import json, sys

def create_heuristic(the_maze):
    h = {}
    the_map = the_maze["map"]
    end_coords = the_maze["end"].split("_")
    (end_i, end_j) = (int(end_coords[0]), int(end_coords[1]))
    n = the_maze["n"]
    m = the_maze["m"]
    for i in range(n):
        for j in range(m):
            h["%d_%d" % (i, j)] = abs(end_i - i) + abs(end_j - j)
    return h


if __name__ == "__main__":
    try:
        with open("the_maze.json", "r") as f:
            the_maze = json.load(f)
    except IOError:
        sys.exit("Failed loading input maze.")

    the_map = the_maze["map"]

    g = MazeGraph(the_map, create_heuristic(the_maze))
    start = the_maze["start"]
    end = the_maze["end"]
    print("Dijkstra: %s" % str(g.dijkstra(start, end)))
    print("A*: %s" % str(g.astar(start, end)))

