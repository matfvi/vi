#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

class Tacka:
    """
    Python klase se najcesce dokumentuju na ovaj nacin
    (na primer https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/linear_model/base.py)

    Klasa koja predstavlja tacku u ravni.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        """ Translira tacku za vektor (dx, dy). """
        self.x += dx
        self.y += dy

    # Slicno toString metodu u jeziku Java
    def __str__(self):
        """ Java toString ekvivalent - tekstuelna reprezentacija objekta."""
        return "(%g, %g)" % (self.x, self.y)

    # Oznacavamo funkciju kao staticku koristeci @staticmethod
    @staticmethod
    def euclid_distance(t1, t2):
        """ Izracunava euklidsko rastojanje izmedju tacaka. """
        return math.sqrt((t1.x-t2.x)*(t1.x-t2.x) + (t1.y-t2.y)*(t1.y-t2.y))

    def distance(self, t):
        # Pozivamo staticku funkciju unutar klase Tacka
        return Tacka.euclid_distance(self, t)


def main():
    # Konstruise se objekat klase tacka (ne koristi se kljucna rec new)
    t1 = Tacka(0, 0)
    t1.translate(2, 3)
    print("x koordinata: %g" % t1.x)
    print("y koordinata: %g" % t1.y)
    print(t1)    # poziva __str__

    t2 = Tacka(10, 3)
    print("dist(%s, %s) = %g" % (t1, t2, t1.distance(t2)))

if __name__ == "__main__":
    main()
