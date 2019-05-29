#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Primer koriscenja biblioteke numpy.
"""

# ---------------------------------------------------------------
# U tekstu ce se pod niz skoro uvek smatrati visedimenzioni niz.
# ---------------------------------------------------------------
import numpy as np

def header(name):
    bar = "-----------------------------------------------------------------------------------"
    print('\n' + bar + '\n' + name + '\n' + bar)

def tutorial00():
    """ Pravljenje numpy nizova. """
    header('Pravljenje numpy nizova.')

    a = np.array([1, 2, 3])             # Pravimo niz duzine 3
    print(type(a))                      # Prikazujemo tip objekta na standardni izlaz
    print(a.shape)                      # "(3,)" (nedostatak drugog indeksa oznacava da je u pitanju niz)
    print(a[0], a[1], a[2])             # "1 2 3" <- indeksiranje
    a[0] = 5                            # Menjanje elementa nizu
    print(a)                            # "[5, 2, 3]"

    b = np.array([[1,2,3],[4,5,6]])     # Pravimo visedimenzioni niz dimenzija (2, 3)
    print(b.shape)                      # "(2, 3)" <- 2 vrste, 3 kolone
    print(b[0, 0], b[0, 1], b[1, 0])    # "1 2 4"
    print(b[0][0], b[0][1], b[1][0])    # "1 2 4"

def tutorial01():
    """ Numpy poseduje nekoliko izuzetno korisnih funkcija za popunjavanje nizova.  """
    header('Generisanje numpy nizova.')

    a = np.zeros((2,2))                 # Pravi se matrica dimenzija (2, 2) ciji su elementi 0
    print(a)                            # "[[ 0.  0.]
                                        #   [ 0.  0.]]"

    b = np.ones((1,2))                  # Pravi se matrica dimenzija (1, 2) ciji su elementi 1
    print(b)                            # "[[ 1.  1.]]"

    c = np.full((2,2), 7)               # Pravi se matrica dimenzija (2, 2) ciji su elementi 7
    print(c)                            # "[[ 7.  7.]
                                        #   [ 7.  7.]]"

    d = np.eye(2)                       # Pravi se jedinicna matrica dimenzija (2, 2)
    print(d)                            # "[[ 1.  0.]
                                        #   [ 0.  1.]]"

    np.random.seed(42)                  # Postavljamo seed ukoliko zelimo da mozemo reprodukovati pseudoslucajne brojeve
    e = np.random.random((2,2))         # Pravi se matrica dimenzija (2, 2) cije su vrednosti iz uniformne raspodele [0, 1]
    print(e)                            # "[[0.37454012 0.95071431]
                                        #  [0.73199394 0.59865848]]""

def tutorial02():
    """ Indeksiranje nizova. """
    header('Indeksiranje nizova.')

    # Pravimo matricu dimenzija (3, 4)
    # [[ 1  2  3  4]
    #  [ 5  6  7  8]
    #  [ 9 10 11 12]]
    a = np.array([[1, 2, 3, 4],  [5, 6, 7, 8],  [9, 10, 11, 12]])
    print("a = \n{}".format(a))

    # Koristimo odsecanje (eng. slicing) da uzmemo podniz koji se
    # sastoji od prve dve vrste, pri cemu uzimamo kolone 1 i 2.
    # Time dobijamo podniz dimenzija (2, 2).
    # [[2 3]
    #  [6 7]]
    b = a[:2, 1:3]
    print("\na[:2, 1:3] = b = \n{}".format(b))

    # Odsecanje ne pravi novi niz vec daje 'pogled' na originalni, tako
    # da ukoliko menjamo dobijeni podniz, menjamo i originalni.
    print(a[0, 1])   # "2"
    b[0, 0] = 77     # b[0, 0] is the same piece of data as a[0, 1]
    print(a[0, 1])   # "77"

def tutorial03():
    """ Racun nad nizovima. """
    header('Racun nad nizovima')

    x = np.array([[1, 2], [3, 4]], dtype=np.float64)
    y = np.array([[5, 6], [7, 8]], dtype=np.float64)
    print('x\n{}'.format(x))
    print('y\n{}\n'.format(x))

    # Pokoordinatno sabiranje
    # [[ 6.0  8.0]
    #  [10.0 12.0]]
    print('x + y\n{}'.format(x + y))
    print('np.add(x, y)\n{}\n'.format(np.add(x, y)))

    # Pokoordinatno oduzimanje
    # [[-4.0 -4.0]
    #  [-4.0 -4.0]]
    print('x - y\n{}'.format(x - y))
    print('np.subtract(x, y)\n{}\n'.format(np.subtract(x, y)))

    # Pokoordinatno mnozenje
    # [[ 5.0 12.0]
    #  [21.0 32.0]]
    print('x * y\n{}'.format(x * y))
    print('np.multiply(x, y)\n{}\n'.format(np.multiply(x, y)))

    # Pokoordinatno deljenje
    # [[ 0.2         0.33333333]
    #  [ 0.42857143  0.5       ]]
    print('x / y\n{}'.format(x / y))
    print('np.divide(x, y)\n{}\n'.format(np.divide(x, y)))

    # Pokoordinatno izracunavanje funkcije 'sqrt'
    # [[ 1.          1.41421356]
    #  [ 1.73205081  2.        ]]
    print('np.sqrt(x)\n{}\n'.format(np.sqrt(x)))

    # Matricno mnozenje se izvodi funkcijom 'dot',
    # i treba biti pazljiv, * izvodi pokoordinatno mnozenje a ne matricno.
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])
    # Matricno mnozenje; proizvodi matricu (2, 2)
    # [[19 22]
    #  [43 50]]
    print('x.dot(y)\n{}'.format(x.dot(y)))
    print('np.dot(x, y)\n{}\n'.format(np.dot(x, y)))

    # 'dot' se moze koristiti i za skalarni proizvod
    v = np.array([9,10])
    w = np.array([11, 12])
    # "219"
    print('v.dot(w)\n{}'.format(v.dot(w)))
    print('np.dot(v, w)\n{}'.format(np.dot(v, w)))

def main():
    print('Dostupni tutoriali:')
    print('0) tutorial00 - pravljenje numpy nizova')
    print('1) tutorial01 - generisanje i popunjavanje numpy nizova')
    print('2) tutorial02 - indeksiranje nizova')
    print('3) tutorial03 - racun nad nizovima')
    i = int(input('Koji tutorial zelite da izvrsite? 0,1,2,3: '))
    tuts = [tutorial00, tutorial01, tutorial02, tutorial03]             # niz funkcija :)
    tuts[i]()                                                           # pozivamo funkciju koju je odabrao korisnik

if __name__ == "__main__":
    main()

