#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Iz modula ucitava klasu 'Point'
from geometry_util import Point

# Ucitava modul 'geometry'.
# Elementima modula pristupamo preko reference na modul (pogledati kako se instancira pravougaonik)
import geometry

# Ucitavamo jos neke zanimljive module
import random

# Ako zelimo da ucitamo sve iz module ali bez potrebe da koristimo referencu na modul (geometry.Rectangle)
# from geometry import *
# Tada bismo klasi Rectangle pristupili bez 'geometry',
# r = Rectangle(Point(10, 10), 100, 200)

def main():
    r = geometry.Rectangle(Point(10, 10), 100, 200)

    # U listu dodajemo pocetni pravougaonik.
    rects = [r]

    # Generisemo jos nasumicnih 10.
    for i in range(10):
        # pseudoslucajno odabrani brojevi iz intervala [0, 30)
        x = random.randrange(30)
        y = random.randrange(30)
        w = random.randrange(30)
        h = random.randrange(30)
        rects.append(geometry.Rectangle(Point(x, y), w, h))

    for rect in rects:
        print(rect)

if __name__ == "__main__":
    main()
