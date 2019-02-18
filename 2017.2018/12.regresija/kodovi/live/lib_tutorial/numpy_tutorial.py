#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 1, 1], [2, 2, 2]])
    c = a.dot(b)
    c = np.dot(a, b)
    print(c)


if __name__ == "__main__":
    main()
