#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


def main():
    # Ucitavamo podatke koristeci funkciju 'read_csv' koja nam vraca
    # pandas okvir podataka (eng. dataframe).
    df = pd.read_csv('./data/concrete.csv')

    # Prikazujemo mali podskup podataka kako bi stekli osecaj sa cime radimo.
    print(df.head())

    # Delimo podatke na trening i test skup
    X = df.drop('concrete_compressive_strength', axis=1)
    y = df[['concrete_compressive_strength']]

    # -------------------------------------------------------------------------
    # STUDENTSKI KOD
    # ...
    # -------------------------------------------------------------------------

if __name__ == "__main__":
    main()

