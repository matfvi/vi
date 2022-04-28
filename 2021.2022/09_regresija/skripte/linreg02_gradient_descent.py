#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def loss_function(X, y, w):
    """
    Funkcija za podatke X, ciljnu promenljivu y i koeficijente w,
    izracunava vrednost funkcije greske i gradijent.
    """

    # Uzimamo broj instanci (radi citljivijeg koda)
    N = y.shape[0]

    # Pravimo gradijent - parcijalni izvodi po svakom w_i
    gradient = np.zeros(w.shape[0])

    # Izracunavamo vektor u kojem su predikcije
    # onoga sto nas model govori za prosledjene podatke.
    predictions = X.dot(w)

    # Izracunavamo vektor koji predstavlja razliku nasih predikcija
    # u odnosu na prave vrednosti ciljen promenljive.
    diff = predictions - y

    # Izracunavamo gradijent
    gradient = 1/N * (X.transpose().dot(diff))

    # Izracunavamo funkciju greske
    loss = 1/(2*N) * np.sum(diff**2)

    return loss, gradient

def gradient_descent(X, y, w, num_iters, alpha):
    # Pravimo inicijalni vektor za funkciju greske (imace onoliko mesta
    # koliko iteracija ima gradijentni spust).
    loss_history = np.zeros((num_iters, 1))

    for i in range(num_iters):
        # Izracunavamo funkciju greske i gradijente.
        loss, gradient = loss_function(X, y, w)

        # Azuriramo (tehnicki 'biramo nove') koeficijente.
        w = w - alpha * gradient

        # Usput belezimo trenutnu vrednost funkcije greske.
        loss_history[i] = loss

        # Belezimo iteraciju na standardnog izlazu.
        print("Iteration {}/{} Loss = {}".format(i+1, num_iters, loss))

    return w, loss_history

def test_primer_1():
    height = np.array([4, 4.5, 5, 5.2, 5.4, 5.8, 6.1, 6.2, 6.4, 6.8])
    weight = np.array([42, 44, 49, 55, 53, 58, 60, 64, 66, 69])
    N = height.shape[0]
    X = np.ones((N, 2))
    X[:, 1] = height
    y = weight.reshape(-1, 1)
    return X, y

def test_primer_2():
    # Uzimamo 50 (podrazumevano je) uniformno raspodeljenih tacaka
    # iz intervala [1, 10]
    height = np.linspace(1, 10)
    N = height.shape[0]

    # Generise podatke sa prave 3x + 2*eps, gde eps (sum) uzimamo
    # iz normalne raspodele N(0, 1).
    weight = height*3 + 2*np.random.normal(size=(1, N))

    # Dodajemo kolonu jedinica iz tehnickih pogodnosti (prva kolona, tj nulta)
    X = np.ones((N, 2))

    # Dodajemo i podatke
    X[:, 1] = height

    # menjamo shape (N,) u (N, 1)
    y = weight.reshape(-1, 1)
    return X, y

def show_model(w):
    return "f_w(x) = %.2f + height*%.2f" % (w[0][0], w[1][0])

def main():
    X, y = test_primer_2()

    print("X.shape = {}".format(X.shape))
    print("y.shape".format(y.shape))

    # Broj iteracija koje ce izvrsiti gradijentni spust.
    num_iters = 40

    # Parametar ucenja - za koliko se pomera gradijentni spust.
    alpha = 0.01

    # Inicijalni koeficijenti modela.
    w = np.zeros((2, 1))

    # Pozivamo gradijentni spust koji nam vraca koeficijente w
    # kojie predstavljaju koeficijente obucenog modela.
    w, loss_history = gradient_descent(X, y, w, num_iters, alpha)
    print(show_model(w))

    # Izracunavamo predikcije naseg modela, trebace nam za crtanje.
    y_predicted = X.dot(w)

    plt.scatter(X[:, 1], y)
    plt.plot(X[:, 1], y_predicted, color='red')
    plt.xlabel('height')
    plt.ylabel('weight')
    plt.legend([show_model(w), 'Data points'])
    plt.show()

    plt.plot(np.arange(num_iters), loss_history)
    plt.show()

if __name__ == "__main__":
    main()

