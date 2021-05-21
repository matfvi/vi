#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Primer koriscenja biblioteke pandas za rad sa podacima.

Iris skup podataka:
https://en.wikipedia.org/wiki/Iris_flower_data_set
"""

import pandas as pd


def main():
    df = pd.read_csv('iris.csv')

    # Prikazujemo prvih 5 instanci iz skupa podataka
    print('Prvih 5 instanci:')
    print(df.head())

    # Izracunavamo neke statistike nad podacima
    print('\nOpis podataka:')
    print(df.describe())

    # Broj elemenata
    print('\nBroj instanci:')
    print(df.size)

    # Dimenzionalnost
    # (150, 5)
    # 150   -> broj instanci
    # 5     -> 5 atributa
    print('\nBroj instanci:')
    print(df.shape)

    print("Kolone (atributi):")
    for col in df.columns:
        print('- {}'.format(col))
    # - sepal_length
    # - sepal_width
    # - petal_length
    # - petal_width
    # - species

    # Uzorkovanje, na primer zelimo da uzmemo 10% uzorka skupa podataka
    df_sample = df.sample(frac=0.1)
    print('\nVelicina uzorka: {}'.format(df_sample.size))

    # Odabir atributa moze biti vrlo bitan korak u koraku pripreme podataka
    # jer dimenzionalnost podataka moze biti visoka. Smanjivanje dimenzionalnosti
    # moze doprineti boljem ponasanju algoritama masinskoug ucenja, te je korisno
    # izostaviti neke atribute.
    # print(df[['sepal_length', 'sepal_width']])

    # ----------------------------------------------------------------------------------------
    # Delimo skup podataka na atribute i ciljnu promenljivu.
    # ----------------------------------------------------------------------------------------
    # Za atribute uzimamo prva 4 atributa u podacima (videti linije 39, 40, 41, 42 u kodu).
    # Funkciju iloc se koristi za odabir vrsti/kolona koristeci indeksiranje brojevima.
    # : kao prva koordinata oznacava da se uzmu sve vrste.
    # 0:4 oznacava da se uzmu prva 4 elemente
    X = df.iloc[:, :4]
    # Slicno smo mogli postici i sa funkcijom 'loc' koja prihvata labele (ime vrste/kolone)
    # X = df.loc[:, ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    # Kraca sintaksa
    # X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    print(X.head())
    y = df['species']

    # Na primer, pretpostavimo da smo primenom neke metode zakljucili da su nam bitni
    # samo atributi sepal_length i sepal_width, a da ostala dva mozemo izostaviti.
    print('\nNakon izostavljanja 2 atributa:')

    X = df[['sepal_length', 'sepal_width']]             # nacin 1
    X = df.iloc[:, :2]                                  # nacin 2
    print(X.head())

if __name__ == "__main__":
    main()
