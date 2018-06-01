#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def main():
    x = np.linspace(0, 10, 50)
    y1 = np.log(x)
    y2 = np.sqrt(x)
    y3 = x
    y4 = x*np.log(x)
    y5 = x**2

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)
    plt.plot(x, y5)

    plt.title('Matplotlib tutorial')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend([
        'log(x)',
        '$\sqrt{x}$',
        'x',
        'x*log(x)',
        '$x^2$'
    ])
    plt.savefig('the_image_who_escaped.png')
    plt.savefig('the_image_who_escaped.svg')

    plt.show()

if __name__ == "__main__":
    main()
