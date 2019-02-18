#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Materials created for the course of Artificial Intelligence at Faculty of Mathematics, University of Belgrade.
# Materijail napravljeni za kurs ,,Vestacka Inteligencija" na Matematickom fakultetu Univerziteta u Beogradu.
# -------------------------------------------------------------------------------------------------------------------
"""
Primer prikazuje odabir koeficijenata w za model linearne regresije.
"""

import numpy as np


def show_model(model):
    return 'f(height) = {0} + {1}*height'.format(model[0], model[1])

def main():
    height=np.array([4.0, 4.5, 5.0, 5.2, 5.4, 5.8, 6.1, 6.2, 6.4, 6.8])
    weight=np.array([42, 44, 49, 55, 53, 58, 60, 64, 66, 69])

    # Analiticko resenje za odabir koeficijenata 'w'.
    # w = inverse(X.transpose()*X)*X.transpose()*Y

    # Broj instanci u skupu podataka
    N = height.shape[0]

    # Matrici X dodajemo kolonu jedinica kao prvu kolonu.
    # U stvari, napravili smo matricu jedinica pa smo kolonu na indeksu 1
    # zamenili sa vektorom podataka (u nasem slucaju visina).
    X = np.ones((N, 2))
    X[:, 1] = height
    y = weight
    print('X.shape: {}'.format(X.shape))
    print('y.shape: {}'.format(y.shape))

    w = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(y)
    print(show_model(w))

if __name__ == "__main__":
    main()
