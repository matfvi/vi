#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Primer koriscenja biblioteke matplotlib za crtaje grafikona funkcija.
"""

import matplotlib.pyplot as plt
import numpy as np


def main():
    # Uzimamo 100 (podrazumevano je 50) ekvidistantnih tacaka iz intervala [1, 5]
    x = np.linspace(1, 5, 100)

    # Izracunavamo funkcije
    y0 = x
    y1 = x * np.log(x)
    y2 = np.sqrt(x)
    y3 = x*x
    y4 = x*x*x

    # Iscrtavamo funkcije, ukoliko ne definisemo sami boju, matplotlib
    # ce vrsiti odabir sam.
    plt.plot(x, y0)
    plt.plot(x, y1, color='aqua')
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)

    # Definisemo labele na osama
    plt.xlabel('x')
    plt.ylabel('y')

    # Redosled elemenata u legendi biblioteka povezuje sa redosledom kojim
    # je izvodjeno crtanje. Dozvoljeno je koristiti i LaTeX formule koje
    # se navode izmedju simbola '$'.
    plt.legend([
        'y = x',
        'y = $x*log(x)$',
        'y = $\sqrt{x}$',
        'y = $x^2$',
        'y = $x^3$',
    ])

    # Mozemo sliku sacuvati na disku
    # PAZNJA: Obavezno uraditi 'savefig' PRE poziva funkcije 'show', inace ce 'savefig'
    # iscrtati prazne slike.
    plt.savefig('funkcije.png')
    plt.savefig('funkcije.pdf')
    plt.savefig('funkcije.svg')
    print('Sacuvane slike.')

    # Prikazujemo prozor u kojem je nacrtana slika
    plt.show()

if __name__ == "__main__":
    main()
