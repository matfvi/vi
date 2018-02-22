#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Iz modula ucitava klasu 'Point'
from geometry_util import Point

# Ucitava modul 'geometry'.
# Elementima modula pristupamo preko reference na modul (pogledati kako se instancira pravougaonik)
# Primetimo da na ovaj nacin
import geometry

# Ucitavamo jos neke zanimljive module
import random

# Ako zelimo da ucitamo sve iz module ali bez potrebe da koristimo referencu na modul
# Tada bismo klasi Rectangle pristupili bez 'geometry'.
# from geometry import *

def main():
    a = geometry.Rectangle(Point(0, 0), 10, 20)
    b = geometry.Circle(Point(1, 1), 30)
    c = geometry.Square(Point(3, 3), 40)
    print(a)
    print(b)
    print(c)

    shapes = [a, b, c]
    for shape in shapes:
        # Kako sistemski dobiti ime klase kojoj pripada objekat?
        print("%s P=%g O=%g" % (type(shape).__name__, shape.get_area(), shape.get_circum()))

        # Ime klase koristeci nas apstraktni metod
        # print("%s P=%g O=%g" % (shape.get_type(), shape.get_area(), shape.get_circum()))

if __name__ == "__main__":
    main()
