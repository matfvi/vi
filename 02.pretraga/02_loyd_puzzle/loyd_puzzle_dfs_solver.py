#! /usr/bin/env python
# -*- coding: utf-8 -*-

import loyd_puzzle

def main():
    p = loyd_puzzle.Puzzle([
        [3,0,6],
        [1,4,2],
        [7,5,8]
    ])

    solution = p.solveDFS()
    loyd_puzzle.show_solution(solution)

if __name__ == "__main__":
    main()
