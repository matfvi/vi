#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

def osnovni_primeri():
    # Generisanje pseudoslucajnih celih brojeva iz opsega [min, max)
    mini = 10
    maksi = 12
    x = random.randrange(mini, maksi)
    print("pseudoslucajni broj iz intervala [%d, %d) -> %d" % (mini, maksi, x))

    # Mozemo i definisati korak
    mini = 1
    maksi = 100
    step = 2
    x = random.randrange(mini, maksi, step)
    print("pseudoslucajni broj iz intervala [%d, %d) sa korakom %d -> %d" % (mini, maksi, step, x))

    # Nasumicno odabiranje elemente iz liste
    xs = [100, 200, 300, 400, 500]
    x = random.choice(xs)
    print("Nasumicno odabran element iz %s je %d" % (str(xs), x))

    # Mesamo listu
    random.shuffle(xs)
    print("Nakon mesanja: %s" % str(xs))

    # Uzimamo k jedinstvenih elemenata iz liste
    the_sample = random.sample(xs, 2)
    print("Primerak velicine 2 je %s" % str(the_sample))


def primeri():
    # Vraca pseudoslucajni broj u pokretnom zarezu iz intervala [0, 1)
    x = random.random()
    print("x iz [0, 1) -> %g" % x)

    # Vraca broj iz uniformne raspodele [a, b]
    x = random.uniform(100, 200)
    print("x iz U(0, 1) -> %g" % x)

    # Vraca broj iz normalne raspodele (mu, sigma)
    mu = 40
    sigma = 20
    x = random.gauss(mu, sigma)
    print("x iz N(%d, %d) -> %g" % (x, mu, sigma))


def main():
    osnovni_primeri()
    primeri()

# Obrazlozenje za koriscenje funkcije 'main'.
# https://stackoverflow.com/questions/4041238/why-use-def-main
if __name__ == "__main__":
    main()

