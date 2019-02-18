#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree
from sklearn.model_selection import train_test_split
import sklearn.metrics
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('./glass.csv')
    print('Nekoliko instanci glass skupa\n{}'.format(df.head()))

    print("\nStatistike iris skupa:\n{}".format(df.describe()))

    # Izdvajamo razlicite klase koje staklo moze imati
    variety = df['glass_type'].unique()
    print("Vrste stakla u skupu podataka: {}".format(variety))

    print('Data:')
    X = df.iloc[:, 1:10]
    y = df[['glass_type']]
    print(X.head())
    print(y.head())
    import sys

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
