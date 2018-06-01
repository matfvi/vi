#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

def main():
    height = np.array([4, 4.5, 5, 5.2, 5.4, 5.8, 6.1, 6.2, 6.4, 6.8])
    weight = np.array([42, 44, 49, 55, 53, 58, 60, 64, 66, 69])

    N = height.shape[0]

    # X = np.ones((N, 2))
    # X[:, 1] = height
    # y = weight

    height = height.reshape((-1, 1))
    weight = weight.reshape((-1, 1))

    print("height.shape = {}".format(height.shape))
    print("weight.shape = {}".format(weight.shape))
    lin_reg = linear_model.LinearRegression()
    # Pokrecemo obucavanje modela
    lin_reg.fit(height, weight)

    predictions = lin_reg.predict(height)
    print(predictions)

    # Koeficijenti
    print("{} + {}*height".format(lin_reg.intercept_[0], lin_reg.coef_[0][0]))

    # predicted_values = X.dot(w)
    # print(predicted_values)

    plt.scatter(height, weight)
    plt.plot(height, predictions)
    plt.legend(['data', 'predictions'])
    plt.xlabel('height')
    plt.xlabel('weight')
    plt.show()

if __name__ == "__main__":
    main()
