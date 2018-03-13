#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

if __name__ == "__main__":
    with open("../the_maze.json", "r") as f:
        the_maze = json.load(f)

    output_f = "the_maze.dot"
    with open(output_f, "w") as f:
        f.write("digraph maze {\n")

        the_map = the_maze["map"]
        for (node, neighbours) in the_map.items():
            for neighbour in neighbours:
                f.write("    \"%s\" -> \"%s\";\n" % (node, neighbour[0]))

        f.write("}")
        print("Saved graph at %s" % output_f)
