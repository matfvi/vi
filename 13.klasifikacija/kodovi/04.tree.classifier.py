#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Materials created for the course of Artificial Intelligence at Faculty of Mathematics, University of Belgrade.
# Materijail napravljeni za kurs ,,Vestacka Inteligencija" na Matematickom fakultetu Univerziteta u Beogradu.
# -------------------------------------------------------------------------------------------------------------------
"""
Primer upotrebe klasifikatora zasnovanog na stablima odlucivanja.
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree
from sklearn.model_selection import train_test_split
import sklearn.metrics
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('./data/iris.csv')
    print('Nekoliko instanci iris skupa\n{}'.format(df.head()))

    print("\nStatistike iris skupa:\n{}".format(df.describe()))

    # Izdvajamo 2 atributa kako bi izvrsili vizuelizaciju
    # (variety ce biti ciljna promenljiva)
    attribute_1 = 'petal.length'
    attribute_2 = 'petal.width'
    df = df[[attribute_1, attribute_2, 'variety']]

    # Izdvajamo razlicite klase koje cvetovi mogu imati
    # ['Setosa', 'Versicolor', 'Virginica']
    variety = df['variety'].unique()
    print("Vrste cvetova u skupu podataka: {}".format(variety))

    X = df[[attribute_1, attribute_2]]
    y = df[['variety']]

    # Kako bi primenili algoritam, potrebno je da ciljnu promenljivu
    # (tipa string) zamenimo brojevima.
    # Na primer:
    # Setosa -> 0
    # Versicolor -> 1
    # Virginica -> 2
    #
    # Pravimo mapu koja slika ime cveta u njegov broj :)
    changes = dict(zip(variety, range(len(variety))))
    print("Enkodiranje cilje promenljive:\n{}".format(changes))
    # Koristeci mapu, menjamo vrednosti y vektora
    y = y.replace(changes)

    # Delimo skup podataka
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    print("\nVelicina skupa za obucavanje: {}".format(X_train.size))
    print("Velicina skupa za testiranje: {}".format(X_test.size))

    # Pravimo klasifikator
    # Pri konstrukciji objekta mozemo odabrati parametre za algoritam (slede
    # neki)
    # - criterion -> Kriterijum po kojem se vrsi podela u cvorovima
    #               gini    -> Ginijeva funkcija
    #               entropy -> Entropija (videti u knjizi za kurs)
    # - max_depth -> maksimalna dubina stabla
    #               Nekada smanjivanje dubine moze doprineti performansama
    clf = DecisionTreeClassifier(criterion='gini')

    # Treniramo model
    # ravel() prebacuje dimenziju (x, 1) u dimenziju (x,)
    clf.fit(X_train, y_train.values.ravel())

    # Vrsimo predikciju
    y_test_predicted = clf.predict(X_test)
    y_train_predicted = clf.predict(X_train)

    # Izracunavamo preciznost
    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    print('train preciznost: {}'.format(train_acc))
    print('test preciznost: {}'.format(test_acc))

    # Prikazujemo matricu konfuzije
    test_rep = sklearn.metrics.classification_report(y_test, y_test_predicted)
    train_rep = sklearn.metrics.classification_report(y_train, y_train_predicted)
    print("\nTest izvestaj:\n{}".format(test_rep))
    print("Train izvestaj:\n{}".format(train_rep))

    train_conf = sklearn.metrics.confusion_matrix(y_train, y_train_predicted)
    test_conf = sklearn.metrics.confusion_matrix(y_test, y_test_predicted)
    print("Matrica konfuzije za skup za obucavanje:\n{}".format(train_conf))
    print("\nMatrica konfuzije za skup za testiranje:\n{}".format(test_conf))

if __name__ == "__main__":
    main()
