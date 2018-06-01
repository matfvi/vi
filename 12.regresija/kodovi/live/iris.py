#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

def main():
    df = pd.read_csv('iris.csv')
    print(df.head())
    attribute_1 = 'petal_length'
    attribute_2 = 'petal_width'

    variety = df['species'].unique()
    print(variety)

    df = df[[attribute_1, attribute_2, 'species']]
    colors = ['red', 'blue', 'green']

    for v, color in zip(variety, colors):
        subsamples = df.loc[df['species'] == v]
        plt.scatter(subsamples[attribute_1], subsamples[attribute_2], color=color)

    plt.legend(variety)
    plt.xlabel(attribute_1)
    plt.ylabel(attribute_2)
    plt.show()


if __name__ == "__main__":
    main()
