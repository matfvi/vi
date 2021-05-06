from z3 import *

A = Array('A', IntSort(), IntSort()) # niz A: Z -> Z
x,y = Ints('x y')
solve(A[x] == x, Store(A,x,y) == A)