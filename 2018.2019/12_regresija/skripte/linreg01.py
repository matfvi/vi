#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Materials created for the course of Artificial Intelligence at Faculty of Mathematics, University of Belgrade.
# Materijail napravljeni za kurs ,,Vestacka Inteligencija" na Matematickom fakultetu Univerziteta u Beogradu.
# -------------------------------------------------------------------------------------------------------------------
"""
Example of linear regression.
"""

from sklearn import linear_model
import matplotlib.pyplot as plt


def show_model(model):
    return 'f(height) = {0} + {1}*height'.format(model.intercept_, model.coef_[0])

def main():
    height=[[4.0],[4.5],[5.0],[5.2],[5.4],[5.8],[6.1],[6.2],[6.4],[6.8]]
    weight=[42, 44 ,49, 55, 53, 58, 60, 64, 66, 69]

    print("height weight")

    for row in zip(height, weight):
        print(row[0][0],"->",row[1])

    plt.scatter(height,weight,color='black')
    plt.xlabel("height")
    plt.ylabel("weight")

    lin_reg = linear_model.LinearRegression()
    lin_reg.fit(height, weight)

    # Show trained model
    print(show_model(lin_reg))

    # Plot the model
    predicted_values = [lin_reg.coef_ * i + lin_reg.intercept_ for i in height]
    # predicted_values = lin_reg.predict(height)
    plt.plot(height, predicted_values, 'b')
    plt.xlabel('height')
    plt.xlabel('weight')
    plt.legend(['Dobijeni model'])
    plt.legend([show_model(lin_reg)])

    plt.show()

if __name__ == "__main__":
    main()
