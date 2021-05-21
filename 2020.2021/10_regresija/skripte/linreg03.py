#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Materials created for the course of Artificial Intelligence at Faculty of Mathematics, University of Belgrade.
# Materijail napravljeni za kurs ,,Vestacka Inteligencija" na Matematickom fakultetu Univerziteta u Beogradu.
# -------------------------------------------------------------------------------------------------------------------
"""
mpg - Miles per gallon
Mera koja govori o tome koliko milja auto moze ici ukoliko mu se sipa 1 galon (3.785 litara)
Pokusacemo da predvidjamo 'mpg' uz pomoc ostalih atributa koristeci linearnu regresiju.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


def main():
    # Ucitavamo podatke koristeci funkciju 'read_csv' koja nam vraca
    # pandas okvir podataka (eng. dataframe).
    df = pd.read_csv('data/auto-mpg.csv')

    # Prikazujemo mali podskup podataka kako bi stekli osecaj sa cime radimo.
    print(df.head())

    # Nasi podaci imaju sledece atribute:
    # mpg  cylinders  displacement  horsepower  weight  acceleration  model-year

    # Za slucaj da postoje neke nepoznate vrednosti u podacima, uklanjamo te podatke.
    df = df.replace('?', np.nan)
    df = df.dropna()

    # Delimo podatke na trening i test skup
    X = df.drop('mpg', axis=1)          # mpg izostavljamo jer nam predstavlja ciljnu promenljivu
    y = df[['mpg']]

    # Funkcija 'train_test_split' vrsi podelu skupu podataka na trening i test u zavisnosti
    # od prosledjenog odnosa 'test_size'. U nasem slucaju, 25% podataka ce biti uzeto kao
    # test skup, a ostakak (75%) kao trening.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    reg = LinearRegression()
    reg.fit(X_train, y_train)

    print('Slobodan clan je {}\n'.format(reg.intercept_))
    for idx, col_name in enumerate(X_train.columns):
        print('Koeficijent za {} je {}'.format(col_name, reg.coef_[0][idx]))

    # Izracunavamo R^2 metriku
    r2_test = reg.score(X_test, y_test)
    r2_train = reg.score(X_train, y_train)
    print('\nR^2 test = {}'.format(r2_test))
    print('R^2 train = {}'.format(r2_train))
    # Drugi nacin
    # r2_test = r2_score(y_test, reg.predict(X_test))
    # r2_train = r2_score(y_train, reg.predict(X_train))

    # Izracunavamo srednje-kvadratnu gresku
    mse_test = mean_squared_error(y_test, reg.predict(X_test))
    mse_train = mean_squared_error(y_train, reg.predict(X_train))
    print('\nMSE test = {}'.format(mse_test))
    print('MSE train = {}'.format(mse_train))

    # Za koliko milja gresimo prosecno?
    # Izracunacaemo koren srednjekvadratne greske kako bi se vratili u red velicine ciljne promenljive.
    rmse_test = np.sqrt(mse_test)
    rmse_train = np.sqrt(mse_train)
    print('\nRMSE test = {}'.format(rmse_test))
    print('RMSE train = {}'.format(rmse_train))

if __name__ == "__main__":
    main()

