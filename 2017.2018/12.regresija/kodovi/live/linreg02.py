#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def main():
    height = np.array([4, 4.5, 5, 5.2, 5.4, 5.8, 6.1, 6.2, 6.4, 6.8])
    weight = np.array([42, 44, 49, 55, 53, 58, 60, 64, 66, 69])

    N = height.shape[0]

    X = np.ones((N, 2))
    X[:, 1] = height
    y = weight

    w = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(y)
    print(w)

    predicted_values = X.dot(w)
    print(predicted_values)

    plt.scatter(height, weight)
    plt.plot(height, predicted_values)
    plt.legend(['data'])
    plt.xlabel('height')
    plt.xlabel('weight')
    plt.show()

if __name__ == "__main__":
    main()
