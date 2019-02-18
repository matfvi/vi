#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
import sklearn.tree
from sklearn.model_selection import train_test_split
import sklearn.metrics
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('iris.csv')
    attribute_1 = 'petal_length'
    attribute_2 = 'petal_width'
    df = df[[attribute_1, attribute_2, 'species']]

    species = df['species'].unique()
    print("Vrsta cveca: {}".format(species))

    X = df[[attribute_1, attribute_2]]
    y = df[['species']]

    changes = dict(zip(species, range(len(species))))
    y = y.replace(changes)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

    clf = sklearn.tree.DecisionTreeClassifier(criterion='gini')
    clf.fit(X_train, y_train)

    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    print("train_acc = {}".format(train_acc))
    print("test_acc = {}".format(test_acc))

    y_test_predict = clf.predict(X_test)
    y_train_predict = clf.predict(X_train)
    test_rep = sklearn.metrics.classification_report(y_test, y_test_predict)
    train_rep = sklearn.metrics.classification_report(y_train, y_train_predict)
    print("test_report = {}".format(test_rep))
    print("train_report = {}".format(train_rep))

if __name__ == "__main__":
    main()
