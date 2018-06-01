#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Materials created for the course of Artificial Intelligence at Faculty of Mathematics, University of Belgrade.
# Materijail napravljeni za kurs ,,Vestacka Inteligencija" na Matematickom fakultetu Univerziteta u Beogradu.
# -------------------------------------------------------------------------------------------------------------------
"""
Primer upotrebe kNN klasifikatora.
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import sklearn.metrics
import matplotlib.pyplot as plt


class IrisClassifier():
    """
    Klasa prikazuje kako se model masinskog ucenja nakon evaluacije
    (prethodna datoteka) moze obmotati klasom (eng. wrap) i koristit
    u nekom programu kao klasifikator.

    Primetimo da ovde koristimo celokupan skup podataka za predikciju.
    Zasto? A zasto ne? :)
    Naime, podelu na trening i test skup radimo kako bi "procenili" koliko
    model gresi. Tu procenu koristimo da steknemo osecaj da li model
    uopste generalizuje i slicno. Nakon toga, model obucavamo nad svim podacima,
    jer nema potrebe da nepotrebno odbacujemo deo podataka.
    """
    def __init__(self):
        # Ucitavamo podatke
        df = pd.read_csv('./data/iris.csv')

        # Vrsimo odabir atributa za model kao u proslom primeru.
        self._attr1 = 'petal.length'
        self._attr2 = 'petal.width'

        variety = df['variety'].unique()
        # Enkodiramo ciljnu promenljivu u vektor brojeva
        self._encode_target = dict(zip(variety, range(len(variety))))
        # Usput, moze biti korisno da imamo i dekodiranje
        self._decode_target = dict(zip(range(len(variety)), variety))
        self._variety = df['variety'].unique()

        self._X = df[[self._attr1, self._attr2]]
        self._y = df[['variety']].replace(self._encode_target)

        # Pravimo klasifikator
        # Pri konstrukciji objekta mozemo odabrati parametre za algoritam:
        # - n_neighbors -> broj suseda koji se razmatra
        # - weights -> metrika rastojanja ['distance', 'uniform']
        #               uniform  -> svi sused ravnomerno ucestvuju
        #               distance -> sto je sused dalji (d), manje je bitan (1/d)
        self._clf = KNeighborsClassifier(n_neighbors=5, weights='distance')

        # Treniramo nad celim skupom podataka
        self._clf.fit(self._X, self._y.values.ravel())

    def predict(self, sepal_width, sepal_length, petal_width, petal_length):
        """
        Funkcija vrsi predikciju za prosledjene atribute.
        Od korisnika krijemo da nismo koristili sve atribute.
        """
        x_input = np.array([petal_length, petal_width])
        # Biblioteka ne dozvoljava da se prosledi 1d niz vec visedimenzioni niz.
        # U nasem slucaju, posto saljemo jednu instancu sa 2 atributa
        # prosledjujemo (1, 2) umesto (2,)
        # Kako bi to elegantno ucinili, moze se koristit magicna konstanta
        # -1 koja numpy biblioteci kaze da pogleda 1d niz predstavi kao
        # 2d matricu - tamo gde je -1 1d vektor se razmotava po toj dimenziji.
        # https://stackoverflow.com/questions/14126201/performance-standard-using-1d-vs-2d-vectors-in-numpy
        print("Originalni .shape instance: {}".format(x_input.shape))
        x_input = x_input.reshape(1, -1)        # prave shape (1, 2)
        print("Promenjeni .shape instance: {}".format(x_input.shape))
        print(x_input.shape)

        # predict vraca listu predikcija, u nasem slucaju ce vratiti listu
        # duzine 1 pa uzimamo prvi element liste
        prediction = self._clf.predict(x_input)[0]
        # Dekodiramo broj u originalni naziv klase
        decoded_target = self._decode_target[prediction]
        return decoded_target

    def classification_report(self):
        """ Funkcija vraca izvestaj klasifikacije za celokupan iris skup. """
        return sklearn.metrics.classification_report(self._y, self._clf.predict(self._X))

    def accuracy(self):
        """ Funkcija vraca preciznost za celokupan iris skup. """
        return self._clf.score(self._X, self._y)

    def confusion_matrix(self):
        """ Funkcija vraca matricu konfuzije za celokupan iris skup. """
        predicted = self._clf.predict(self._X)
        return sklearn.metrics.confusion_matrix(self._y, predicted)

def main():
    clf = IrisClassifier()
    # [min, max] su uzeti nad iris skupom za svaki atributom.
    # Nismo ograniceni na te vrednosti, uzete su vise za savet
    # korisniku skripte da zna red velicine za atribute.
    sepal_length = float(input("Molimo unesite sepal_length [4.3, 7.9]: "))
    sepal_width = float(input("Molimo unesite sepal_width [2, 4.4]: "))
    petal_length = float(input("Molimo unesite petal_length [1, 6.9]: "))
    petal_width = float(input("Molimo unesite petal_width: [0.1, 2.5]"))

    y = clf.predict(sepal_length, sepal_width, petal_length, petal_width)
    print("Vas cvet je: ... {}".format(y))

    print("Matrica konfuzije:\n{}".format(clf.confusion_matrix()))

if __name__ == "__main__":
    main()
