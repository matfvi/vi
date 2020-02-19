#! /usr/bin/env python
# -*- coding: utf-8 -*-

from geometry_util import Point

class Rectangle:
    def __init__(self, top_left, width, height):
        self.top_left = top_left
        self.height = height
        self.width = width

    def __str__(self):
        return "%s w=%g h=%g" % (str(self.top_left), self.width, self.height)
