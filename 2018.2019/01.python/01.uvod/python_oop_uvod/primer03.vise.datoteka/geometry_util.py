#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    # Slicno toString metodu u jeziku Java
    def __str__(self):
        return "(%g, %g)" % (self.x, self.y)

    # Oznacavamo funkciju kao staticku
    @staticmethod
    def euclid_distance(t1, t2):
        return math.sqrt((t1.x-t2.x)*(t1.x-t2.x) + (t1.y-t2.y)*(t1.y-t2.y))

    def distance(self, t):
        # Pozivamo staticku funkciju unutar klase Point
        return Point.euclid_distance(self, t)
