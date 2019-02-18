#! /usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph


def main():
    g = Graph({
        0: [(2, 1),(1, 10)],
        1: [(0, 1)],
        2: [(2, 1), (1, 1)]
    })
    print("DFS: %s" % str(g.DFS(0, 1)))
    print("BFS: %s" % str(g.BFS(0, 1)))
    print("Dijkstra: %s" % str(g.dijkstra(0, 1)))
    print("A*: %s" % str(g.astar(0, 1)))

if __name__ == "__main__":
    main()
