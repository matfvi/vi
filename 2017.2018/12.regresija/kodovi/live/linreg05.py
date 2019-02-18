#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split


def main():
    df = pd.read_csv('auto-mpg.csv')
    df = df.replace('?', np.nan)
    df = df.dropna()

    X = df.drop('mpg', axis=1)
    y = df[['mpg']]
    print(X.head())

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.25, random_state=42)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    print(reg.coef_)

    print("Slobodan clan (w_0): {}".format(reg.intercept_))
    for id, col in enumerate(X_train.columns):
        print("Koeficijent za {} je {}".format(col, reg.coef_[0][id]))

    y_train_predict = reg.predict(X_train)
    y_test_predict = reg.predict(X_test)

    r2_test = r2_score(y_test, y_test_predict)
    r2_train = r2_score(y_train, y_train_predict)
    print("r2_test = {}".format(r2_test))
    print("r2_train = {}".format(r2_train))

    mse_test = mean_squared_error(y_test, y_test_predict)
    mse_train = mean_squared_error(y_train, y_train_predict)
    print("mse_test = {}".format(mse_test))
    print("mse_train = {}".format(mse_train))

    rmse_test = np.sqrt(mse_test)
    rmse_train = np.sqrt(mse_train)
    print("rmse_test = {}".format(rmse_test))
    print("rmse_train = {}".format(rmse_train))


if __name__ == "__main__":
    main()
