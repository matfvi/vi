#! /usr/bin/env python
# -*- coding: utf-8 -*-

from geometry_util import Point

# Iz modula abc se importuju nadklasa ABC (sablon za apstraktnu klasu - abstract base class),
# a 'abstractmethod' je anotacija kojom oznacavamo da je metod abstraktan.
from abc import ABC, abstractmethod

import math


class BaseShape(ABC):
    def __init__(self, top_left):
        self.top_left = top_left

    def translate(dx, dy):
        self.top_left.translate(dx, dy)

    # pass oznacava praznu naredbu, odnosno za metod ne navodimo implementaciju.
    @abstractmethod
    def get_area(self): pass

    @abstractmethod
    def get_circum(self): pass

    @abstractmethod
    def get_type(self): pass


class Rectangle(BaseShape):
    def __init__(self, top_left, width, height):
        super().__init__(top_left)
        self.height = height
        self.width = width

    def __str__(self):
        return "Rectangle %s w=%g h=%g" % (str(self.top_left), self.width, self.height)

    def get_area(self): return self.width * self.height

    def get_circum(self): return 2*self.width + 2*self.height

    def get_type(self): return "Rectangle"


class Square(Rectangle):
    def __init__(self, top_left, dimension):
        super().__init__(top_left, dimension, dimension)

    def __str__(self):
        return "Square %s d=%g" % (str(self.top_left), self.height)

    def get_type(self): return "Square"


class Circle(BaseShape):
    def __init__(self, top_left, radius):
        super().__init__(top_left)
        self.radius = radius

    def __str__(self):
        return "Circle %s radius=%g" % (str(self.top_left), self.radius)

    def get_area(self):
        return math.pi * math.pi * self.radius

    def get_circum(self):
        return 2 * self.radius * math.pi

    def get_type(self): return "Circle"
