#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def main():
    df = pd.read_csv('iris.csv')

    for col in df.columns:
        print('- {}'.format(col))

    # X = df.iloc[:, :4]
    y = df['species']

    X = df[['sepal_length', 'sepal_width']]
    X = df.iloc[:, :2]

    print(X.head())
    print(y.head())

if __name__ == "__main__":
    main()
