#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque

class Graph:

    def __init__ (self, start_state, end_state):
        self.start_state = start_state
        self.end_state = end_state

    def reset_marks(self):
        self.marked = {}  

    # Heuristika
    def h(self, n):
        hamming_distance

        '''Studentski kod, funkcija vraca hamingovo rastojanje tekuce niske
            od ciljne niske'''

        return hamming_distance


    def get_neighbors(self, state):
        neighbors = []

        ''' Studentski kod, funkcija generise sve niske koje se razlikuju za jedan karakter
            u odnosu na prosledjenu kao argument'''

        return list(zip(neighbors, [1 for i in range(len(neighbors))]))


    def astar(self, start, stop):
        ''' Studentski kod, kod funkcije A* prilagodjen problemu'''
        return []


def main():
    start_state = 'SECRET'
    end_state = 'PORUKA'

    game = Graph(start_state, end_state)
    print(game.astar(start_state, end_state))

if __name__ == "__main__":
    main()

