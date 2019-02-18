#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Materials for course of Artificial Intelligence.
"""

import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('./data/iris.csv')
    print('Nekoliko instanci iris skupa\n{}'.format(df.head()))

    # Izdvajamo 2 atributa kako bi izvrsili vizuelizaciju (variety ce biti ciljna promenljiva)
    attribute_1 = 'petal.length'
    attribute_2 = 'petal.width'
    df = df[[attribute_1, attribute_2, 'variety']]

    # Izdvajamo razlicite klase koje cvetovi mogu imati (to ce biti 'Versicolor', 'Virginica' i 'Setosa')
    variety = df['variety'].unique()      # ['Setosa', 'Versicolor', 'Virginica']
    print("Vrste cvetova u skupu podataka: {}".format(variety))

    colors = ['red', 'blue', 'green']
    for v, color in zip(variety, colors):
        # Uzimamo sve instance (vrste) kojima je variety = v
        print(v)
        subsamples = df.loc[df['variety'] == v]
        print(subsamples.size)
        plt.scatter(subsamples[attribute_1], subsamples[attribute_2], color=color)

    plt.legend(variety)
    plt.xlabel(attribute_1)
    plt.ylabel(attribute_2)
    plt.show()

    # Na slici mozemo zakljuciti da odabrani atributi lepo razdvajaju klase (primetite kako su tacke iste boje medjusobno "blizu").
    # U sledecem kodu cemo izvrsiti klasifikaciju nad ovim atributima.

if __name__ == "__main__":
    main()

